import maya.cmds as cmds
import random

def clear_scene():
    all_spheres = cmds.ls()
    cmds.delete(all_spheres)
def create_earth(sun_radius = 4, sun_name = "Earth", moons = 7, moon_radius = 2, min_rotation = -180, max_rotation = 180, min_angle_main = -45, max_angle_main = 45):
    distance = 4
    cmds.polySphere(r=sun_radius, n=sun_name)

    for i in range(moons):
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

clear_scene()
create_earth()
