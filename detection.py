"""
This script will use opencv mainly and other libraries to detect the position of players' face to generate direction command 
as outputs to 2048 game. The game will analyze the command output and give response(check the file: face_detection_2048_sub.py)
"""
#-------------------------------------------------------------------------------------------------
import cv2
import pygame
import os
import numpy as np
import time
import operator
from math import*
import random
# import face_detection_2048_sub# importing 2048 game algorithm for outputing the direction command
from GUI import*

#-------------------------------------------------------------------------------------------------

iteration=1   #number of the detection iteration
cap = cv2.VideoCapture(0) 
command_collector={} #dictionary for collecting commands in case of command conflicts to avoid unwanted command output
half_width=cap.get(3)/2 #half width of the camera scope 
half_height=cap.get(4)/2 #half height of the camera scope 
face_cascade = cv2.CascadeClassifier('/home/zhecan/Downloads/opencv-2.4.10/data/haarcascades/haarcascade_frontalface_alt.xml')
#import the face detection algorithm from local computer

while(1):
    __, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(400,400))
    try:
        for (x,y,w,h) in faces:
            cx=x+w/2
            cy=y+h/2  # find the center point coordination of the face

            command=' '
            x_range=abs(cx-half_width)
            y_range=abs(cy-half_height)# find the distance between the center of the face and the center of the camera scope
            distance=80# the ditance offset triger value, the critical, minimun distance the face has to be away from the center of the scope to give the direction command

            if x_range>distance or y_range>distance: #conditional for differentiating either the horizontal or the vertical move of the face
                if x_range>y_range:
                    if half_width-cx>distance: # four directions outputs
                        command='d'
                    else:
                        command='a'
                else:
                    if cy-half_height>distance:
                        command='s'
                    else:
                        command="w"
            else:
                pass

            if command in command_collector.keys():
                command_collector[command]+=1
            else:
                command_collector[command]=1   # in case of accidentally giving too many commands at one time. the dictionary will
                                                      # filter out and finds the most frequently command output         

            if command==' ': #if the command becomes blank again then that means the face comes back into the square 
                command=max(command_collector.iteritems(), key=operator.itemgetter(1))[0] #finds the most frequent command
                command_collector={}
                if command!=' ':
                    # if iteration!=1:  # skip the first trigger direction since that is used for starting the game
                    if command=="w":# making sound effects depending on the direction output
                        pygame.mixer.init()
                        pygame.mixer.music.load("horse.wav")
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy() == True:
                            continue
                    if command=="s":
                        pygame.mixer.init()
                        pygame.mixer.music.load("cow.wav")
                        pygame.mixer.music.play()
                    if command=="a":
                        pygame.mixer.init()
                        pygame.mixer.music.load("yahoo.wav")
                        pygame.mixer.music.play()
                    if command=="d":
                        pygame.mixer.init()
                        pygame.mixer.music.load("getoffcomputer.wav")
                        pygame.mixer.music.play()
                    game_2048_text_version(command)
                    # time.sleep(0.01) # rest after outputing in case of mistakely detecting the move offset
                    iteration+=1
            else:
                pass
            cv2.circle(frame, (cx,cy), 10, (0,255,0),10,-1) # drawing circle to display the center of face
             # display a square to show the unsensitive, non-detective area.
            cv2.rectangle(frame, (int(half_width-distance),int(half_height-distance)), (int(half_width+distance),int(half_height+distance)), (0,0,255),10)
            cv2.imshow("2048 game detection",frame)

        k = cv2.waitKey(5) & 0xFF# pressing escape key will exit the game
        if k == 27:
                break
           
    except:
        pass
cap.release()

cv2.destroyAllWindows()

