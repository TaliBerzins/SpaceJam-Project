from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.showbase.DirectObject import DirectObject



class Planet:

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):

        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)


class Universe:

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):


        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)

class SpaceStation:

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):

        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)





class Drone:

        #How many drones have been spawned
    droneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):

        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)


class SpaceShip(DirectObject):

     

    def __init__(self, loader: Loader, camera : NodePath, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):

        DirectObject.__init__(self)

        self.render = parentNode
        self.camera = camera
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)

        self.camera.reparentTo(self.modelNode)
        self.camera.setPos(0, -40, 10)
        self.camera.lookAt(self.modelNode)

        self.setKeyBindings()


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


    def Thrust(self, keyDown):
                if keyDown:
                        base.taskMgr.add(self.ApplyThrust, 'forward-thrust')

                else:
                        base.taskMgr.remove('forward-thrust')

    def ApplyThrust(self, task):
                rate = 5

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
        rate = .5
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
        rate = .5
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
        rate = .5
        self.modelNode.setR(self.modelNode.getR() + (rate * direction))
        return task.cont


        
 
