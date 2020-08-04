import cv2 
import numpy as np
import math  #inbuilt module in python

#first we configure our webcamera to turn it on
cap = cv2.VideoCapture(0)

#as it is continuous feed so we use an infinite loop
while cap.isOpened():

    #it will check untill the camera is on for live-feed
    
    #now we start reading from live-feed
    #so capture frames from the camera
    ret, frame = cap.read() #output will be in frame variable

    #get hand data from rectangle sub window
    #so we create a rectangle are in frame
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
    crop_image = frame[100:300, 100:300] # here for cropping the image we make out the list using x & y coordinates

    #applying gaussian blur like passing through filter to remove the noise (passing through kernel which has 3,3 value)
    blur = cv2.GaussianBlur(crop_image, (3, 3), 0)

    #now we change the color-space
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #creating a binary image where skin color is white, rest is black.. masking kind of
    #defining the lower values and upper values of hand for filtering out the skin color and store into mask2
    mask2 = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 255, 255]))

    #now we apply dilasion and erosion (to add and remove the pixels) for getting tht value which maybe extracted
    #so we use kernel for morphological transformation
    kernel = np.ones((5, 5))

    #applying morpho trans. to filter out the background noise
    dilation = cv2.dilate(mask2, kernel, iterations=1) #for multiple time dilation => inc iterations
    erosion = cv2.erode(dilation, kernel, iterations=1)

    #after adding or removing the values, we again apply glaussian blur and threshold it
    filtered = cv2.GaussianBlur(erosion, (3, 3), 0)
    ret, thresh = cv2.threshold(filtered, 127, 255, 0)  #thresholding the filtered image

    #for displaying threshold image
    cv2.imshow("threshold",thresh)

    #find contours
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #let we write a try block in which we check remaining things
    try:
        #find contours with max area
        contour = max(contours, key=lambda x: cv2.contourArea(x)) #lambda is anonymous function

        #now we make our bounded rectangle which capture area of hand which will apply on max contour
        #x & y are coordinates and w & h are variables parameters for hand
        #x,y are starting value and x+w,y+h are end values or extended values
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(crop_image,(x,y),(x+w, y+h),(0,0,255), 0)

        #now we find out convex hull on max contour
        #find convex hull around hand
        hull = cv2.convexHull(contour)

        #draw contour
        drawing = np.zeros(crop_image.shape, np.uint8) #this is a separate black window where both o/p will draw
        cv2.drawContours(drawing, [contour],-1,(0,255,0),0)
        cv2.drawContours(drawing, [hull],-1,(0,255,0),0)

        #convexity defects = angles made by points like start, end, farthest and distant points
        #find convexity defects
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour,hull)

        #now we calculate the defects
        #using cosine rule to find an angle of far pt frm start & end pt
        #no of defects calculation algorithm
        count_defects = 0  #shows how many fingers are on screen

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]          #s:start, e:end, f:far, d:distant
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])

            #using math formula of cosine rule to find an angle in trigo
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

            #if angle  > 90, draw a cicle at far pt so tht we can find out the defect
            #and then we draw a line to connect the points
            if angle <=90:
                count_defects +=1
                cv2.circle(crop_image, far, 1, [0,0,255], -1) # -1 so that boundary will be inside 

                cv2.line(crop_image, start, end, [0,255,0], 2)

            #now we count the defects and displaying them
                #print numbers of fingers using defects             

        # Print number of fingers
        if count_defects == 0:
            cv2.putText(frame, "ONE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2)
        elif count_defects == 1:
            cv2.putText(frame, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        elif count_defects == 2:
            cv2.putText(frame, "THREE", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        elif count_defects == 3:
            cv2.putText(frame, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        elif count_defects == 4:
            cv2.putText(frame, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        else:
            pass
    except:
        pass


         #show the recorded images
    cv2.imshow("gesture", frame)
                #horizontal stack is used here => it merge the drawing and cropped output which it will show in all_image
    all_image = np.hstack((drawing, crop_image))  
    cv2.imshow('contours', all_image)
                # Close the camera if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break
               
cap.release()
cv2.destroyAllWindows()
