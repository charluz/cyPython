#!/usr/bin/env python3
# encoding: utf-8

import sys, os
import numpy as np
#import cv2
import argparse
import time



#---------------------------------------------------------------
# __main__
#---------------------------------------------------------------


#----------------------
# Argument Parse
#----------------------
if True:
    #argParser = argparse.ArgumentParser(usage="An example to demonstrate edge detection using GaussianBlur and Canny algorithms.")
    argParser = argparse.ArgumentParser(description='Convert Amba Raw to MTK Raw8.')
    #argParser.add_argument("cascPath", help="path of cascade classifier for face detection")
    argParser.add_argument("iff", type=str, help="the name of input file (Amba RAW)")
    argParser.add_argument("of", type=str, help="the name of output file (MTK Raw8)")
    argParser.add_argument("--width", default=2592, type=int, help="image width of the raw file")
    argParser.add_argument("--height", default=1944, type=int, help="image height of the raw file")
    # argParser.add_argument("--camid", required=True, type=int, help="the ID number of the camera, default=0")
    # argParser.add_argument("--delay", default=3, type=int, choices=range(2, 10), help="delay (sec) before starting detection and capture")
    # argParser.add_argument("--skip", default=2, choices=range(1,10), type=int, help="skip inteval (sec) after one frame is processed ")
    #argParser.add_argument("--ht", type=int, help="the high threshold of Canny detection")
    args = argParser.parse_args()

    #-- DEBUG only
    if False:
        print('args.iff= ', args.iff)
        print('args.of= ', args.of)


#---------------------------------------------------------
# Handle output directory
#---------------------------------------------------------

if False: #-- Debug ONLY !!
    print('Amba RAW: ', args.iff)
    srcPath = os.path.abspath(args.iff)
    srcName = os.path.basename(args.iff)
    srcBaseName, srcExtName = os.path.splitext(srcName)
    print('Path: ', srcPath)
    print('srcName={}, srcBaseName={}, srcExtname={}'.format(srcName, srcBaseName, srcExtName) )

    print('MTK RAW: ', args.of)

#-- read input file
ambaRawFile = args.iff
mtkRawFile = args.of
imgWidth = args.width
imgHeight = args.height
print("Reading Amba RAW: {} image size: {}x{}".format(ambaRawFile, imgWidth, imgHeight))

try:
    # f = open(rawfname, 'rb')
    # rawdata = f.read()
    # f.close()
    ambaRaw = np.fromfile(ambaRawFile, dtype=np.uint16)
except:
    print('Failed to open file : \n' + ambaRawFile)
    exit()

#-- reshape image to correct dimension
# for a in ambaRaw[:10]:
#     print('0x{:04x} '.format(a), end='')
# print('\n')

imgRaw = ambaRaw.reshape(imgHeight, imgWidth)
mtkRaw = (imgRaw >> 6)
mtkRaw = mtkRaw.astype(np.uint8)
outRaw = mtkRaw.reshape(imgWidth * imgHeight)

# for a in outRaw[:10]:
#     print('0x{:04x} '.format(a), end='')
# print('\n')

#-- Write MTK Raw8 file
print("Writing MTK RAW: {} ".format(mtkRawFile))
outRaw.tofile(mtkRawFile)
