from panda3d.core import *
from direct.task.Task import TaskManager
import DefensePaths as defensePaths
from CollideObjectBase import *
from panda3d.core import Vec3
from panda3d.core import CardMaker, TransparencyAttrib, ColorBlendAttrib




class Planet(SphereCollideObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, max_hp: 1000):
        super(Planet, self). __init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 1.1)



        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.parentNode = parentNode

 # Create an unscaled dummy node at the planet's position for drones/moons to attach to
        self.droneRoot = parentNode.attachNewNode(nodeName + "droneRoot")
        self.droneRoot.setPos(posVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)
        self.collisionNode.setPythonTag("owner", self)

# 1. Create billboarded health bar container above the planet
        # self.hp_bar_root = self.modelNode.attachNewNode("hp_bar_root")
        # self.hp_bar_root.setPos(0, 0, scaleVec + 100)
        # self.hp_bar_root.reparent_to(parentNode)
        # # self.hp_bar_root.setLightOff()  # Keep colors bright from all angles

        self.max_hp = max_hp
        self.hp = max_hp

        self.bar_width = 400
        self.bar_depth = 10
        self.bar_height = 50
        self.offSet =  Vec3(-(self.bar_width / 2), 0, scaleVec + 100)
        # # 2. Stationary 3D dark background box
        # self.hp_bg = loader.loadModel("models/box")
        # # self.hp_bg.reparentTo(self.hp_bar_root)
        # self.hp_bg.setScale(bar_width, bar_depth, bar_height)
        # self.hp_bg.setPos(0, 0, 0)
        # self.hp_bg.setColor(0.15, 0.15, 0.15, 0.85)
        # # self.hp_bg.setTransparency(True)

        # 3. Left-aligned pivot wrapper for the green health fill
        self.hp_fg_pivot = self.droneRoot.attachNewNode("hp_fg_pivot")
        self.hp_fg_pivot.setPos(self.offSet)

        # Slightly thicker than background box so faces never flicker
        self.hp_fg = loader.loadModel("models/box")
        self.hp_fg.reparentTo(self.hp_fg_pivot)
        self.hp_fg.setScale(self.bar_width, self.bar_depth * 1.08, self.bar_height * 1.08)
        self.hp_fg.setPos(0, 0 ,0)
        self.hp_fg.setTextureOff(1)
        self.hp_fg_pivot.setLightOff(1)
        self.hp_fg.setColor(0.1961, 0.8039, 0.1961, 1.0)

        self.hp_fg_pivot.show()

    def take_damage(self, amount):
             self.hp -= amount
             health_ratio = self.hp / self.max_hp
             self.hp_fg.setScale(self.bar_width * health_ratio, self.bar_depth * 1.08, self.bar_height * 1.08)
             self.hp_fg.setPos(0, 0, 0)
             self.hp_fg.setTextureOff(1)
             self.hp_fg_pivot.setLightOff(1)
             self.hp_fg.setColor(0.1961, 0.8039, 0.1961, 1.0)

             self.hp_fg_pivot.show()
             if health_ratio<=0:
                  self.hp_fg_pivot.hide()

class Sun(SphereCollideObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, max_hp = 1000):
        super(Sun, self). __init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 1.1)



        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)
        self.collisionNode.setPythonTag("owner", self)

# 1. Create billboarded health bar container above the planet
        # self.hp_bar_root = self.modelNode.attachNewNode("hp_bar_root")
        # self.hp_bar_root.setPos(0, 0, scaleVec + 100)
        # self.hp_bar_root.reparent_to(parentNode)
        # # self.hp_bar_root.setLightOff()  # Keep colors bright from all angles

        self.max_hp = max_hp
        self.hp = max_hp

        self.bar_width = 400
        self.bar_depth = 10
        self.bar_height = 50

        # # 2. Stationary 3D dark background box
        # self.hp_bg = loader.loadModel("models/box")
        # # self.hp_bg.reparentTo(self.hp_bar_root)
        # self.hp_bg.setScale(bar_width, bar_depth, bar_height)
        # self.hp_bg.setPos(0, 0, 0)
        # self.hp_bg.setColor(0.15, 0.15, 0.15, 0.85)
        # # self.hp_bg.setTransparency(True)

        # 3. Left-aligned pivot wrapper for the green health fill
        self.hp_fg_pivot = self.modelNode.attachNewNode("hp_fg_pivot")
        self.hp_fg_pivot.setPos(-(self.bar_width/2), 0, scaleVec + 100)
        self.hp_fg_pivot.reparent_to(parentNode)

        # Slightly thicker than background box so faces never flicker
        self.hp_fg = loader.loadModel("models/box")
        self.hp_fg.reparentTo(self.hp_fg_pivot)
        self.hp_fg.setScale(self.bar_width, self.bar_depth * 1.08, self.bar_height * 1.08)
        self.hp_fg.setPos(0, 0, 0)
        self.hp_fg.setTextureOff(1)
        self.hp_fg_pivot.setLightOff(1)
        self.hp_fg.setColor(0.1961, 0.8039, 0.1961, 1.0)

        self.hp_fg_pivot.show()

    def take_damage(self, amount):
             self.hp -= amount
             health_ratio = self.hp / self.max_hp
             self.hp_fg.setScale(self.bar_width * health_ratio, self.bar_depth * 1.08, self.bar_height * 1.08)
             self.hp_fg.setPos(0, 0, 0)
             self.hp_fg.setTextureOff(1)
             self.hp_fg_pivot.setLightOff(1)
             self.hp_fg.setColor(0.1961, 0.8039, 0.1961, 1.0)

             self.hp_fg_pivot.show()
             if health_ratio<=0:
                  self.hp_fg_pivot.hide()
             

  



class Universe(InverseSphereCollideObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self). __init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 0.9)



        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)

class SpaceStation(CapsuleCollidableObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)

        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)





class Drone(SphereCollideObject):

        #How many drones have been spawned
    droneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):

        super(Drone, self). __init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 1.1)



        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)



        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)


class Missile(SphereCollideObject):

    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    Intervals = {}
    count = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
                    super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
    
    
                    self.modelNode.setScale(scaleVec)
                    self.modelNode.setPos(posVec)
                    
                    
                    Missile.count += 1
                    Missile.fireModels[nodeName] = self.modelNode
                    Missile.cNodes[nodeName] = self.collisionNode
    
                    Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
                    Missile.cNodes[nodeName].show()
                    print("Fire missile #" + str(Missile.count))


class Laser(CapsuleCollidableObject):
    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    Intervals = {}
    count = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
        # Build the procedural quad directly under parentNode
        length = 50
        self.modelNode = self.create_laser_bolt(parentNode)
        self.modelNode.setName(nodeName)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)

        # Attach collision solid manually (CollisionBox or CollisionSphere)
        cNode = CollisionNode(nodeName + '_cNode')
        cNode.addSolid(CollisionCapsule(0, 0, 0, 0, length, 0, 1.5))
        self.collisionNode = self.modelNode.attachNewNode(cNode)

        Laser.count += 1
        Laser.fireModels[nodeName] = self.modelNode
        Laser.cNodes[nodeName] = self.collisionNode
        Laser.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Laser.cNodes[nodeName].show()
        print("Fire laser #" + str(Laser.count))

    def create_laser_bolt(self, parentNode, length=50, width=3, color=(1, 0.1, 0.1, 1)):

        bolt_root = parentNode.attachNewNode("laser_bolt")
        cm = CardMaker("laser_beam")
        cm.setFrame(-width / 2, width / 2, 0, length)
        card_geom = cm.generate()

    # Horizontal card (lies flat in XY plane pointing +Y)
        card1 = bolt_root.attachNewNode(card_geom)
        card1.setP(-90)

        # Vertical card (stands upright in YZ plane pointing +Y)
        card2 = bolt_root.attachNewNode(card_geom)
        card2.setHpr(90, 0, 90)
        bolt_root.setLightOff()
        bolt_root.setColorScale(*color)
        bolt_root.setTransparency(TransparencyAttrib.MAlpha)
        bolt_root.setAttrib(ColorBlendAttrib.make(
            ColorBlendAttrib.MAdd,
            ColorBlendAttrib.OIncomingAlpha,
            ColorBlendAttrib.OOne
        ))
        bolt_root.setTwoSided(True)
        return bolt_root


    
                    
class PowerUp(SphereCollideObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                  nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(PowerUp, self). __init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 1.1)



        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)  

class Orbiter(SphereCollideObject):
    numOrbits = 0
    velocity = 0.005
    cloudTimer = 240
    def __init__(self, loader: Loader, taskMgr: TaskManager, modelPath: str, parentNode: NodePath, nodeName: str, scaleVec: Vec3, texPath:str,
         centralObject: PlacedObject, orbitRadius: float, orbitType: str, staringAt: Vec3):
         super(Orbiter, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 3.2)
         self.taskMgr = taskMgr
         self.orbitType = orbitType
         self.modelNode.setScale(scaleVec)
         tex = loader.loadTexture(texPath)
         self.modelNode.setTexture(tex,1)
         self.orbitObject = centralObject
         self.orbitRadius = orbitRadius
         self.staringAt = staringAt
         Orbiter.numOrbits += 1

         self.cloudClock = 9

         self.taskFlag = "Traveler- " + str(Orbiter.numOrbits)
         self.taskMgr.add(self.Orbit, self.taskFlag)
         


    def Orbit(self, task):
            if self.orbitType == "MLB":
                positionVec= defensePaths.BaseballSeams(task.time * Orbiter.velocity, self.numOrbits, 2.0)
                self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

            elif self.orbitType == "Cloud":
                 if self.cloudClock < Orbiter.cloudTimer:
                    self.cloudClock += 1

                 else:
                      self.cloudClock = 0
                      positionVec = defensePaths.Cloud()
                      self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

            self.modelNode.lookAt(self.staringAt.modelNode)
            return task.cont




        
 
