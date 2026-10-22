import math, sys, random
from panda3d.core import Vec3


def Cloud(radius =1):

    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1

    unitVec = Vec3(x,y,z)
    unitVec.normalize()

    return unitVec * radius


def BaseballSeams(steps, numSeams, B, F= 1):
    time = steps / float(numSeams) * 2 * math.pi

    F4 = 0

    R = 1

    xxx = math.cos(time) - B * math.cos(3*time)
    yyy = math.sin(time) + B * math.sin(3 * time)
    zzz = F * math.cos(2 * time) + F4 * math.cos(4 * time)

    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)

    x = R * xxx/rrr
    y = R * yyy/rrr
    z = R * zzz/rrr

    return Vec3(x, y ,z)

def circleX(theta,radius=1):

    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    z = 0

    

    unitVec = Vec3(x,y,z)
    unitVec.normalize()

    return unitVec * radius


def circleY(theta,radius=1):

    x = 0
    y = radius * math.sin(theta)
    z = radius * math.tan(theta)

    

    unitVec = Vec3(x,y,z)
    unitVec.normalize()

    return unitVec * radius

def circleZ(theta, radius = 1):

    x = radius * math.cos(theta)
    y = 0
    z = radius * math.tan(theta)

    

    unitVec = Vec3(x,y,z)
    unitVec.normalize()

    return unitVec * radius