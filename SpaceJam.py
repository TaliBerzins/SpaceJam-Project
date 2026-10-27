from direct.showbase.ShowBase import ShowBase
import math, sys, random
from panda3d.core import Vec3
import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import Player as playerClasses
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from CollideObjectBase import *


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()





        self.accept('escape', self.quit)


        def setScene(self):
            self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, "Universe", "./Assets/Universe/images.jpeg", (0, 0, 0), 10000)
            self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet1", "./Assets/Planets/images-1.jpeg", (-6000, 6000, -800), 250)
            self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet2", "./Assets/Planets/images-2.jpeg", (0, 6000, 0), 300)
            self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet3", "./Assets/Planets/images-3.png", (500, -5000, 200), 500)
            self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet4", "./Assets/Planets/images-4.png", (300, 6000, 2000), 150)
            self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet5", "./Assets/Planets/images-5.jpeg", (700, -2000, 100), 500)
            self.Planet6 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet6", "./Assets/Planets/images-6.jpeg", (0, -9000, -1400), 700)

            self.SpaceStation1 = spaceJamClasses.SpaceStation(self.loader, "./Assets/Space Station/spaceStation.x", self.render, 'Space Station', "./Assets/Space Station/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)


            self.Hero = playerClasses.SpaceShip(self.loader, self.camera, self.taskMgr, self.accept,"./Assets/Spaceships/Dumbledore.egg", self.render, "Hero", "./Assets/Spaceships/spacejet_N.png", Vec3(1000, 1200, -50), 50)

        setScene(self)
        






        def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
            unitVec = defensePaths.BaseballSeams(step, numSeams, B= 0.4)
            unitVec.normalize()
            position = unitVec * radius * 250 + centralObject.modelNode.getPos()
            spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.x", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position ,5)

        def DrawCloudDefense(self, centralObject, droneName):
            unitVec = defensePaths.Cloud()
            unitVec.normalize()
            position = unitVec * 500 + centralObject.modelNode.getPos()
            spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.x", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5)


        def DrawCircleX(self, centralObject, droneName, theta):
            unitVec = defensePaths.circleX(theta)
            unitVec.normalize()
            position = unitVec * 600 + centralObject.modelNode.getPos()
            spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.x", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5)


        def DrawCircleY(self, centralObject, droneName, theta):
            unitVec = defensePaths.circleY(theta)
            unitVec.normalize()
            position = unitVec * 1000 + centralObject.modelNode.getPos()
            spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.x", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5)


        def DrawCircleZ(self, centralObject, droneName, theta):
            unitVec = defensePaths.circleZ(theta)
            unitVec.normalize()
            position = unitVec * 300  + centralObject.modelNode.getPos()
            spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.x", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5)


        fullCycle = 60

        for j in range(fullCycle):
            theta = j*6
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            DrawCloudDefense(self, self.Planet1, nickName)
            DrawBaseballSeams(self, self.SpaceStation1, nickName, j, fullCycle, 2)
            DrawCircleX(self, self.Planet2, nickName, theta )
            DrawCircleY(self, self.Planet3, nickName, theta )
            DrawCircleZ(self, self.Planet4, nickName, theta)

        self.Hero.setKeyBindings()

        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Hero.collisionNode, self.Hero.modelNode)
        self.cTrav.addCollider(self.Hero.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)

    


  

    def quit(self):
        sys.exit()
    
    


app = MyApp()
app.run()

#Link for planet picture https://www.nbcnews.com/mach/science/what-dwarf-planet-ncna926751
#Link for planet picture - image 6 - https://www.nhm.ac.uk/discover/planet-mercury.html
#Link for planet picture - image 2 - https://esawebb.org/wordbank/planet/
#Link for planet picture - image 3 - https://openlearn.medium.com/what-is-the-weather-like-on-all-8-planets-of-our-solar-system-e99165f4cef3
#Link for planet picture - image 4 - https://www.asc-csa.gc.ca/eng/astronomy/fact-sheets/planet.asp
#Link for planet picture - image 5 - https://www.wired.com/story/scientists-scan-mysterious-planet-as-it-drifts-through-space/
#Universe picture https://www.newscientist.com/article/2524208-100-year-old-assumption-about-the-universe-may-soon-be-overturned/
#Space ship - https://www.artstation.com/artwork/YqvZq


        # # Camera movement
        # self.moveSpeed = 500
        # self.mouseSensitivity = 100

        # # Camera rotation
        # self.cameraHeading = 0
        # self.cameraPitch = 0

        # # Movement keys
        # self.keys = {
        #     "forward": False,
        #     "backward": False,
        #     "left": False,
        #     "right": False,
        #     "up": False,
        #     "down": False
        # }

        # # W/S/A/D
        # self.accept("w", self.setKey, ["forward", True])
        # self.accept("w-up", self.setKey, ["forward", False])

        # self.accept("s", self.setKey, ["backward", True])
        # self.accept("s-up", self.setKey, ["backward", False])

        # self.accept("a", self.setKey, ["left", True])
        # self.accept("a-up", self.setKey, ["left", False])

        # self.accept("d", self.setKey, ["right", True])
        # self.accept("d-up", self.setKey, ["right", False])

        # # Space / Shift
        # self.accept("space", self.setKey, ["up", True])
        # self.accept("space-up", self.setKey, ["up", False])

        # self.accept("shift", self.setKey, ["down", True])
        # self.accept("shift-up", self.setKey, ["down", False])

        # # Mouse
        # self.accept("mouse1", self.startMouseLook)
        # self.accept("mouse1-up", self.stopMouseLook)

        # self.mouseLooking = False

        # # Mouse wheel
        # self.accept("wheel_up", self.moveForward)
        # self.accept("wheel_down", self.moveBackward)

        # # Update every frame
        # self.taskMgr.add(self.updateCamera, "updateCamera")


          # def SetCamera(self) :
            #     self.disableMouse()
            #     self.camera.reparentTo(self.Hero.modelNode)
            #     self.camera.setFluidPos(0, 1, 0)
        
            # def setKey(self, key, value):
            #     self.keys[key] = value
        
        
            # def startMouseLook(self):
            #     self.mouseLooking = True
        
        
            # def stopMouseLook(self):
            #     self.mouseLooking = False
        
        
            # def moveForward(self):
            #     self.camera.setY(self.camera.getY() + 200)
        
        
            # def moveBackward(self):
            #     self.camera.setY(self.camera.getY() - 200)
        
        
            # def updateCamera(self, task):
        
            #     dt = globalClock.getDt()
        
            #     # -------------------------
            #     # Mouse rotation
            #     # -------------------------
        
            #     if self.mouseLooking and self.mouseWatcherNode.hasMouse():
        
            #         mouseX = self.mouseWatcherNode.getMouseX()
            #         mouseY = self.mouseWatcherNode.getMouseY()
        
            #         self.cameraHeading -= mouseX * self.mouseSensitivity * dt
            #         self.cameraPitch += mouseY * self.mouseSensitivity * dt
        
            #         # Prevent camera from flipping upside down
            #         self.cameraPitch = max(-89, min(89, self.cameraPitch))
        
            #         self.camera.setHpr(
            #             self.cameraHeading,
            #             self.cameraPitch,
            #             0
            #         )
        
            #     # -------------------------
            #     # Keyboard movement
            #     # -------------------------
        
            #     movement = Vec3(0, 0, 0)
        
            #     if self.keys["forward"]:
            #         movement.y += 1
        
            #     if self.keys["backward"]:
            #         movement.y -= 1
        
            #     if self.keys["left"]:
            #         movement.x -= 1
        
            #     if self.keys["right"]:
            #         movement.x += 1
        
            #     if self.keys["up"]:
            #         movement.z += 1
        
            #     if self.keys["down"]:
            #         movement.z -= 1
        
            #     # Normalize so diagonal movement isn't faster
            #     if movement.length() > 0:
            #         movement.normalize()
        
            #         movement *= self.moveSpeed * dt
        
            #         # Move relative to camera's orientation
            #         self.camera.setPos(
            #             self.camera,
            #             movement
            #         )
        
            #     return task.cont