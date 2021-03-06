#!/usr/bin/env python

import numpy as np
import cv2

#--------------------------------------
# Class: CvOSD
#--------------------------------------
class osdText():
    """Define a class to simplify putting osd text on an image with cv2.

    Usage:
    -------------
    1. Import cy_CvOSD as OSD
    1. osd = osdText()
    1. osd.show(cv_img, text, X, Y)
        * where X, Y is the coordinate of top-left point of the text
    * Use set_property() to modify font, such as font face, color, scale, and thickness
    * Use get_textSize() to calculate the width, height, margine of the string
    * To calculate the coordinate of the "next line" :
        1. call get_textSize("this string") to get width, height, pads
        1. the starting (Xn,Yn) of "next line":
            Xn= Xc, Yn= Yc+(h+pads*2)
        1. the starting (Xn, Yn) of "next string":
            Xn= Xc+(w+pads*2), Yn= Yc
    """
    def __init__(self, fface=cv2.FONT_HERSHEY_SIMPLEX, fcolor=(255, 255, 255), fscale=1, fthick=2):
        """
        """
        self.fontFace       = fface
        self.fontScale      = fscale
        self.fontColor      = fcolor
        self.fontThickness  = fthick

    def set_property(self, **kwargs):
        """
        """
        for kw, val in kwargs.items():
            if kw == 'fontColor':
                self.fontColor = val
            elif kw == 'fontScale':
                self.fontScale = val
            elif kw == 'fontFace':
                self.fontFace = val
            elif kw == 'fontThickness':
                self.fontThickness = val
            else:
                pass

    def get_textSize(self, text):
        """To calcualte the text(string) width, height, and margin
        """
        #-- get size of text
        ((tw, th),tpad) = cv2.getTextSize(  text,
                                            fontFace=self.fontFace,
                                            fontScale=self.fontScale,
                                            thickness=self.fontThickness)
        return tw, th, tpad

    def show(self, cv_img, text, X=0, Y=0):
        """To show text on given image
        """
        w, h, pads = self.get_textSize(text)
        x = X + pads
        y = Y + h + pads*2
        cv2.putText( cv_img, text, (x, y),
                        self.fontFace, self.fontScale,
                        self.fontColor, self.fontThickness, 255)

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
