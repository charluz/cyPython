#!/usr/bin/python

import os, sys, platform

import argparse

# import _thread
# import time

import numpy as np
import cv2


import cyPyModules.Add_cyModules
import cyPyModules.shading_test_util as shadingUTIL

import cy_OSUTIL as cyOS
import image_Shading as IS
import cy_CvOSD as OSD
import cy_debug as DP
import cy_COMMON as cyCMN


gImgFilename    = ""
gSrcImgDir      = ""
gSrcImgBase     = ""
gSrcImgExt      = ""

# just to declare global variables
gSrcImgName=''
gSpecLumaC2C    = 0
gSpecLumaDev    = 0
gSpecChromaDev  = 0
gWinSizeRatio   = 0
gDiagField      = 0
gHvField        = 0
gIsGui          = False


color_pass = (0, 255, 0)
color_ng = (0, 0, 255)
lwidth = 2



###########################################################
# Print Program arguments
###########################################################
def print_arguments(args):
    print("--- Program Arguments -----------------------------------------------")
    print(args)
    print("---------------------------------------------------------------------")
    print()


###########################################################
# MainEntry
###########################################################


DBG = DP.DebugPrint('ShadingTEST')
DBG.enable_trace(False)

def main():
    #-------------------------------------
    # Parse arguements
    #-------------------------------------
    """
    lumaspec  : 1x2 array, 1st: CornerLuma/CenterLuma 最小百分比， 2nd: CornerLuma/所有CornerLuma平均 的偏差百分比 e.g., 10 --> 90% ~ 110%
    chromaspec: corner R/G, B/G 的色偏百分比
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('img', help="input image file name")
    parser.add_argument('--gui', nargs='?', const=1, type=int, default=0, help='JSON file for default RAW format.')
    parser.add_argument('--conf', help='JSON file for default RAW format.')
    parser.add_argument("--lumaspec", nargs=2, type=int, default=[85, 10], help='spec of luma shading, Corner/Center percentage, Inter-Corner Deviation percentage')
    parser.add_argument("--chromaspec", type=int, default=10, choices=range(1, 100), help='spec of chroma shading, Corner R/G, B/G percentage, Inter-Corner Deviation percentage')
    parser.add_argument("--winsize", type=int, default=10, choices=range(1,31), help='spec of chroma shading, Corner R/G, B/G percentage, Inter-Corner Deviation percentage')
    parser.add_argument("--dfield", type=int, default=100, choices=range(0,101), help='spec of chroma shading, Corner R/G, B/G percentage, Inter-Corner Deviation percentage')
    parser.add_argument("--hvfield", type=int, default=100, choices=range(0,101), help='spec of chroma shading, Corner R/G, B/G percentage, Inter-Corner Deviation percentage')
    parser.add_argument("--saveimg", nargs='?', const=1, type=int, default=0, help='save result shading image if specified')
    parser.add_argument("--output", type=str, default="", help='the directory to store the result image')
    #parser.add_argument("--scale", type=int, help="percentage to downscale while generating output images, e.g., 30 stands for 30%%.")
    #parser.add_argument("--ROI", help='+x+y*w+h to specify ROI of RAW image.')
    args = vars(parser.parse_args())

    if True:
        print_arguments(args)

    # print(args.conf)
    if args['conf']:
        conf_json_load(args['conf'])

    global gIsGui

    gImgFilename    = args['img']
    gSpecLumaC2C    = args['lumaspec'][0]/100.0
    gSpecLumaDev    = args['lumaspec'][1]/100.0
    gSpecChromaDev  = args['chromaspec']/100.0
    gWinSizeRatio   = args['winsize']/100.0
    gDiagField      = args['dfield']/100.0
    gHvField        = args['hvfield']/100.0
    gIsGui          = args['gui']
    gIsSaveImg      = args['saveimg']
    gOutputDir      = args['output']

    if True:
        #-- print global variables
        print('--- gImgFilename= ', gImgFilename)
        print('--- gSpecLumaC2C= ', gSpecLumaC2C)
        print('--- gSpecLumaDev= ', gSpecLumaDev)
        print('--- gSpecChromaDev= ', gSpecChromaDev)
        print('--- gWinSizeRatio= ', gWinSizeRatio)
        print('--- gDiagField= ', gDiagField)
        print('--- gHvField= ', gHvField)
        print('--- gIsGui= ', gIsGui)
        print('--- gIsSaveImg= ', gIsSaveImg)
        print('--- gOutputDir= ', gOutputDir)


    try:
        # f = open(gOpenFileName, 'rb')
        # rawdata = f.read()
        # f.close()
        # rawdata = np.fromfile(gOpenFileName, dtype=np.uint16)
        gSrcImgDir, gSrcImgBase, gSrcImgExt = cyOS.parse_path(gImgFilename)
        DBG.info("Image file:{} --> D:{}, B:{}, E:{}".format(gImgFilename, gSrcImgDir, gSrcImgBase, gSrcImgExt))
    except:
        DBG.error('Failed to open file :\n' + gOpenFileName)
        return


    # -- modify title of main window, change button to RESET
    gSrcImgName = gSrcImgBase + gSrcImgExt

    # -- Open and show image with CV2
    #os.chdir(gSrcImgDir)
    try:
        gImgSrc = cv2.imread(gImgFilename)
        DBG.info('Image Size: ', gImgSrc.shape[1], '*', gImgSrc.shape[0])
    except:
        DBG.error('CV2 failed to load image file: ' + gImgFilename)
        return


    #-------------------------------------------
    # Create & configure shading test control
    #-------------------------------------------
    #global gIsImgOpened
    #gIsImgOpened = True

    global gImageShading
    gImageShading = IS.ImageShading(gImgSrc.shape[1], gImgSrc.shape[0])
    hvEnabled = (gHvField > 0.0)
    gImageShading.set_property(h_enable=hvEnabled)
    gImageShading.set_property(v_enable=hvEnabled)
    #gImageShading.set_property(luma_enable=True)
    #gImageShading.set_property(chroma_enable=False)

    #-- Update center rectangle size
    gImageShading.set_property(c_size_ratio=gWinSizeRatio)
    gImageShading.set_property(e_size_ratio=gWinSizeRatio)
    gImageShading.set_property(d_field=gDiagField)
    gImageShading.set_property(hv_field=gHvField)

    #shadingUTIL.update_shading_rectangles(gImageShading, gImgSrc)

    imgWC = gImgSrc.copy()
    gShadingINFO = gImageShading.update(imgWC)

    #test_all_shadings(gSrcImgName, imgWC)


    centerY = gShadingINFO['Co'].get('Y')
    isChkLuma = (gSpecLumaC2C > 0)
    isChkColor = (gSpecChromaDev > 0)
    spec = [centerY, gSpecLumaC2C, gSpecLumaDev, gSpecChromaDev, isChkLuma, isChkColor]
    DBG.trace("SPEC: ceterY= {}, lumaC2C= {}, lumadev={}, chromaDev= {}, chkLuma= {}, chkChroma= {}".format(centerY, gSpecLumaC2C, gSpecLumaDev, gSpecChromaDev, isChkLuma, isChkColor))
    #-------------------------
    # Diagonal: Q1/Q2/Q3/Q4
    #-------------------------
    shadingUTIL.test_shading(imgWC, gShadingINFO, ['Q1', 'Q2', 'Q3', 'Q4'], spec)

    #-------------------------
    # Horizontal: Hr, Hl
    #-------------------------
    if hvEnabled:
        shadingUTIL.test_shading(imgWC, gShadingINFO, ['Hr', 'Hl'], spec)

    #-------------------------
    # Horizontal: Vt, Vb
    #-------------------------
    if hvEnabled:
        shadingUTIL.test_shading(imgWC, gShadingINFO, ['Vb', 'Vt'], spec)

    #--- Display
    if gIsGui:
        cv2.namedWindow(gSrcImgName, cv2.WINDOW_NORMAL)
        #-- resize window to 720p in image height
        resizeH = 720
        if gImgSrc.shape[1] > resizeH:
            w = int(resizeH*gImgSrc.shape[1]/gImgSrc.shape[0])
            h = resizeH
            cv2.resizeWindow(gSrcImgName, w, h)
            DBG.info('Output window resized to: ', w, '*', h)

        cv2.imshow(gSrcImgName, imgWC)

    #--- Save result image
    if gIsSaveImg:
        gOutputDir = cyCMN.SelectAB(gSrcImgDir, gOutputDir, (gOutputDir == ""))
        cyOS.create_dir(gOutputDir)
        gOutputImgFilename = gOutputDir + '/' + gSrcImgBase + '_shading' + gSrcImgExt
        DBG.trace("OUTPUT: {}".format(gOutputImgFilename))
        cv2.imwrite(gOutputImgFilename, imgWC)

    return




###########################################################
# Function : exit_prog
###########################################################
def exit_prog():
    cv2.destroyAllWindows()
    DBG.info('<<<exit_prog>>>')



if __name__ == "__main__":
    global gIsGui
    main()

    if gIsGui:
        while True:
            if 27 == cv2.waitKey(100):
                cv2.destroyAllWindows()
                break

    exit_prog()
