import maya.cmds as cmds
import random

def clear_scene():
    all_spheres = cmds.ls()
    cmds.delete(all_spheres)
def create_earth(min_sun_radius = 6, max_sun_radius = 12, sun_name = "Earth", min_moons = 1, max_moons = 7, min_moon_radius = 1, max_moon_radius = 3, min_rotation = -180, max_rotation = 180, min_angle_main = -45, max_angle_main = 45):

    sun_radius = random.randint(min_sun_radius, max_sun_radius)
    distance = sun_radius
    cmds.polySphere(r=sun_radius, n=sun_name)
    moons = random.randint(min_moons, max_moons)

    # create shader node
    shader = cmds.shadingNode("lambert", n="lambertRed", asShader=1)

    # set color attribute - now shader has "red" color
    # color must be in range 0..1, i.e. White = 1, Black = 0
    cmds.setAttr(shader + ".color", 1, 0.2, 0.2, type="double3")

    # select object and assign shader to it
    cmds.select("Earth")
    cmds.hyperShade(assign=shader)

    for i in range(moons):

        # create shader node
        shader = cmds.shadingNode("lambert", n="lambertRed", asShader=1)
        # set color attribute - now shader has "red" color
        # color must be in range 0..1, i.e. White = 1, Black = 0
        color_variation = random.random()
        cmds.setAttr(shader + ".color", 1, color_variation, color_variation, type="double3")

        moon_radius = random.randint(min_moon_radius, max_moon_radius)
        s = cmds.polySphere(r=moon_radius)[0]
        r = cmds.polySphere(s, query=True, radius=True)
        distance = distance + 4 + r

        cmds.group()
        around_earth_rotation = random.randint(min_angle_main, max_angle_main)
        cmds.xform(rotation = [0, 0, around_earth_rotation])

        # animation for a moon(s)
        new_rotation = random.randint(min_rotation, max_rotation)
        cmds.xform(s, translation = [distance, 0, 1], rotation = [new_rotation, new_rotation, new_rotation])
        cmds.currentTime(cmds.playbackOptions(query=True, minTime=True))
        cmds.setKeyframe(s, attribute='rotateY')
        cmds.keyTangent(s, edit=True, outTangentType='linear')
        cmds.currentTime(cmds.playbackOptions(query=True, maxTime=True))
        cmds.xform(s, rotation=[0, 680, around_earth_rotation])
        cmds.setKeyframe(s, attribute='rotateY')
        cmds.keyTangent(s, edit=True, inTangentType='linear')

        cmds.ls()

        #pivot offset for a moon rotation around the sun
        current_pivot = cmds.xform(query=True, ws=True, pivots=True)
        translation = [current_pivot[0]-current_pivot[0], 0, 0]
        cmds.xform(pivots=translation, ws=True)

        #animation for a pivot group
        cmds.currentTime(cmds.playbackOptions(query=True, minTime=True))
        cmds.setKeyframe(attribute='rotateY')
        cmds.keyTangent(edit=True, outTangentType='linear')
        cmds.currentTime(cmds.playbackOptions(query=True, maxTime=True))
        cmds.xform(rotation=[0, 360, around_earth_rotation])
        cmds.setKeyframe(attribute='rotateY')
        cmds.keyTangent(edit=True, inTangentType='linear')

        # select object and assign shader to it
        cmds.select()
        cmds.hyperShade(assign=shader)




clear_scene()
create_earth()
