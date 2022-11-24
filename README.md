# Pingpong trajectory analysis

Codes provided in this repository are built to extract the trajectory of a pingpong ball from the recorded video. The main idea of the codes are as follows :

1)  Variance of pixels throughout the motion: RGB values of background pixels would remain the same unless the pingpong ball coincides the pixel at a moment. Therefore, By thresholding the variance of pixels along the time interval, the trajectory of a pingpong ball can be extracted.

2)  Color information of the pingpong ball: For an experiment, orange pingpong ball is used. Hence, using the RGB information of the orange color, among the pixels obtained from 1), the exact area that the pingpong ball is located at a specific time can be obtained by the inner product between RGB values.

## Part 1.

![Figure 1. Initial / final frame of interest in the original video](Figures/1_WindowSettingManual.png)

## ![Figure 2. The visualization of the variance in pixels along the time (gray)](Figures/2_VarianceOfPixels.png){width="300"}

![Figure 3. The variance of pixels after thresholding![Figure 4. The location of the pingpong ball at a specific frame](Figures/4_LocationOfBall_inPath.png){width="300"}![Figure 5. Original image at the selected frame](Figures/4_LocationOfBall_OriginalImage.png){width="300"}![Figure 6. Extracted contours](Figures/5_ContourBall.png){width="300"}](Figures/3_Thresholding.png){width="295"}
