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
              self.accept("a", self.LeftTurn, [1])
              self.accept("a-up", self.LeftTurn, [0])

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



    def LeftTurn(self, keyDown):
              if keyDown:
                    base.taskMgr.add(self.ApplyLeftTurn, 'left-turn')

              else:
                    base.taskMgr.remove('left-turn')

    def ApplyLeftTurn(self, task):
              # Half a degree every frame.
              rate = .5
              self.modelNode.setH(self.modelNode.getH() + rate)
              return task.cont


        
 
