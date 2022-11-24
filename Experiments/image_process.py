# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:08:26 2022

@author: JaeHoanKim
"""

##########################
#%% 1. Importing video ###
##########################

import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
filename = 'videos/IMG_3417.MOV'
cap = cv2.VideoCapture(filename)
cnt = 1
while cap.isOpened(): # check whether the video is imported properly
    ret, frame = cap.read() # ret: TRUE until all frames is shown, frame: imported image at certain frame
    cnt = cnt + 1
    if not ret:
        print('No more frame to show.')
        break
    frame_resized = cv2.resize(frame, (frame.shape[1], frame.shape[0]))
    cv2.imshow('vid2', frame_resized)
    if cv2.waitKey(1) == ord('q'): # when the button q is pressed
        break
cv2.destroyAllWindows() # close all the windows

################################################
#%% 2. Assign the frame in interest manually ###
################################################

frame_start = 998 # the frame when the pingpongball starts its own motion
frame_end = 1075 # the frame just before the pingpongball hits the ground
fps = 240 # fps of the recorded video

######################################
#%% 3. Crop the window in interest ###
######################################

cap = cv2.VideoCapture(filename)
frames_border = []
for i in [frame_start, frame_end]:
    cap.set(1, i)
    ret, fr = cap.read()
    frames_border.append(fr)
plt.close();plt.figure()
#plt.imshow(cv2.cvtColor(frame_with_ctr, cv2.COLOR_BGR2RGB))
plt.subplot(211);plt.imshow(cv2.cvtColor(frames_border[0], cv2.COLOR_BGR2RGB))
#plt.imshow(frames_border[0])
plt.subplot(212);plt.imshow(cv2.cvtColor(frames_border[1], cv2.COLOR_BGR2RGB))
###############################
#%% Set the window manually ###
###############################

xmin, xmax = 650, 1150 # left and right end of the pingpong ball
ymin, ymax = 0, 800 # bottom and top end of the pingpong ball

###############################################################
#%% 4.calculate the variance of each pixel among the frames ###
###############################################################
# Intuition: the background is fixed and the motion of the pingpong ball generates the variance of the pixel
# check_int : the matrix with the values of the variance of pixels

cap = cv2.VideoCapture(filename)
frames = []
for i in range(frame_start, frame_end):
    cap.set(1, i)
    ret, fr = cap.read()
    frames.append(fr[ymin:ymax, xmin:xmax]) 
frames_array = np.asarray(frames)
check = np.std(frames_array, axis = 0)
check_int = check.astype('uint8')
plt.imshow(cv2.cvtColor(check_int, cv2.COLOR_BGR2RGB))

#############################
#%% Convert to gray image ###
#############################

ball_img = check_int[:,:,:]
ball_gray = LA.norm(ball_img, axis = 2)
ball_gray = ball_gray*255/np.max(ball_gray)
ball_gray = ball_gray.astype('uint8')
plt.imshow(ball_gray, cmap='gray')

#######################################################
#%% 5. thresholding 1 - to clarify trajectory range ###
#######################################################

thres = 25
index = np.where(ball_gray>=thres)
check_path = np.zeros(ball_gray.shape)
for  i in range(index[0].shape[0]):
    check_path[index[0][i], index[1][i]] = 255
plt.imshow(check_path, cmap = 'gray')

############################################################################
#%% 6. thresholding 2 - to extract ball location using color information ###
############################################################################

bgr_orange = [0, 127, 255]
frame_test = frames[55]
ball_detect = np.zeros(shape = frame_test.shape[0:2])
for i in range(len(index[0])):
    xx = index[0][i]; yy = index[1][i]
    ball_detect[xx, yy] = np.dot(frame_test[xx, yy,:],bgr_orange) / np.max([LA.norm(frame_test[xx, yy, :]), 1])
ball_detect = ball_detect * 255 / np.max(ball_detect)

thres2 = 220
index2 = np.where(ball_detect>=thres2)
ball_thres = np.zeros(shape = ball_detect.shape)
for  i in range(index2[0].shape[0]):
    ball_thres[index2[0][i], index2[1][i]] = 255
ball_thres = ball_thres.astype('uint8')
plt.imshow(ball_thres, cmap = 'gray')

####################################################
#%% Compare the loaction with the original image ###
####################################################

plt.imshow(cv2.cvtColor(frame_test, cv2.COLOR_BGR2RGB))

#####################################################################
#%% 7. find contour and extract the exact center of pingpong ball ###
#####################################################################

contours, _ = cv2.findContours(
    ball_thres, 
    mode=cv2.RETR_LIST, 
    method=cv2.CHAIN_APPROX_SIMPLE
)
frame_with_ctr = frame_test.copy()
cv2.drawContours(frame_with_ctr, contours=contours, contourIdx=-1, color=(255, 0, 255), thickness = 5)

plt.imshow(cv2.cvtColor(frame_with_ctr, cv2.COLOR_BGR2RGB))
# cv2.imshow('img', frame_with_ctr)
cv2.waitKey(0)

########################################################
#%% Making rectangular contour on the previous image ###
########################################################
contours_dict = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(frame_with_ctr, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=2)
    # insert to dict
    contours_dict.append({
        'contour': contour,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'cx': x + (w / 2),
        'cy': y + (h / 2)
    })
plt.imshow(cv2.cvtColor(frame_with_ctr, cv2.COLOR_BGR2RGB))
cv2.waitKey(0)

########################################################################################
#%% Extracting the center of the pingpong ball using the restriction on the contours ###
########################################################################################

MIN_WIDTH, MIN_HEIGHT = 20, 20
MAX_WIDTH, MAX_HEIGHT = 60, 60
MIN_RATIO, MAX_RATIO = 0.7, 1.3
possible_contours = []
cnt = 0
for d in contours_dict:
    area = d['w'] * d['h']
    ratio = d['w'] / d['h']
    
    # selecting the contour using contour size and width height ratio
    if d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
    and d['w'] < MAX_WIDTH and d['h'] < MAX_HEIGHT \
    and MIN_RATIO < ratio < MAX_RATIO:
        d['idx'] = cnt
        cnt += 1
        possible_contours.append(d)
if cnt >= 2 or cnt ==0:
    print('multiple or no contour selected')
    
######################################################################################################
#%% 7. If multiple contours are selected, choose the exact contour manually (usually not required) ###
######################################################################################################

cv2.drawContours(frame_test, contours = possible_contours[0]['contour'], contourIdx=-1, color=(255, 0, 255), thickness = 5)
plt.imshow(cv2.cvtColor(frame_test, cv2.COLOR_BGR2RGB))
#%%
x_fin = possible_contours[0]['cx']
y_fin = possible_contours[0]['cy']
print(x_fin)
print(y_fin)

