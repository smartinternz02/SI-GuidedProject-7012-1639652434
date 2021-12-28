# Importing of Libraries
# Importing of opencv library
import cv2
# Importing of time library for adding delays
import time
# Import Client library from twilio
from twilio.rest import Client

# Adding testing video path
cam = cv2.VideoCapture(r'Testing.mp4')
# Initialising Backgound Subtractor
bg = cv2.createBackgroundSubtractorMOG2()
j = 0

# Main function 
while(1):
    # Reading the frames from the Video Streaming
    ret, frame = cam.read()
    #gray scaling of detected fromes
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fg = bg.apply(gray)
    # Intialising Contour 
    contours, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    if contours:
        areas = []
        for contour in contours:
            ar = cv2.contourArea(contour) # Defining Contour Area
            areas.append(ar) # Appending the Area
        max_area = max(areas or [0])
        max_area_index = areas.index(max_area)
        cnt = contours[max_area_index]
        M = cv2.moments(cnt)
        # Drawing the bounding box to the frames
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.drawContours(fg, [cnt], 0, (255,255,255), 3, maxLevel = 0)
        if h < w:
            j += 1
        # Conditions for fall detection contour Area
        if j > 20:
            cv2.putText(frame, 'FALL', (x+5, y-5), cv2.FONT_HERSHEY_TRIPLEX, 2, (79,244,255), 2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            # Twilio Account Service ID 
            account_sid='AC4985513a8079f9e1553c819b227072ef'
            # Twilio Account Auth Token
            auth_token='6325538f934b62da6af68bb2cea59a10'
            # Initialise the client 
            client=Client(account_sid,auth_token)
            # Creation of Message API
            message=client.messages.create(
            to='+91 7989254635', # Fillthe contact to your desired one
            from_='+12673607175', # Fill with your created Twilio number
            body="Your Kid has fallen Down" # Alert SMS Text   
            )
            #time.sleep(1000)
        if h > w:
            j = 0 
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow('video', frame)
        if cv2.waitKey(33) == 27:
            break
cv2.destroyAllWindows()