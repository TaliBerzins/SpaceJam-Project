from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, TransparencyAttrib, CollisionHandlerEvent, CollisionTraverser, CollisionHandlerPusher
from direct.task.Task import TaskManager
from typing import Callable
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
import re
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from SpaceJamClasses import Missile, Sun
import random


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
        self.rate = 25
        self.missileBay = 1
        self.cntExplode = 0
        self.explodeIntervals = {}
        self.traverser = CollisionTraverser()
        self.traverser.traverse(self.render)
        self.taskMgr.add(self.collisionLoop, "collisionTask")


        self.handler = CollisionHandlerEvent()
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)
        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)
        self.EnableHUD()
        self.SetParticles()
        

        


        

    def collisionLoop(self, task):
        # This must be called every single frame manually
        self.traverser.traverse(self.render) 
        return task.cont

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
                

                trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
                trajectory.normalize()

                self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * self.rate)

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

                self.traverser.addCollider(currentMissile.collisionNode, self.handler)
                self.traverser.showCollisions(self.render)



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
         return task.cont


    def EnableHUD(self):
         self.Hud = OnscreenImage(image = './Assets/Hud/Reticle3b.png', pos= Vec3(0, 0, 0), scale = 0.1)
         self.Hud.setTransparency(TransparencyAttrib.MAlpha)

    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode: " + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        tempVar = fromNode.split('_')
        print("tempVar: " + str(tempVar))
        shooter = tempVar[0]
        print("Shooter: " + str(shooter))
        tempVar = intoNode.split('_')
        print("TempVar1: " + str(tempVar))
        tempVar = intoNode.split('_')
        print("TempVar2: " + str(tempVar))
        victim = tempVar[0]
        print("Victim: " + str(victim))
        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)
        print(strippedString)
        if (strippedString == "Drone"  or strippedString == 'Space Station'):
             print(victim, ' hit at ', intoPosition)
             self.DestroyObject(victim, intoPosition)
        elif(strippedString == "Planet"):
             into_np = entry.getIntoNodePath()
             planet_node = into_np.getNetPythonTag('owner')
             if planet_node.hp > 0:
                self.DamageObject(into_np, intoPosition)
             else:
                self.DestroyObject(victim, intoPosition)
        elif(strippedString =="PowerUp"):
             self.RandomPowerUp()

        print(shooter + 'is DONE.')
        Missile.Intervals[shooter].finish()

    def RandomPowerUp(self):
         if random.randint(1, 100) % 2 == 0:
              self.rate *= 10
              print("Speed increased!")
         else:
              self.missileDistance /= 2
              print("Missile slows down")

    def DamageObject(self, nodePath, hitPosition):
         owner = nodePath.getNetPythonTag('owner')
         if owner is not None:
              owner.take_damage(100)

              


    def DestroyObject(self, hitID, hitPosition):

         nodeID = self.render.find("**/" + hitID)
         nodeID.detachNode()

         self.explodeNode.setPos(hitPosition)
         self.Explode()

    def Explode(self):
         self.cntExplode += 1
         tag = 'particles-' + str(self.cntExplode)

         self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
         self.explodeIntervals[tag].start()


    def ExplodeLight(self, t):
         if t == 1.0 and self.explodeEffect:
              self.explodeEffect.disable()

         elif t == 0:
              self.explodeEffect.start(self.explodeNode)

    def SetParticles(self):
         base.enableParticles()
         self.explodeEffect = ParticleEffect()
         self.explodeEffect.loadConfig("./Assets/ParticleEffects/basic_xpld_efx.ptf")
         self.explodeEffect.setScale(20)
         self.explodeNode = self.render.attachNewNode('ExplosionEffects')


            

          




