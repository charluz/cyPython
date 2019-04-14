#!/usr/bin/python
#-- encoding: utf-8 --

import os, sys, platform
import argparse
import cv2
import numpy as np

import Add_cyModules as addCY

import cy_OSUTIL as cyOS
import cy_RawIMGUTIL as cySocRaw


SelAB = lambda A_true, B_false, Condtion : A_true if Condition else B_false

gImgRepoRoot = repr(os.getcwd())
gImgRepoCurr = gImgRepoRoot

gIsShowBayerImage = 0
gIsShowRawGray = 0
gIsShowRawRGB = 1

gIsSaveBayerImage = 0
gIsSaveRawGray = 0
gIsSaveRawRGB = 1

gMaxImgShowWidth = 640

debug_ctrl = False

bayerImg_geometric = { # (X, Y)
    0: (300, 140),  # R
    1: (340, 170),  # Gr
    2: (380, 200),  # Gb
    3: (420, 230),  # B
    100: (300, 300), # RawGray
    101: (330, 330) # RawRGB
}

###########################################################
# Print Program arguments
###########################################################
def print_arguments():
    global gCallByGui
    print("--- Program Arguments -----------------------------------------------")
    print("Called by GUI: ", gCallByGui)
    argstr = "rawImage"
    print(argstr, ": ", gRawImgFile)
    argstr = "width"
    print(argstr, ": ", gRawFormat[argstr])
    argstr = "height"
    print(argstr, ": ", gRawFormat[argstr])
    argstr = "bayer"
    print(argstr, ": ", gRawFormat[argstr])
    argstr = "bits"
    print(argstr, ": ", gRawFormat[argstr])
    print("---------------------------------------------------------------------")
    print()

###########################################################
# RAW Format JSON Parser
###########################################################
def conf_json_load(strJson):
    import json
    global gRawFormat

    #jsonDict = {}
    conf_json = strJson
    try:
        with open(conf_json, "r") as f:
            jsonDict = json.load(f)
    except:
        print("Error: failed to load configuration file ... ", conf_json)
        jsonDict = None

    #print(jsonDict)
    if jsonDict:
        # gRawFormat["showBayerColor"] = jsonDict["showBayerColor"]
        # gRawFormat["showRawGray"] = jsonDict["showRawGray"]
        gRawFormat["width"] = jsonDict["width"]
        gRawFormat["height"] = jsonDict["height"]
        gRawFormat["bits"] = jsonDict["bits"]
        gRawFormat["bayer"] = jsonDict["bayer"]

    return jsonDict




###########################################################
# MainEntry
###########################################################


gRawFormat = {
    "width"         : 1600,
    "height"        : 1200,
    "bits"          : 10,
    "bayer"         : 3,    #-- "bayer cdoe: R=0, Gr=1, Gb=2, B=3"
}


gProgConf = {
    "showBayerColor"    : False,
    "showRawGray"       : False,
    "showRawRGB"        : True,

    "saveRawRGB"        : True,
    "saveRawGray"       : True,
    "saveBayerColor"      : True,
}


if __name__ == "__main__":
    #-------------------------------------
    # Parse arguements
    #-------------------------------------
    argparse.ArgumentParser()
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('rawImg', help="input RAW image file name")
    parser.add_argument('--gui', nargs='?', const=1, type=int, default=0, help='JSON file for default RAW format.')
    parser.add_argument('--conf', help='JSON file for default RAW format.')
    parser.add_argument("-w", "--width", type=int, help='the width of the RAW image')
    parser.add_argument("-h", "--height", type=int, help='the height of the RAW image')
    parser.add_argument("--bayer", choices=['R', 'Gr', 'Gb', 'B'], help='bayer type of starting pixel\navailable options:R, Gr, Gb, B.')
    parser.add_argument("--bits", type=int, help='number of bits per pixel')
    parser.add_argument("--scale", type=int, help="percentage to downscale while generating output images, e.g., 30 stands for 30%%.")
    parser.add_argument("--ROI", help='+x+y*w+h to specify ROI of RAW image.')
    args = parser.parse_args()

    # print(args.conf)
    if args.conf:
        conf_json_load(args.conf)

    if args.width and args.height:
        gRawFormat["width"]     = args.width
        gRawFormat["height"]    = args.height

    if args.bits:
        gRawFormat["bits"]      = args.bits

    if args.bayer:
        gRawFormat["bayer"]     = args.bayer

    #-------------------------------------
    # Initialize globals
    #-------------------------------------
    gRawImgFile = args.rawImg
    gCallByGui = args.gui

    gRawWidth, gRawHeight = gRawFormat["width"], gRawFormat["height"]
    gRawBits = gRawFormat["bits"]
    gRawBayerType = gRawFormat["bayer"]

    gIsShowBayerImage = gProgConf["showBayerColor"]
    gIsShowRawGray = gProgConf["showRawGray"]
    gIsShowRawRGB = gProgConf["showRawRGB"]


    if False:   #-- Debug only !!
        print_arguments()

    #--------------------------------------------------
    rawIMG = cySocRaw.cySoCRaw(gRawImgFile, (gRawWidth, gRawHeight, gRawBits), gRawBayerType, debug=False)

    #--------------------------------------------------
    rawIMG.save_rawGray()
    #rawIMG.save_rawGray(outDir='./tmpImg')
    #rawIMG.display_rawGray()

    #--------------------------------------------------
    rawIMG.save_rawRGB()
    #rawIMG.display_rawRGB()

    #--------------------------------------------------
    rawIMG.split_raw_bayer_image()
    #rawIMG.save_raw_bayer_image()

    #--------------------------------------------------
    rawIMG.print_statistics(saveOutput=True, outExt=".txt")

    #--------------------------------------------------
    if not gCallByGui:
        while True:
            if 27 == cv2.waitKey(100):
                cv2.destroyAllWindows()
                break
