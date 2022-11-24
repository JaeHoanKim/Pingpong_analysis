# Ping-pong ball trajectory analysis

## Introduction

Codes provided in this repository are initially built to extract the trajectory of a ping-pong ball from the recorded video. The main idea is as follows :

1)  **Variance of pixels throughout the motion**: RGB values of background pixels would remain the same unless the ping-pong ball coincides the pixel at a moment. Therefore, By thresholding the variance of pixels along the time interval, the trajectory of a ping-pong ball can be extracted.

2)  **Color information of the ping-pong ball**: For an experiment, orange ping-pong ball is used. Hence, using the RGB information of the orange color, among the pixels obtained from 1), the exact area the ball is located at a specific time can be obtained by the inner product between RGB values.

## Results

In *image_process.py*, the illustration of each code blocks were provided. The following is the figures generated along the code.

<center>

![](Figures/1_WindowSettingManual.png) 

*Figure 1. Initial / final frame of interest in the original video*

![](Figures/2_VarOfPixels.png) 

*Figure 2. The visualization of the variance in pixels along the time (gray image)*

![](Figures/3_BallLocation.png) 

*Figure 3. The location of the ping-pong ball at a specific frame & original image*

![](Figures/4_ExactBallLocation.png) 

*Figure 4. Extracted contours and selected the contour of the ball*

</center>

## Notes

Along the code, there are several features which require manual settings.

-   Start / end frame of the video: In the first block of the code, one should manually put the index of the start frame and end frame. This work requires you to play the video twice to obtain the inital / final frame. By default, press 'q' and check 'cnt' value, which denotes the frame number.

-   Window of interest: To enhance the computation speed, it is recommended to choose the rectangular window of interest. For this, minimum / maximum values of x, y coordinate should be provided. It can be easily processed by checking the popped up image after running the third code block.

-   Threshold values (optional) : Depending on the video and purpose, threshold values should be adjusted. Usually, for the fixed experiment situation (fixed background, fixed objects), one or two adjustments would be sufficient.

- Before processing, don't forget to check whether the working directory is set properly.
