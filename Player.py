from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, TransparencyAttrib
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from SpaceJamClasses import Missile

class SpaceShip(SphereCollideObject):

     

    def __init__(self, loader: Loader, camera : NodePath, taskMgr: TaskManager, accept: Callable[[str, Callable], None],modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):

        super(SpaceShip, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1)

        self.render = parentNode
        self.camera = camera
        self.taskMgr = taskMgr
        self.accept = accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.loader = loader

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)

        self.camera.reparentTo(self.modelNode)
        self.camera.setPos(0, -40, 10)
        self.camera.lookAt(self.modelNode)

        self.setKeyBindings()
        self.reloadTime = .25
        self.missileDistance = 4000
        self.missileBay = 1


    def setKeyBindings(self):

        self.accept('w', self.Thrust, [1])
        self.accept('w-up', self.Thrust, [0])
        # Heading/Yaw (Turning Left/Right)
        self.accept("a", self.Turn, [1, 1])       # Left (positive direction)
        self.accept("a-up", self.Turn, [1, 0])
        self.accept("d", self.Turn, [-1, 1])      # Right (negative direction)
        self.accept("d-up", self.Turn, [-1, 0])

        # Pitch (Pitching Up/Down)
        self.accept("arrow_up", self.Pitch, [1, 1])    # Nose Up
        self.accept("arrow_up-up", self.Pitch, [1, 0])
        self.accept("arrow_down", self.Pitch, [-1, 1])  # Nose Down
        self.accept("arrow_down-up", self.Pitch, [-1, 0])

        # Roll (Banking Left/Right)
        self.accept("q", self.Roll, [1, 1])       # Roll Left
        self.accept("q-up", self.Roll, [1, 0])
        self.accept("e", self.Roll, [-1, 1])      # Roll Right
        self.accept("e-up", self.Roll, [-1, 0])
        self.accept('f', self.Fire)


    def Thrust(self, keyDown):
                if keyDown:
                        base.taskMgr.add(self.ApplyThrust, 'forward-thrust')

                else:
                        base.taskMgr.remove('forward-thrust')

    def ApplyThrust(self, task):
                rate = 25

                trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
                trajectory.normalize()

                self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

                return task.cont


    # YAW LEFT / RIGHT (Z-Axis Rotation)
    def Turn(self, direction, keyDown):
        # direction: 1 for left, -1 for right
        task_name = 'turn-task'
        if keyDown:
            base.taskMgr.add(self.ApplyTurn, task_name, extraArgs=[direction], appendTask=True)
        else:
            base.taskMgr.remove(task_name)

    def ApplyTurn(self, direction, task):
        rate = 2
        # Modifying H (Heading/Yaw) steers the ship left or right
        self.modelNode.setH(self.modelNode.getH() + (rate * direction))
        return task.cont



    # --- PITCH UP / DOWN (X-Axis Rotation) ---
    def Pitch(self, direction, keyDown):
        # direction: 1 for up, -1 for down
        task_name = 'pitch-task'
        if keyDown:
            base.taskMgr.add(self.ApplyPitch, task_name, extraArgs=[direction], appendTask=True)
        else:
            base.taskMgr.remove(task_name)

    def ApplyPitch(self, direction, task):
        rate = 2
        # Modifying P (Pitch) tilts the ship nose up or down
        self.modelNode.setP(self.modelNode.getP() + (rate * direction))
        return task.cont


    #  ROLL LEFT / RIGHT (Y-Axis Rotation) 
    def Roll(self, direction, keyDown):
        # direction: 1 for roll left, -1 for roll right
        task_name = 'roll-task'
        if keyDown:
            base.taskMgr.add(self.ApplyRoll, task_name, extraArgs=[direction], appendTask=True)
        else:
            base.taskMgr.remove(task_name)

    def ApplyRoll(self, direction, task):
        rate = 2
        self.modelNode.setR(self.modelNode.getR() + (rate * direction))
        return task.cont
    
    def Fire(self):
         if self.missileBay:
                travRate = self.missileDistance
                aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())
                aim.normalize()
                fireSolution = aim * travRate
                inFront = aim * 150
                travVec = fireSolution + self.modelNode.getPos()
                self.missileBay -= 1
                tag = 'Missile' + str(Missile.missileCount)

                posVec = self.modelNode.getPos() + inFront
                currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)
                Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
                Missile.Intervals[tag].start()

         else:
          if not self.taskMgr.hasTaskNamed('reload'):
                print("Initializing reload...")
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont



    def Reload(self, task):
        if task.time > self.reloadTime:
             self.missileBay += 1
             print("Reload Complete")

        if self.missileBay>1:
            self.missileBay = 1

        elif task.time <= self.reloadTime:
             print("Reload processing...")
             return Task.cont

        return Task.done

    def CheckIntervals(self, task):
         for i in Missile.Intervals:
              if not Missile.Intervals[i].isPlaying():
                   Missile.cNodes[i].detachNode()
                   Missile.fireModels[i].detachNode()
                   del Missile.Intervals[i]
                   del Missile.fireModels[i]
                   del Missile.cNodes[i]
                   del Missile.collisionSolids[i]
                   print(i + ' has reached the end of its fire solution')
                   break
              return Task.cont
         self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)

    def EnableHUD(self):
         self.Hud = OnscreenImage(image = './Assets/Hud/Reticle3b.png', pos= Vec3(0, 0, 0), scale = 0.1)
         self.Hud.setTransparency(TransparencyAttrib.MAlpha)

            

          




