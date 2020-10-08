# import the necessary packages
import cv2
import vehicle_density as vd


# now let's initialize the list of reference point
ref_point = []
print("1111111111111111")
flag=0
areas_list=[]
def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, crop , image,flag

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))

        # draw a rectangle around the region of interest
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        print(ref_point[0])
        print(ref_point[0][0])
        print(ref_point[1])
        cv2.imshow("image", image)
        print("33333333333333")
        areas_list.append(ref_point)
        flag = 1
    print("4444444444444444")
    
if flag==1:
    print("yes")

# load the image, clone it, and setup the mouse callback function
print("22222222222222222")
def image_select(image_path,x):
    global image
    image = cv2.imread(image_path)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", shape_selection)
    
    
    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        print(flag)
    
        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()
            areas_list.clear()
    
        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            print(ref_point[0])
            print(ref_point[0][0])
            print(ref_point[1])
            print(areas_list)
            vd.mainfunc(areas_list,x)
            break 
            
        elif key == ord('q'):
            break               
    # close all open windows
    cv2.destroyAllWindows() 


