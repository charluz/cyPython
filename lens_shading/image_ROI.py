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
        ''' imgW: the image width, for boundary handling,
        imgH: the imgage height, for boundary handling
        '''
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
    """A class to define a list of ROI rectangles of an image.

    The list is implemented as a dictionary, e.g., { "Q1":roiRect, "C0":roiRect, ... }
    The key of the element is a string to identify the ROI rectangle,
    and the value of the element is an object of roiRect class.

    ...
    Attributes
    -----------
    ROIs: {}
        a dictionary to manage a list of ROI rectangle.
    imgW, imgH: int
        the image size which is for boundary handling

    Methods
    -----------
    add(name:str, center:(x,y), size(w,h))
        create and add a rectangle to ROIs list
        if the named rectangle exists, update the center and size as specified
    delete(name:str)
        remove a designated roiRect from the list
    get_vertex(name:str) -> (Vt, Vb)
        get vertexes (Vt: TopLeft, Vb:BottomRight) of the rectangle
    get_vertex_all() --> a list of [ [name:str, Vt:(x,y), Vb:(x,y) ], ...[] ]
        get vertexes of all rectangles
    """
    def __init__(self, imgW, imgH):    # -- winName, matImg):
        '''
        '''
        self.ROIs = {}  # -- use Dictionary key="roiName", val=roiRect
        self.imgW = imgW
        self.imgH = imgH
        #self.matImg = matImg.copy()


    def add(self, name, center, size):
        """add a new rectangle to ROI list

        Arguments
        -------------
        name: str
            the string ID to identify this rectangle
        center:(x,y)
            the center coordinate of the rectangle
        size:(w,h)
            the size of the rectangle

        Returns
        -------------
        list
            a list of the format: [name:str, Vt:(x,y), Vb:(x,y))], e.g., ["Q1", (10, 10), (30,30)]
        """
        if name not in self.ROIs:
            rect = roiRect(self.imgW, self.imgH, Xc=center[0], Yc=center[1], W=size[0], H=size[1])
            self.ROIs.setdefault(name, rect)
        else:
            rect = self.ROIs[name]
            rect.set_center(center[0], enter[1])
            rect.set_size(size[0], size[1])

        rect.update()
        return [ name, rect.Vertex0, rect.Vertex1 ]

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

    def draw(self, nameID, cv_img):
        ''' To draw the specified ROI rectangle on the image'''
        # self.matImg = self.matOrigin.copy()
        if nameID in self.ROIs:
            self.ROIs[nameID].draw(cv_img)

    def draw_all(self, cv_img):
        """Draw all ROI rectangle on the image

        Arguements
        -----------
        cv_img: cv image
            the target image

        Returns
        -----------
        None
        """
        for k in self.ROIs:
            self.ROIs[k].draw(cv_img)

    def show(self, cv_window, cv_img):
        ''' To display the image with ROIs imprinted '''
        #self.matImg = self.matOrigin.copy()
        # for k in self.ROIs:
        #     self.ROIs[k].show(self.winName, self.matImg)
        self.draw_all(cv_img) #-- have all rectabgle to be drawn on self.matImg
        cv2.imshow(cv_window, cv_img)

    def get_vertex_all(self):
        """get vertex of all rectangles

        Arguments
        -------------
        None

        Returns
        -------------
        list
            a list of the list [name:str, Vt:(x,y), Vb:(x,y))], e.g., [ ["Q1", (10, 10), (30,30)], [], ..., [] ]
        """
        allp = []
        for k in self.ROIs:
            p = [ k ]
            p.append(self.ROIs[k].Vertex0)
            p.append(self.ROIs[k].Vertex1)
            #print(p)
            allp.append(p)
        return allp

    def get_vertex(self, name):
        """get vertex of the rectangle of the ID name:str

        Arguments
        -------------
        name: str
            the ID (key) to query the vertexes of the rectangle

        Returns
        -------------
        list
            a list of the format: [name:str, Vt:(x,y), Vb:(x,y))], e.g., ["Q1", (10, 10), (30,30)]
        """
        if name in self.ROIs:
            p = [name]
            p.append(self.ROIs[name].Vertex0)
            p.append(self.ROIs[name].Vertex1)
            #print(p)
        return p


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
    shadingRects = ImageROI(mat2draw.shape[1], mat2draw.shape[0])

    #--------------------------
    # -- Center ROI
    #--------------------------
    shadingRects.add('C0', (imgCenterX, imgCenterY), (roiW, roiH))

    #--------------------------
    # -- Diagonal: Qudrant Q1, Q2, Q3, Q4
    #--------------------------

    fraction = 0.65
    # -- Q1
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q1: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    shadingRects.add('Q1', (x, y), (roiW, roiH))

    # -- Q2
    Po = (imgCenterX, imgCenterY)
    Pv = (0, 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q2: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    shadingRects.add('Q2', (x, y), (roiW, roiH))

    # -- Q3
    Po = (imgCenterX, imgCenterY)
    Pv = (0, imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q3: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    shadingRects.add('Q3', (x, y), (roiW, roiH))

    # -- Q4
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Q4: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    shadingRects.add('Q4', (x, y), (roiW, roiH))


    fraction = 0.85
    #--------------------------
    # -- Latitude(Horizontal): Hr (right), Hl (left)
    #--------------------------
    Po = (imgCenterX, imgCenterY)
    Pv = (imgW, int(imgH/2))
    x, y = interpolateXY(Po, Pv, fraction)
    print("Hr: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    shadingRects.add('Hr', (x, y), (roiW, roiH))

    Po = (imgCenterX, imgCenterY)
    Pv = (0, int(imgH/2))
    x, y = interpolateXY(Po, Pv, fraction)
    print("Hl: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    shadingRects.add('Hl', (x, y), (roiW, roiH))

    #--------------------------
    # -- Longitude(Vertical): Vt (top), Vb (bottom)
    #--------------------------
    Po = (imgCenterX, imgCenterY)
    Pv = (int(imgW/2), 0)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Vt: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    shadingRects.add('Vt', (x, y), (roiW, roiH))

    Po = (imgCenterX, imgCenterY)
    Pv = (int(imgW/2), imgH)
    x, y = interpolateXY(Po, Pv, fraction)
    print("Vb: P0= ", Po, " P1= ", Pv, " P= ", (x, y))
    shadingRects.add('Vb', (x, y), (roiW, roiH))


    shadingRects.show(winName, mat2draw)

    if False:
        # -- Just for Debug
        cv2.namedWindow('Original')
        cv2.imshow('Original', mat2draw)

    while not cv2.waitKey(100) == 27:
        pass



if __name__ == "__main__":
    main()
