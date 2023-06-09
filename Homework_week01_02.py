import maya.cmds as cmds

cmds.polyCube( name = "BigBoy")
cmds.currentTime(1)
cmds.move(-10, 0, 10)

cmds.parentConstraint("SmallBoy", "BigBoy", maintainOffset = 1)

start=(cmds.playbackOptions(query=1, minTime=1))
end=(cmds.playbackOptions(query=1, maxTime=1))

cmds.bakeResults ( "BigBoy", t=(start, end), simulation=1)

cmds.select("BigBoy")
cmds.delete("BigBoy_parentConstraint1")