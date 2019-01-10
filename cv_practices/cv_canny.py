#!/usr/bin/env python
# encoding: utf-8
import numpy as np
import cv2
import argparse

Set_Global = lambda arg, default: arg if arg else default

#----------------------
# Argument Parse
#----------------------
#argParser = argparse.ArgumentParser(usage="An example to demonstrate edge detection using GaussianBlur and Canny algorithms.")
argParser = argparse.ArgumentParser()
argParser.add_argument("srcImg", help="source image")
argParser.add_argument("--ksize", help="the kernel size of Gaussian blur")
argParser.add_argument("--lt", type=int, help="the low threshold of Canny detection")
argParser.add_argument("--ht", type=int, help="the high threshold of Canny detection")
args = argParser.parse_args()

gSrcImg = args.srcImg
kernelSize = int(Set_Global(args.ksize, 3))
lowThd = int(Set_Global(args.lt, 60))
highThd = int(Set_Global(args.ht, 150))


#----------------------
# Argument Parse
#----------------------

#-- read image and convert to gray image
srcImg = cv2.imread("sample.jpg")
grayImg = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)

#-- Gaussian blur
#kernelSize = 3
gaussianImg = cv2.GaussianBlur(grayImg, (kernelSize, kernelSize), 0)
blurImg = cv2.blur(grayImg, (kernelSize, kernelSize) )
medianImg = cv2.medianBlur(grayImg, kernelSize )
bilateralImg = cv2.bilateralFilter(grayImg, kernelSize, 31, 31)

#-- Canny edge detection
#lowThd, highThd = 60, 150
edgeImg = cv2.Canny(gaussianImg, lowThd, highThd)

#windowTitle = "Source"
#cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
#cv2.imshow(windowTitle, srcImg)

windowTitle = "cvt2Gray"
cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
cv2.imshow(windowTitle, grayImg)

windowTitle = "Gaussian Blur"
cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
cv2.imshow(windowTitle, gaussianImg)

if False:
    windowTitle = "Average Blur"
    cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(windowTitle, blurImg)

    windowTitle = "Median Blur"
    cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(windowTitle, medianImg)

windowTitle = "Bilateral Filter"
cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
cv2.imshow(windowTitle, bilateralImg)



windowTitle = "Canny Edge"
cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
cv2.imshow(windowTitle, edgeImg)

while True:
    if 27 == cv2.waitKey(100):
        cv2.destroyAllWindows()
        break
