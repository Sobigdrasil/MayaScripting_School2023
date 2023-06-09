import maya.cmds as cmds

cmds.polySphere( name = "SmallBoy")
cmds.currentTime(1)
cmds.move(-10, 0, 0)
cmds.setKeyframe("SmallBoy")

cmds.currentTime(cmds.playbackOptions(query=1, maxTime=1))
cmds.move(10, 0, 0)
cmds.setKeyframe("SmallBoy")