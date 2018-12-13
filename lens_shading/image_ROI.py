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
    def __init__(self, imgW, imgH, **kwargs):
        ''' '''
        self._property = {
            'enabled'       : True,
            'lwidth'        : 2,
            'lcolor'        : (0, 255, 0),
        }
        # self.gWinName = winName
        # self.gMatImg = matImg
        self.Xc, self.Yc, self.W, self.H = (1, 1, 2, 2)
        self.Vertex0 = (0, 0)
        self.Vertex1 = (2, 2)
        self.is_dirty = True
        self.imgW = imgW
        self.imgH = imgH
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
        p1 = (MIN_AB(self.imgW, self.Xc+halfW), MIN_AB(self.imgH, self.Yc+halfH))
        self.Vertex0 = p0
        self.Vertex1 = p1
        self.is_dirty = False
        return (p0, p1)


    def draw(self, cv_img):
        ''' To draw the ROI rectangle onto the image'''
        if self.is_dirty:
            self.update()

        if self._property['enabled'] == True:
            color = self._property['lcolor']
            lwidth = self._property['lwidth']
            cv2.rectangle(cv_img, self.Vertex0, self.Vertex1, color, lwidth)
            ## cv2.imshow(self.gWinName, self.gMatImg)


    def show(self, cv_window, cv_img):
        ''' To display the image with ROIs imprinted '''
        self.draw(cv_img)
        cv2.imshow(cv_window, cv_img)    #-- (self.gWinName, self.gMatImg)


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
        self.matOrigin = matImg
        self.matImg = matImg.copy()

    def new_rect(self, name):
        '''
        Create a roi object and return to caller.
            name: the string of the cv2 namedWindow

        return: roiRect
        '''
        if name in self.ROIs:
            return self.ROIs[name]
        else:
            imgW, imgH = self.matOrigin.shape[1], self.matOrigin.shape[0]
            new_rect = roiRect(imgW, imgH)  # --(self.winName, self.matImg)
            return new_rect

    def add(self, name, roi):
        self.ROIs.setdefault(name, roi)

    def get(self, name):
        if name in self.ROIs:
            return self.ROIs.get(name)
        else:
            return None
    def delete(self, name):
        self.ROIs.pop(name)

    def set_center(self, name, Xc, Yc):
        ''' Set coordinate (x, y) of the ROI center'''
        if name in self.ROIs:
            roi_rect = self.ROIs[name]
            roi_rect.set_center(Xc, Yc)

    def set_size(self, name, w, h):
        ''' Set size (w, h) of the ROI'''
        if name in self.ROIs:
            roi_rect = self.ROIs[name]
            roi_rect.set_size(w, h)

    def set_property(self, name, **kwargs):
        ''' Set properities :
                enabled:    True/False -- show or no show
                lwidth:     width of rectangle line
                lcolor:     the color to draw rectangle (R, G, B)
        '''
        if name in self.ROIs:
            roi_rect = self.ROIs[name]
            for argkey, argval in kwargs.items():
                if argkey == 'enabled':
                    roi_rect.set_property['enabled'] = argval   # True or False
                elif argkey == 'lwidth':
                    roi_rect.set_property['lwidth'] = argval   # line width
                elif argkey == 'lcolor':
                    roi_rect.set_property['lcolor'] = argval   # line color
                else:
                    pass

    def get_property(self, name, protKey):
        '''To query property with following key:
                'enabled', 'lwidth', 'lcolor'
        '''
        if name in self.ROIs:
            roi_rect = self.ROIs[name]
            return roi_rect.get_property[protKey]
        else:
            return None

    def update(self):
        ''' To re-calculate the ROI Vertex0 and Vertex1

            Return: (Vertex0, Vertex1)
                where Vertex0, Vertex1 is coordinates of top-left, and bottom-right
        '''
        for k in self.ROIs:
            self.ROIs[k].update()

    def draw(self):
        ''' To draw the ROI rectangle onto the image'''
        self.matImg = self.matOrigin.copy()
        for k in self.ROIs:
            self.ROIs[k].draw(self.matImg)

    def show(self):
        ''' To display the image with ROIs imprinted '''
        #self.matImg = self.matOrigin.copy()
        # for k in self.ROIs:
        #     self.ROIs[k].show(self.winName, self.matImg)
        self.draw() #-- have all rectabgle to be drawn on self.matImg
        cv2.imshow(self.winName, self.matImg)

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

    mat2draw = matImg.copy()
    shadingRects = ImageROI(winName, mat2draw)

    #--------------------------
    # -- Center ROI
    #--------------------------
    rect = shadingRects.new_rect('C0')
    rect.set_center(imgCenterX, imgCenterY)
    rect.set_size(roiW, roiH)
    shadingRects.add('C0', rect)
    #shadingRects.update()
    #shadingRects.show()
    #print(shadingRects)

    # #roiC=roiRect(winName, matImg.copy(), X=10, Y=20, W=100, H=50)
    # mat2draw = matImg.copy()
    # roiC=roiRect(winName, mat2draw)
    # roiC.set_center(imgCenterX, imgCenterY)
    # roiC.set_size(roiW, roiH)
    # roiC.set_property(lcolor=(0, 0, 255))
    # # roiC.set_property(enabled=False)
    # roiC.show()

    #--------------------------
    # -- Diagonal: Qudrant Q1, Q2, Q3, Q4
    #--------------------------

    fraction = 0.65
    # -- Q1
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q1: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    rect = shadingRects.new_rect('Q1')
    rect.set_center(x, y)
    rect.set_size(roiW, roiH)
    shadingRects.add('Q1', rect)

    # -- Q2
    Po = (imgCenterX, imgCenterY)
    Pv = (0, 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q2: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    rect = shadingRects.new_rect('Q2')
    rect.set_center(x, y)
    rect.set_size(roiW, roiH)
    shadingRects.add('Q2', rect)

    # -- Q3
    Po = (imgCenterX, imgCenterY)
    Pv = (0, imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q3: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    rect = shadingRects.new_rect('Q3')
    rect.set_center(x, y)
    rect.set_size(roiW, roiH)
    shadingRects.add('Q3', rect)

    # -- Q4
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q4: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    rect = shadingRects.new_rect('Q4')
    rect.set_center(x, y)
    rect.set_size(roiW, roiH)
    shadingRects.add('Q4', rect)


    fraction = 0.85
    #--------------------------
    # -- Latitude(Horizontal): Hr (right), Hl (left)
    #--------------------------
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, int(imgH/2))
    x, y = interpolateXY(Po, Pv, fraction)
    print("Hr: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    rect = shadingRects.new_rect('Hr')
    rect.set_center(x, y)
    rect.set_size(roiW, roiH)
    shadingRects.add('Hr', rect)

    Po = (imgCenterX, imgCenterY)
    Pv = (0, int(imgH/2))
    x, y = interpolateXY(Po, Pv, fraction)
    print("Hl: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    rect = shadingRects.new_rect('Hl')
    rect.set_center(x, y)
    rect.set_size(roiW, roiH)
    shadingRects.add('Hl', rect)

    #--------------------------
    # -- Longitude(Vertical): Vt (top), Vb (bottom)
    #--------------------------
    Po = (imgCenterX, imgCenterY)
    Pv = (int(imgW/2), 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Vt: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    rect = shadingRects.new_rect('Vt')
    rect.set_center(x, y)
    rect.set_size(roiW, roiH)
    shadingRects.add('Vt', rect)

    Po = (imgCenterX, imgCenterY)
    Pv = (int(imgW/2), imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Vb: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    rect = shadingRects.new_rect('Vb')
    rect.set_center(x, y)
    rect.set_size(roiW, roiH)
    shadingRects.add('Vb', rect)


    shadingRects.show()

    if False:
        # -- Just for Debug
        cv2.namedWindow('Original')
        cv2.imshow('Original', mat2draw)

    while not cv2.waitKey(100) == 27:
        pass



if __name__ == "__main__":
    main()
