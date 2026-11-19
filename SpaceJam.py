from direct.showbase.ShowBase import ShowBase
import math, sys, random
from panda3d.core import Vec3
import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import Player as playerClasses
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from CollideObjectBase import *
from direct.task.Task import Task
from direct.task.Task import TaskManager
from direct.actor.Actor import Actor





class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        self.setScene()
        self.taskMgr.add(self.orbit_task, "OrbitTask")
        self.Hero.setKeyBindings()

        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Hero.collisionNode, self.Hero.modelNode)
        self.cTrav.addCollider(self.Hero.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)









        self.accept('escape', self.quit)


    def setScene(self):
            self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, "Universe", "./Assets/Universe/images.jpeg", (0, 0, 0), 10000)
            self.Sun = spaceJamClasses.Sun(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet3", "./Assets/Planets/images-3.png", (0, 0, 0), 500, 1000)

            self.planet1_orbit = self.render.attachNewNode("planet1_orbit")
            self.planet2_orbit = self.render.attachNewNode("planet2_orbit")
            self.planet2_orbit.setPos(-4000, 0, -4000)

            self.planet3_orbit = self.render.attachNewNode("planet3_orbit")
            self.planet4_orbit = self.render.attachNewNode("planet4_orbit")
            self.planet5_orbit = self.render.attachNewNode("planet5_orbit")

            self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.planet1_orbit, "Planet1", "./Assets/Planets/images-1.jpeg", (0, 6000, 0), 250, 1000)
            self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.planet2_orbit, "Planet2", "./Assets/Planets/images-2.jpeg", (0, 1400, 0), 300, 1000)
            self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.planet3_orbit, "Planet3", "./Assets/Planets/images-4.png", (0, 2500, 0), 150, 1000)
            self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.planet4_orbit, "Planet4", "./Assets/Planets/images-5.jpeg", (0, 3500, 0), 200, 1000)
            self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.planet5_orbit, "Planet5", "./Assets/Planets/images-6.jpeg", (0, 4500, 0), 300, 1000)

            self.SpaceStation1 = spaceJamClasses.SpaceStation(self.loader, "./Assets/Space Station/spaceStation.x", self.render, 'Space Station', "./Assets/Space Station/SpaceStation1_Dif2.png", (1500, 1000, -2000), 40)


            self.Hero = playerClasses.SpaceShip(self.loader, self.camera, self.taskMgr, self.accept,"./Assets/Spaceships/Dumbledore.egg", self.render, "Hero", "./Assets/Spaceships/spacejet_N.png", Vec3(1000, 1200, -50), 50)
            self.powerUp = spaceJamClasses.PowerUp(self.loader, "./Assets/Player/sphere.egg", self.render, "PowerUp", "./Assets/Player/sphere1_auv.jpg", (2000, 1500, -1500), 100)
            self.Sentinal1 = spaceJamClasses.Orbiter(self.loader, self.taskMgr,  "./Assets/DroneDefender/DroneDefender.x", self.Planet2.droneRoot, "Drone", 6.0,  "./Assets/DroneDefender/octotoad1_auv.png", self.Planet2, 900, "MLB", self.Hero)
            self.Sentinal2 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/DroneDefender.x", self.Planet5.droneRoot, "Drone", 6.0,  "./Assets/DroneDefender/octotoad1_auv.png", self.Planet5, 500, "Cloud", self.Hero)
            self.Sentinal3 = spaceJamClasses.Orbiter(self.loader, self.taskMgr,  "./Assets/DroneDefender/DroneDefender.x", self.Planet2.droneRoot, "Drone", 6.0,  "./Assets/DroneDefender/octotoad1_auv.png", self.Planet2, 700, "MLB", self.Hero)
            self.Sentinal4 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/DroneDefender.x", self.Planet5.droneRoot, "Drone", 6.0,  "./Assets/DroneDefender/octotoad1_auv.png", self.Planet5, 300, "Cloud", self.Hero)
    


            def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
                    unitVec = defensePaths.BaseballSeams(step, numSeams, B= 0.4)
                    unitVec.normalize()
                    position = unitVec * radius * 250 + centralObject.modelNode.getPos()
                    spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.x", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position ,5)

            def DrawCloudDefense(self, centralObject, droneName):
                    unitVec = defensePaths.Cloud()
                    unitVec.normalize()
                    position = unitVec * 600 

                    spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.x", centralObject.droneRoot, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)


            def DrawCircleX(self, centralObject, droneName, theta):
                    unitVec = defensePaths.circleX(theta)
                    unitVec.normalize()
                    position = unitVec * 600 
                    spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.x", centralObject.droneRoot, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)


            def DrawCircleY(self, centralObject, droneName, theta):
                    unitVec = defensePaths.circleY(theta)
                    unitVec.normalize()
                    position = unitVec * 1000 + centralObject.modelNode.getPos()
                    spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.x", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)


            def DrawCircleZ(self, centralObject, droneName, theta):
                    unitVec = defensePaths.circleZ(theta)
                    unitVec.normalize()
                    position = unitVec * 300  
                    spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.x", centralObject.droneRoot, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)


            fullCycle = 60

            for j in range(fullCycle):
                        theta = j*6
                        spaceJamClasses.Drone.droneCount += 1
                        nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

                        DrawCloudDefense(self, self.Planet1, nickName)
                        DrawBaseballSeams(self, self.SpaceStation1, nickName, j, fullCycle, 2)
                        DrawCircleX(self, self.Planet2, nickName, theta )
                        DrawCircleY(self, self.Sun, nickName, theta )
                        DrawCircleZ(self, self.Planet4, nickName, theta)

                     # 4. Add a task to rotate the orbit root every frame

    def orbit_task(self, task):
            # Rotate the orbit root node around the Z-axis
            # task.time * speed controls the orbital velocity
            orbit_speed = 20.0  #degrees per second
  # Rotates Planet1's separate orbit root around the Sun in the opposite direction
            self.planet1_orbit.setH(task.time * (orbit_speed * -1))
            self.Planet1.modelNode.setH(task.time * 50.0)  
            self.planet2_orbit.setH(task.time * (orbit_speed * 1))
            self.Planet2.modelNode.setH(task.time * 50.0)   
            self.planet3_orbit.setH(task.time * (orbit_speed * -1))
            self.Planet3.modelNode.setH(task.time * 50.0)  
            self.planet4_orbit.setH(task.time * (orbit_speed * 1)) 
            self.Planet4.modelNode.setH(task.time * 50.0)   
            self.planet5_orbit.setH(task.time * (orbit_speed * -1))
            self.Planet5.modelNode.setH(task.time * 50.0)  
            return Task.cont

 

  

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