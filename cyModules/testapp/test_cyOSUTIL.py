#!/usr/bin/env python

import numpy as np
import cv2

import Add_cyModules as addCY

from cy_CvOSD import osdText

#---------------------------------------------------------------
# Module Test
#---------------------------------------------------------------

def main():
    cv_img = cv2.imread("./church.jpg")
    cv_win = "Test Image"
    cv2.namedWindow(cv_win, cv2.WINDOW_AUTOSIZE)

    osd = osdText() #-- use default font setting
    text = "Esc to exit !!"

    osd.set_property(fontScale=1, fontThickness=1, fontColor=(0, 0, 255))
    osd.show(cv_img, text, 10, 10)

    cv2.imshow(cv_win, cv_img)
    cv2.waitKey(0)



if __name__ == "__main__":
    main()
