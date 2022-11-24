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
import pandas as pd

fname = 'IMG_3384'
vidname = 'videos/'+ fname +'.MOV'
cap = cv2.VideoCapture(vidname)
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

frame_start = 845
frame_end = 927
fps = 240
################################################
#%% 3. Assign the window in interest manually ###
#################################################
cap = cv2.VideoCapture(vidname)
frames_border = []
for i in [frame_start, frame_end]:
    cap.set(1, i)
    ret, fr = cap.read()
    frames_border.append(fr)
plt.close();plt.figure()
plt.subplot(211);plt.imshow(frames_border[0])
plt.subplot(212);plt.imshow(frames_border[1])
#%% 
xmin, xmax = 600, 1400
ymin, ymax = 0,750
cap = cv2.VideoCapture(vidname)
frames = []
for i in range(frame_start, frame_end):
    cap.set(1, i)
    ret, fr = cap.read()
    frames.append(fr[ymin:ymax, xmin:xmax])
#%% variance filter
frames_array = np.asarray(frames)
check = np.std(frames_array, axis = 0)
check_int = check.astype('uint8')
plt.imshow(check_int)
ball_img = check_int[:,:,:]
ball_gray = LA.norm(ball_img, axis = 2)
ball_gray = ball_gray*255/np.max(ball_gray)
ball_gray = ball_gray.astype('uint8')
#%% thresholding
thres = 45
index = np.where(ball_gray>=thres)
check_path = np.zeros(ball_gray.shape)
for  i in range(index[0].shape[0]):
    check_path[index[0][i], index[1][i]] = 255
plt.close();plt.figure()
plt.imshow(check_path, cmap = 'gray')
#%% final process
bgr_orange = [0, 127, 255]
x_record = []
y_record = []
aa = 1
for frame_test in frames:
    ball_detect = np.zeros(shape = frame_test.shape[0:2])
    for i in range(len(index[0])):
        xx = index[0][i]; yy = index[1][i]
        ball_detect[xx, yy] = np.dot(frame_test[xx, yy,:],bgr_orange) / np.max([LA.norm(frame_test[xx, yy, :]), 1])
    ball_detect = ball_detect * 255 / np.max(ball_detect)
    thres2 = 225
    index2 = np.where(ball_detect>=thres2)
    ball_thres = np.zeros(shape = ball_detect.shape)
    for  i in range(index2[0].shape[0]):
        ball_thres[index2[0][i], index2[1][i]] = 255
    ball_thres = ball_thres.astype('uint8')
    #cv2.imshow('ball_trajectory', ball_thres)
    #cv2.waitKey(0)
    contours, _ = cv2.findContours(
        ball_thres, 
        mode=cv2.RETR_LIST, 
        method=cv2.CHAIN_APPROX_SIMPLE
    )
    frame_with_ctr = frame_test.copy()
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
    cv2.waitKey(0)
    MIN_WIDTH, MIN_HEIGHT = 18, 18
    MAX_WIDTH, MAX_HEIGHT = 60, 60
    MIN_RATIO, MAX_RATIO = 0.5, 2
    possible_contours = []
    cnt = 0
    for d in contours_dict:
        area = d['w'] * d['h']
        ratio = d['w'] / d['h']
        
        if d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
        and d['w'] < MAX_WIDTH and d['h'] < MAX_HEIGHT \
        and MIN_RATIO < ratio < MAX_RATIO:
            d['idx'] = cnt
            cnt += 1
            possible_contours.append(d)
    if cnt >= 2 or cnt ==0:
        if cnt>=2: 
            print('multiple contour selected')
        else:
            print('no contour selected')
        x_fin = 0;y_fin = 0
    else:
        x_fin = possible_contours[0]['cx']
        y_fin = possible_contours[0]['cy']
    x_record.append(x_fin)
    y_record.append(y_fin)
    aa += 1
    if aa%10 == 0:
        print(aa)
#%%
plt.scatter(x_record, y_record)
df = pd.DataFrame(list(zip(x_record, y_record)),
               columns =['x', 'y'])
csvname = 'trajectory/'+fname+'.csv'
df.to_csv(csvname, index=False)
#%%
plt.imshow('aa',frames[2])