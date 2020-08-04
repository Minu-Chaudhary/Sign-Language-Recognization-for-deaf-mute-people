import cv2
import numpy as np

#create a black image (bgr configuration)
img = np.zeros((512,512,3), np.uint8)
#img = cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
img = cv2.circle(img,(447,50), 50, (0,255,255), 3)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'Mancu+Pitlu=Rudra',(10,250), font, 1,(255,0,0),2,cv2.LINE_AA)
while(1):

    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    #cv2.imshow('Threshold',the)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
