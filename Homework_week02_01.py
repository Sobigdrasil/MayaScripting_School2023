import maya.cmds as cmds
import random

def clear_scene():
    all_spheres = cmds.ls()
    cmds.delete(all_spheres)
def create_earth(planet_radius = 4, planet_name = "Earth", moons = 7, moon_radius = 2, min_rotation = -180, max_rotation = 180, min_angle_main = -45, max_angle_main = 45):
    distance = 4
    cmds.polySphere(r=planet_radius, n=planet_name)

    for i in range(moons):
        s = cmds.polySphere(r=moon_radius)[0]
        r = cmds.polySphere(s, query=1, radius=1)
        distance = distance + 5
        cmds.group()
        earth_rotation = random.randint(min_angle_main, max_angle_main)
        cmds.xform(rotation = [0, 0, earth_rotation])
        new_rotation = random.randint(min_rotation, max_rotation)
        cmds.xform(s, translation = [distance, 0, 1], rotation = [new_rotation, new_rotation, new_rotation])
        cmds.ls()
        current_pivot = cmds.xform(query=1, ws=1, pivots=1)
        translation = [current_pivot[0]-current_pivot[0], 0, 0]
        cmds.xform(pivots=translation, ws=True)



clear_scene()
create_earth()

