#!/usr/bin/python

import os, sys
from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import cv2
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

'''
def show_bayer_shading3D(w, h, imgR):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #print("shape of imgR: ", imgR.shape)
    # print(imgR.shape[0], imgR.shape[1])
    X = np.arange(0,w,1)
    Y = np.arange(0,h,1)
    X, Y = np.meshgrid(X, Y)
    #imgR = imgR / 4; imgR = imgR.astype(np.uint8)
    # print(imgR)
    # print("imgR.dtype ", imgR.dtype)
    surf = ax.plot_surface(X, Y, imgR, cmap=cm.Reds_r)
    fig.colorbar(surf, shrink=0.5, aspect=10)
    plt.show()

    return
'''


def show_RGB_shading3D(w, h, **kwargs):
    '''
    Show 3D shading chart.

    w, h : the width, height of the input images

    image_R, image_G, image_B are used to specify the R/G/G images
    '''
    useR, useG, useB = False, False, False
    for imageKey, imageValue in kwargs.items():
        #print("key= ", imageKey, "-- value= ", imageValue)
        if imageKey == "image_R":
            #print("---> image_R")
            imgR = imageValue
            useR = True
        elif imageKey == "image_G":
            imgG = imageValue
            useG = True
        elif imageKey == "image_B":
            imgB = imageValue
            useB = True
        else:
            pass

    ## Disable plot toolbar before creation of any figure !!
    #cm.rcParams['toolbar'] = 'None'

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #print("shape of imgR: ", imgR.shape)
    # print(imgR.shape[0], imgR.shape[1])
    X = np.arange(0,w,1)
    Y = np.arange(0,h,1)
    X, Y = np.meshgrid(X, Y)
    #imgR = imgR / 4; imgR = imgR.astype(np.uint8)
    # print(imgR)
    # print("imgR.dtype ", imgR.dtype)
    if useR:
        surf0 = ax.plot_surface(X, Y, imgR, cmap=cm.Reds_r)
        #fig.colorbar(surf0, shrink=0.5, aspect=16)

    if useG:
        surf1 = ax.plot_surface(X, Y, imgG, cmap=cm.Greens_r)
        #fig.colorbar(surf1, shrink=0.5, aspect=16)

    if useB:
        surf2 = ax.plot_surface(X, Y, imgB, cmap=cm.Blues_r)
        #fig.colorbar(surf2, shrink=0.5, aspect=16)

    if useR or useG or useB:
        plt.show()

    return


###########################################################
# MainEntry 
###########################################################
gRawFileName = ""
gRawU16 = np.arange(3)
gRawWidth, gRawHeight = 2304, 1296

if __name__ == "__main__":

    gRawFileName = filedialog.askopenfilename()

    try:
        gRawU16 = np.fromfile(gRawFileName, dtype=np.uint16)
    except:
        print('Failed to open file :' + gRawFileName)
        exit()
    #print(gRawFileName)
    #print("geom: ", gRawHeight, gRawWidth)
    gRawU16 = gRawU16.reshape(gRawHeight, gRawWidth)
    #print("shape: ", gRawU16.shape)

    show_RGB_shading3D(gRawWidth, gRawHeight, image_R=gRawU16, image_G=gRawU16, image_B=gRawU16)



'''
fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

plt.show()

--------------------- 
作者：Eddy_zheng 
来源：CSDN 
原文：https://blog.csdn.net/Eddy_zheng/article/details/48713449 
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
