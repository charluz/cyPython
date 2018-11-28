#!/usr/bin/python

import os, sys
from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import cv2
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# def show_bayer_shading3D(imgR, imgG, imgB):
def show_bayer_shading3D(imgR):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  # ax = Axes3D(fig)
    #print("shape of imgR: ", imgR.shape)
    # print(imgR.shape[0], imgR.shape[1])
    X = np.arange(0, imgR.shape[1],1)
    Y = np.arange(0, imgR.shape[0],1)
    X, Y = np.meshgrid(X, Y)
    #imgR = imgR / 4; imgR = imgR.astype(np.uint8)
    # print(imgR)
    # print("imgR.dtype ", imgR.dtype)
    # ax.plot_surface(X, Y, imgR, rstride=1, cstride=1, cmap=cm.Reds)
    surf = ax.plot_surface(X, Y, imgR, cmap=cm.Reds_r)
    # ax.plot_surface(X, Y, imgG, rstride=1, cstride=1, cmap='Greens_r')
    # ax.plot_surface(X, Y, imgB, rstride=1, cstride=1, cmap='Blues_r')

    fig.colorbar(surf, shrink=0.5, aspect=10)

    plt.show()

    print("function exit !!")
    return


###########################################################
# MainEntry 
###########################################################
gRawFileName = ""
gRawU16 = np.arange(3)
gRawWidth, gRawHeight = 2304, 1296

if __name__ == "__main__":

    #gRawFileName = filedialog.askopenfilename()
    gRawFileName = "D:/cyMyProjects/myCvPython/lens_shading/test_lsc_2304_1296_10bit-2bytes.raw"
    #print(gRawFileName)
    try:
        gRawU16 = np.fromfile(gRawFileName, dtype=np.uint16)
    except:
        print('Failed to open file :' + gRawFileName)
        exit()
    print(gRawFileName)
    #print("geom: ", gRawHeight, gRawWidth)
    gRawU16 = gRawU16.reshape(gRawHeight, gRawWidth)
    #print("shape: ", gRawU16.shape)

    show_bayer_shading3D(gRawU16)

    print("Main exit !!")

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
