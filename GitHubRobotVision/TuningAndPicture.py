from robodk.robolink import *
import cv2
import numpy as np
import json

def nothing(x):
    pass

def Tune_camera(img,ListOfColors,RunningMode):
    if RunningMode=="y":
        # reading the data from the Color file
        with open('ColorRangeDataSimulation.txt') as f:
            Color_Data = f.read()
    else:
        # reading the data from the Color file
        with open('ColorRangeData.txt') as f:
            Color_Data = f.read()

    #Makes it a dictionary
    Color_dict = json.loads(Color_Data)

    for x in ListOfColors:
        #Makes the dictionary to ints and set the color range
        int_list1 = [int(x) for x in Color_dict[x][1].split(',')]
        int_list2 = [int(x) for x in Color_dict[x][0].split(',')]
        color_range = np.array([int_list1, int_list2])
        # Create a black image and a window
        cv2.namedWindow(x)

        # create trackbars for color change
        cv2.createTrackbar('H_min', x, 0, 255, nothing)
        cv2.createTrackbar('H_max', x, 0, 255, nothing)
        cv2.createTrackbar('S_min', x, 0, 255, nothing)
        cv2.createTrackbar('S_max', x, 0, 255, nothing)
        cv2.createTrackbar('V_min', x, 0, 255, nothing)
        cv2.createTrackbar('V_max', x, 0, 255, nothing)

        # set start guess for minimum and maximum values
        cv2.setTrackbarPos('H_min', x, color_range[0][0])
        cv2.setTrackbarPos('H_max', x, color_range[1][0])
        cv2.setTrackbarPos('S_min', x, color_range[0][1])
        cv2.setTrackbarPos('S_max', x, color_range[1][1])
        cv2.setTrackbarPos('V_min', x, color_range[0][2])
        cv2.setTrackbarPos('V_max', x, color_range[1][2])

        while True:
            # Convert BGR to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Get current positions of trackbars
            h_min = cv2.getTrackbarPos('H_min', x)
            h_max = cv2.getTrackbarPos('H_max', x)
            s_min = cv2.getTrackbarPos('S_min', x)
            s_max = cv2.getTrackbarPos('S_max', x)
            v_min = cv2.getTrackbarPos('V_min', x)
            v_max = cv2.getTrackbarPos('V_max', x)

            # Define range of colors to filter
            lower_color = np.array([h_min, s_min, v_min])
            upper_color = np.array([h_max, s_max, v_max])

            # Threshold the HSV image to get only selected color
            mask = cv2.inRange(hsv, lower_color, upper_color)

            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(img,img, mask= mask)
            res=cv2.resize(res, (750,350))
            # Display the resulting image
            cv2.imshow(x, res)
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        Color_dict[x][1] = str(h_min) + "," + str(s_min) + "," + str(v_min)
        Color_dict[x][0] = str(h_max) + "," + str(s_max) + "," + str(v_max)
        cv2.destroyAllWindows()

    if RunningMode == "y":
        # reading the data from the Color file
        with open('ColorRangeDataSimulation.txt', 'w') as convert_file:
            convert_file.write(json.dumps(Color_dict))
    else:
        # reading the data from the Color file
        with open('ColorRangeData.txt', 'w') as convert_file:
            convert_file.write(json.dumps(Color_dict))

def Take_picture(CameraName,RunningMode):
    if RunningMode =="n":
        cam = cv2.VideoCapture(1)
        result, image = cam.read()
        return image
    else:
        # Connect to RoboDK
        RDK = Robolink()
        #Takes a picture and saves it
        cam = RDK.Item(CameraName, ITEM_TYPE_CAMERA)
        RDK.Cam2D_Snapshot("Picture.png", cam)

        return cv2.imread("Picture.png")


