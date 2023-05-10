import cv2
import numpy as np
import json

def Find_position(img,Color,RunningMode,Scaling):
    Call_backArray=[]
    if RunningMode=="y":
        # reading the data from the Color file
        with open('ColorRangeDataSimulation.txt') as f:
            ColorRangeData = f.read()
        # Changes the width and height to simulations sizes
        w_h_low = 10
        w_h_high = 100
    else:
        # reading the data from the Color file
        with open('ColorRangeData.txt') as f:
            ColorRangeData = f.read()
        # Changes the width and height if we want to find the red dots.
        if Color == "red":
            w_h_low = 10
            w_h_high = 40
        else:
            w_h_low = 30
            w_h_high = 40

    #reconstructing the data as a dictionary
    Color_dict = json.loads(ColorRangeData)
    ColorToInt1 = [int(x) for x in Color_dict[Color][1].split(',')]
    ColorToInt2 = [int(x) for x in Color_dict[Color][0].split(',')]
    color_range = np.array([ColorToInt1, ColorToInt2])

    #Opens the picture.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Defining mask for detecting color
    bin_color=cv2.inRange(hsv,np.array(color_range[0]),np.array(color_range[1]))

    #----------------------------------------------------------
    # In order to draw the contours in the image we need to convert the binary image to BGR
    img_Bricks_gray = cv2.cvtColor(bin_color, cv2.COLOR_GRAY2BGR)

    # Now finding the contours of RED DOTS existing in the image
    Contours, _ = cv2.findContours(bin_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # As FOUR RED DOTS are present we set up the counter
    count = 1

    for contour in Contours:
        # We calculate the paramters of the bounding rectangle placed around the contour
        x_Brick, y_Brick, w_Brick, h_Brick = cv2.boundingRect(contour)

        # To detect only lego BRICKS we check if the width and height are between 40 and 50
        if w_Brick >= w_h_low and w_Brick <= w_h_high and h_Brick >= w_h_low and h_Brick <= w_h_high:

            # We need to calculate the center of the contour using the moments of the image
            cv2.drawContours(img_Bricks_gray, [contour], 0, (0, 0, 255), 2)
            M_Brick = cv2.moments(contour)
            if M_Brick['m00'] != 0:
                cx_Brick = int(M_Brick['m10'] / M_Brick['m00'])
                cy_Brick = int(M_Brick['m01'] / M_Brick['m00'])

            # We then calculate the angle of rotation of the contour using the function: minAreaRect()
            rect_Brick = cv2.minAreaRect(contour)
            box_Brick = cv2.boxPoints(rect_Brick)
            box_Brick = np.intp(box_Brick)
            cv2.drawContours(img_Bricks_gray, [box_Brick], 0, (0, 0, 255), 2)
            cv2.circle(img_Bricks_gray, (cx_Brick, cy_Brick), 2, (0, 0, 255), -1)
            cv2.putText(img_Bricks_gray, Color + str(count), (cx_Brick - 10, cy_Brick - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)
            # Print the information about the detected DOTS
            #print(f"{Color},{count}: center=({cx_Brick},{cy_Brick}), width={w_Brick}, height={h_Brick}")
            # We now set up a matrix containing the parameters of all detected RED DOTS individually
            matrix_Color_position = []
            print(Color,"Img_point",cx_Brick,cy_Brick)
            print(Color,"Wld_point",cx_Brick*Scaling,cy_Brick*Scaling)
            matrix_Color_position.append(cx_Brick*Scaling)
            matrix_Color_position.append(cy_Brick*Scaling)
            matrix_Color_position.append(rect_Brick[2])
            #matrix_Color_position.append(Color)
            #print(matrix_Color_position)
            Call_backArray.append(matrix_Color_position)
            # We now increase the counter
            count += 1


    # And we now display the found contours
    cv2.imshow(Color, img_Bricks_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return Call_backArray


def Transformation(Img_RedDots,wld_pts):
    INT1 = Img_RedDots[0]
    INT1=INT1[:2]
    INT2 = Img_RedDots[1]
    INT2 = INT2[:2]
    INT3 = Img_RedDots[2]
    INT3 = INT3[:2]
    img_pts = np.array([INT1, INT2, INT3],np.float32)

    # Calculate the transformation matrix using cv2.getAffineTransform()
    transformation_matrix = cv2.getAffineTransform(img_pts, wld_pts)

    # Print the transformation matrix

    return transformation_matrix