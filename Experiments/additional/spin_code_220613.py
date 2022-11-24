# -*- coding: utf-8 -*-
"""
Created on 220613

@author: JaeHoanKim
"""
#%% import video
## from the video, press 'q' at the starting point of measurement of the angular speed
import cv2
import numpy as np
import matplotlib.pyplot as plt
filename = 'videos/IMG_3379.MOV' # file name
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
#%%
frame_start = cnt
fps = 240
#%%
cap = cv2.VideoCapture(filename)
frames = []
for i in range(frame_start, frame_start+20):
    cap.set(1, i)
    ret, fr = cap.read()
    frames.append(fr)
#%%
plt.close();plt.figure()
plt.subplot(211);plt.imshow(frames[0])
plt.subplot(212);plt.imshow(frames[-1])
#%% area range of ball spin
x_min, x_max = 500, 750
y_min, y_max = 50, 120
#%%
plt.close()
w_new, h_new = x_max-x_min, y_max-y_min
for frame in frames:
    frame_ball = frame[y_min:y_max, x_min:x_max, :]
    frame_ball_big = cv2.resize(frame_ball, (3*w_new, 3*h_new))
    cv2.imshow('target', frame_ball_big)
    cv2.waitKey(0)
#%%
rot_round = 3/4
frame_gap = 8
#%%
ang_per_frame = rot_round/frame_gap * fps * 2*np.pi