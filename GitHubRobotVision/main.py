from robodk.robolink import *
from robodk.robomath import *
import TuningAndPicture
import FindPosition
import cv2
import numpy as np
import RobotMovement as RM

# Start the RoboDK API:
RDK = Robolink()
robot = RDK.Item('', ITEM_TYPE_ROBOT)

#Simulation or a live run?
txt_RunningMode= ''
print("Want to run a simulation? (y/n)")
txt_RunningMode = input()

#Setting start position and finden the real coordinates of the three dots
if txt_RunningMode == "y":
    wld_pts = np.array([[258.801, -531.744],[428.648, -348.038], [308.299, -227.688]], np.float32)
    Scaling = 0.65
    target = RDK.Item('Target 1')
    target_pose = target.Pose()
elif txt_RunningMode == "n":
    RDK.setRunMode(RUNMODE_RUN_ROBOT)
    wld_pts=np.array([[223.5, -524.7], [398.5, -354.0], [286.5, -238.5]],np.float32)
    Scaling=0.675
    target=[100,100,50]
    target = RDK.Item('Target 1')
    target_pose = target.Pose()
    xyz_ref = target_pose.Pos()
    robot = RDK.Item('UR5', ITEM_TYPE_ROBOT)

#Moves to start position
robot.MoveL(target_pose)

#Define color in figures
Maggi= "blue","yellow"
Bart="blue", "orange", "yellow"
Lisa="yellow","orange","yellow"
Margs="green","yellow","blue"
Homer="blue","white","yellow"
FigureList={Maggi,Bart,Lisa,Margs,Homer}
ListOfAllColors = "red", "blue", "yellow", "orange", "green", "white"

#-------------------Picture----------------
#Input about tuning the colors in the picture
txt_TuneCamera =''
print("Want to tune colors? (y/n)")
txt_TuneCamera = input()

#Takes a picture and tuning if choosen
img = TuningAndPicture.Take_picture(CameraName="Camera", RunningMode=txt_RunningMode)
if txt_TuneCamera=="y":
    TuningAndPicture.Tune_camera(img, ListOfAllColors, RunningMode=txt_RunningMode)

#-------------Position-------------------
#Get positions and angle of each brick and for the red dots. It also gets the transformation matrix between image and real world.
List_of_Position=[]
for i in ListOfAllColors:
    if i =="red":
        RedDots_img = FindPosition.Find_position(img, i, RunningMode=txt_RunningMode,Scaling=Scaling)
        Transformation_matrix = FindPosition.Transformation(RedDots_img,wld_pts)
    else:
        List_of_Position.append(i)
        Position_list = []
        Call_From_Position_Function = FindPosition.Find_position(img, i, RunningMode=txt_RunningMode,Scaling=Scaling)
        for x in Call_From_Position_Function:
           img_point = np.array([[x[:2]]], dtype=np.float32)
           real_world_points = cv2.transform(img_point,Transformation_matrix)
           real_world_points=real_world_points[0][0][0],real_world_points[0][0][1],x[2]
           Position_list.append(real_world_points)
        List_of_Position.append(Position_list)

#---------------Moves to positions----------------
#Position of first figure
Figure_x=-90
Figure_y=-510

for Figures in FigureList:
    Brick_Middlehight=12
    z_OverBrick=142

    print(Figures)
    for Colors in Figures:
        #Get all the positions for one color
        Points_for_colors = List_of_Position[List_of_Position.index(Colors) + 1]

        #Move over brick and collect it
        RM.MoveRobot(Points_for_colors[0][0],Points_for_colors[0][1],300,(Points_for_colors[0][2]*pi)/180,txt_RunningMode)
        RM.MoveRobot(Points_for_colors[0][0], Points_for_colors[0][1], 148, (Points_for_colors[0][2] * pi) / 180, txt_RunningMode)
        RM.TCP_control("on", txt_RunningMode)
        RM.MoveRobot(Points_for_colors[0][0], Points_for_colors[0][1], 300, (Points_for_colors[0][2] * pi) / 180,txt_RunningMode)

        # Placement of figure
        RM.MoveRobot(Figure_x, Figure_y, 300, 0,txt_RunningMode)
        RM.MoveRobot(Figure_x, Figure_y, z_OverBrick, 0,txt_RunningMode)
        RM.TCP_control("off", txt_RunningMode)
        RM.MoveRobot(Figure_x, Figure_y, 300, 0,txt_RunningMode)

        # Remove the brick from the position list
        position_to_remove = List_of_Position[List_of_Position.index(Colors) + 1].pop(0)
        del position_to_remove
        z_OverBrick = z_OverBrick + 22
    Figure_x = Figure_x + 50
    Figure_y=Figure_y+50
