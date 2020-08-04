import cv2 
import numpy as np 
  
# Let's load a simple image with 3 black squares 
image = cv2.imread('C:/Users/MINU CHAUDHARY/Pictures/PROJECT/hand1.jpg') 

  
# Grayscale 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (3, 3)) # blur the image to remove noise
  
# Find Canny edges 
edged = cv2.Canny(gray, 30, 200)
ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)
 
  
# Finding Contours 
contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
   
# Draw all contours 
# -1 signifies drawing all contours 
cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
  

while(1):

    cv2.imshow('Contours',image)
    cv2.imshow('after Contours',edged)    
    cv2.imshow('threshold', thresh) 
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
