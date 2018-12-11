#!/usr/bin/python

import os, sys
# from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
# from tkinter import filedialog
import cv2
import numpy as np

# import matplotlib.pyplot as plt
# from matplotlib import cm
# from mpl_toolkits.mplot3d import Axes3D

MAX_AB = lambda A, B : A if A > B else B
MIN_AB = lambda A, B : A if A < B else B

def interpolateXY(P0, P1, fraction):
    ''' To interpolate coordinate of a point which is on the line from  P0 to P1 
        fraction is counted from P0
    '''

    ''' 
    XX=abs(x0-x1), YY=abs(y0-y1), X= int(fraction * XX), Y= int(fraction * YY)
    '''
    X = int(fraction * abs(P0[0]-P1[0]))
    Y = int(fraction * abs(P0[1]-P1[1]))
    
    if P0[0] >= P1[0]:
        x = MAX_AB(P1[0], P0[0] - X)
    else:
        x = MIN_AB(P1[0], P0[0] + X)

    if P0[1] >= P1[1]:
        y = MAX_AB(P1[1], P0[1] - Y)
    else:
        y = MIN_AB(P1[1], P0[1] + Y)

    return (x, y)


class roiRect():
    def __init__(self, winName, matImg, **kwargs):
        ''' '''
        self._property = {
            'enabled'       : True,
            'lwidth'        : 1,
            'lcolor'        : (0, 255, 0),
        }
        self.gWinName = winName
        self.gMatImg = matImg
        self.Xc, self.Yc, self.W, self.H = (1, 1, 2, 2)
        self.Vertex0 = (0, 0)
        self.Vertex1 = (2, 2)
        self.is_dirty = True
        #cv2.imshow(self.gWinName, self.gMatImg)
        for argKey, argVal in kwargs.items():
            #print("ImageROI: argKey= ", argKey, " argVal= ", argVal)
            if argKey == 'Xc':
                '''coordinate X of ROI center '''
                self.Xc = argVal
            elif argKey == 'Yc':
                '''coordinate Y of ROI center '''
                self.Yc = argVal
            elif argKey == 'W':
                '''size W'''
                self.W = argVal
            elif argKey == 'H':
                '''size H'''
                self.H = argVal
            else:
                pass
                

    def set_center(self, x, y):
        ''' Set coordinate (x, y) of the ROI center'''
        self.Xc = x
        self.Yc = y
        self.is_dirty = True
        

    def set_size(self, w, h):
        ''' Set size (w, h) of the ROI'''
        self.W = w
        self.H = h
        self.is_dirty = True


    def set_property(self, **kwargs):
        ''' Set properities :
                enabled:    True/False -- show or no show
                lwidth:     width of rectangle line
                lcolor:     the color to draw rectangle (R, G, B)
        '''
        self.is_dirty = True
        for argkey, argval in kwargs.items():
            if argkey == 'enabled':
                self._property['enabled'] = argval   # True or False
            elif argkey == 'lwidth':
                self._property['lwidth'] = argval   # line width
            elif argkey == 'lcolor':
                self._property['lcolor'] = argval   # line color
            else:
                pass


    def get_property(self, protKey):
        '''To query property with following key:
                'enabled', 'lwidth', 'lcolor'
        '''
        return self._property[protKey]


    def update(self):
        ''' To re-calculate the ROI Vertex0 and Vertex1 

            Return: (Vertex0, Vertex1) 
                where Vertex0, Vertex1 is coordinates of top-left, and bottom-right
        '''
        halfW = int(self.W/2)
        halfH = int(self.H/2)
        p0 = (MAX_AB(0, self.Xc-halfW), MAX_AB(0, self.Yc-halfH))
        p1 = (MIN_AB(self.gMatImg.shape[1], self.Xc+halfW), MIN_AB(self.gMatImg.shape[0], self.Yc+halfH))
        self.Vertex0 = p0
        self.Vertex1 = p1
        self.is_dirty = False
        return (p0, p1)


    def draw(self):
        ''' To draw the ROI rectangle onto the image'''
        if self.is_dirty:
            self.update()

        if self._property['enabled'] == True:
            color = self._property['lcolor']
            lwidth = self._property['lwidth']
            cv2.rectangle(self.gMatImg, self.Vertex0, self.Vertex1, color, lwidth)
            ## cv2.imshow(self.gWinName, self.gMatImg)


    def show(self):
        ''' To display the image with ROIs imprinted '''
        self.draw()
        cv2.imshow(self.gWinName, self.gMatImg)


class ImageROI():
    '''
    class to organize multiple ROIs of an image.
        Create instant: ImageROI(winName, matImg) where
            winName is the name of a CV2 namedWindow
            matImg is the CV2 matrix of the target image
    '''
    def __init__(self, winName, matImg):
        self.ROIs = {}  # -- use Dictionary key="roiName", val=roiRect
        self.winName = winName
        self.matImg = matImg

    def add(self, name, roi):
        self.ROIs.set(name, roi)
        pass

###########################################################
# MainEntry 
###########################################################


def main():
    winName='imageROI'
    winPosX, winPosY = 150, 100
    #matImg = cv2.imread('Building.jpeg', cv2.IMREAD_UNCHANGED)
    matImg = cv2.imread('church.jpg', cv2.IMREAD_UNCHANGED)
    # print(matImg.shape)
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.moveWindow(winName, winPosX, winPosY)
    #cv2.imshow(winName, matImg)

    imgH = matImg.shape[0]
    imgW = matImg.shape[1]
    imgCenterX = int(imgW / 2)
    imgCenterY = int(imgH / 2)
    print('image WxH = ', imgW, '*', imgH)

    roiW = int(imgW/10)
    roiH = int(imgH/10)
    #--------------------------
    # -- Center ROI
    #--------------------------
    #roiC=roiRect(winName, matImg.copy(), X=10, Y=20, W=100, H=50)
    mat2draw = matImg.copy()
    roiC=roiRect(winName, mat2draw)
    roiC.set_center(imgCenterX, imgCenterY)
    roiC.set_size(roiW, roiH)
    roiC.set_property(lcolor=(0, 0, 255))
    # roiC.set_property(enabled=False)
    roiC.show()

    #--------------------------
    # -- Diagonal: Qudrant Q1, Q2, Q3, Q4
    #--------------------------

    fraction = 0.65
    # -- Q1
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q1: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    roiQ1 = roiRect(winName, mat2draw, Xc=x, Yc=y, W=roiW, H=roiH)
    roiQ1.show()

    # -- Q2
    Po = (imgCenterX, imgCenterY)
    Pv = (0, 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q2: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    roiQ2 = roiRect(winName, mat2draw, Xc=x, Yc=y, W=roiW, H=roiH)
    roiQ2.show()

    # -- Q3
    Po = (imgCenterX, imgCenterY)
    Pv = (0, imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q3: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    roiQ3 = roiRect(winName, mat2draw, Xc=x, Yc=y, W=roiW, H=roiH)
    roiQ3.show()

    # -- Q4
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q4: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    roiQ4 = roiRect(winName, mat2draw, Xc=x, Yc=y, W=roiW, H=roiH)
    roiQ4.show()


    fraction = 0.85
    #--------------------------
    # -- Latitude(Horizontal): Hr (right), Hl (left)
    #--------------------------
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, int(imgH/2))
    x, y = interpolateXY(Po, Pv, fraction)
    print("Hr: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    roiHr = roiRect(winName, mat2draw, Xc=x, Yc=y, W=roiW, H=roiH)
    roiHr.set_property(lcolor=(255,0, 255))
    roiHr.show()

    Po = (imgCenterX, imgCenterY)
    Pv = (0, int(imgH/2))
    x, y = interpolateXY(Po, Pv, fraction)
    print("Hl: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    roiHl = roiRect(winName, mat2draw, Xc=x, Yc=y, W=roiW, H=roiH)
    roiHl.set_property(lcolor=(255,0, 255))
    roiHl.show()

    #--------------------------
    # -- Longitude(Vertical): Vt (top), Vb (bottom)
    #--------------------------
    Po = (imgCenterX, imgCenterY)
    Pv = (int(imgW/2), 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Vt: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    roiVt = roiRect(winName, mat2draw, Xc=x, Yc=y, W=roiW, H=roiH)
    roiVt.set_property(lcolor=(100, 255, 255))
    roiVt.show()

    Po = (imgCenterX, imgCenterY)
    Pv = (int(imgW/2), imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Hl: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    roiHl = roiRect(winName, mat2draw, Xc=x, Yc=y, W=roiW, H=roiH)
    roiHl.set_property(lcolor=(100, 255, 255))
    roiHl.show()



    if False:
        # -- Just for Debug
        cv2.namedWindow('Original')
        cv2.imshow('Original', mat2draw)
    


    cv2.waitKey(0)



if __name__ == "__main__":
    main()