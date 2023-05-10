from robodk.robolink import *
from robodk.robomath import *

def MoveRobot(x,y,z,Rotation,RunningMode):
    RDK = Robolink()
    robot = RDK.Item('UR5', ITEM_TYPE_ROBOT)
    if RunningMode == "y":
        target_xyz = ([int(x), int(y), int(z)])
        target = RDK.Item('Target 1')
        target_pose = target.Pose()
        target_pose.setPos(target_xyz)
        robot.MoveL(target_pose* rotz(Rotation))
    elif RunningMode == "n":
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        robot.MoveL(123)
def TCP_control(Control,RunningMode):
    RDK = Robolink()

    if RunningMode=="y":
        tool = RDK.Item('Tool 1', ITEM_TYPE_TOOL)
        if Control=="on":
            tool.AttachClosest()
            tool.RDK().RunProgram('TCP_On')
        elif Control=="off":
            tool.DetachAll(0)
            tool.RDK().RunProgram('TCP_Off')
    else:
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        robot = RDK.Item('UR5', ITEM_TYPE_ROBOT)
        if Control=="on":
            robot.setDO(5,1)
            robot.setDO(4,0)
        elif Control=="off":
            robot.setDO(5,0)
            robot.setDO(4,1)


