#!/usr/bin/env python

import os, sys
import argparse

import cv2
import numpy as np

gImgRepoRoot = repr(os.getcwd())
gImgRepoCurr = gImgRepoRoot
gRawBaseName = ""
gIsShowBayerImage = 0
gIsShowRawImage = 1
gIsShowRawRGB = 0


###########################################################
# Functions : Create working folders
###########################################################
def createDirectory(name):
    if not os.path.exists(name):
        try:
            os.mkdir(name)
        except:
            print("Can't create folder : \n"+repr(name))
            return ""
        print("Directory ", name, " created.")
    else:
        print("Directory ", name, " already exists.")

    return name


def createImageRepoRoot(cwd, name):
    # print(cwd + name)
    return createDirectory(cwd+name)


###########################################################
# Functions : saveSplitedImage
###########################################################
def saveSplitedImage(imgGray, bayerCode, isShowImg, winName):
    img = imgGray.astype(np.uint8)
    matImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if bayerCode == 0:      # R
        matImg[:,:,0] = 0
        matImg[:,:,1] = 0
    elif bayerCode == 1 or bayerCode == 2:    # Gr / Gb
        matImg[:,:,0] = 0
        matImg[:,:,2] = 0
    else:                   # B
        matImg[:,:,1] = 0
        matImg[:,:,2] = 0

    if not winName:
        winName = 'bayerColor'+str(bayerCode)
    # print(gRawBaseName+winName)
    cv2.imwrite(gRawBaseName+"_"+winName+".jpg", matImg)

    return matImg

def save_raw_RGrGbB_image(img1, img2, img3, img4):
    saveSplitedImage(img1, 0, gIsShowBayerImage, "RAW_R")
    saveSplitedImage(img2, 1, gIsShowBayerImage, "RAW_Gr")
    saveSplitedImage(img3, 2, gIsShowBayerImage, "RAW_Gb")
    saveSplitedImage(img4, 3, gIsShowBayerImage, "RAW_B")

def save_raw_GrRBGb_image(img1, img2, img3, img4):
    saveSplitedImage(img1, 1, gIsShowBayerImage, "RAW_Gr")
    saveSplitedImage(img2, 0, gIsShowBayerImage, "RAW_R")
    saveSplitedImage(img3, 3, gIsShowBayerImage, "RAW_B")
    saveSplitedImage(img4, 2, gIsShowBayerImage, "RAW_Gb")

def save_raw_GbBRGr_image(img1, img2, img3, img4):
    saveSplitedImage(img1, 2, gIsShowBayerImage, "RAW_Gb")
    saveSplitedImage(img2, 3, gIsShowBayerImage, "RAW_B")
    saveSplitedImage(img3, 0, gIsShowBayerImage, "RAW_R")
    saveSplitedImage(img4, 1, gIsShowBayerImage, "RAW_Gr")

def save_raw_BGbGrR_image(img1, img2, img3, img4):
    saveSplitedImage(img1, 3, gIsShowBayerImage, "RAW_B")
    saveSplitedImage(img2, 2, gIsShowBayerImage, "RAW_Gb")
    saveSplitedImage(img3, 1, gIsShowBayerImage, "RAW_Gr")
    saveSplitedImage(img4, 0, gIsShowBayerImage, "RAW_R")


def save_raw_XXXX_image(img1, img2, img3, img4):
    print("Error, Unknown bayer type !!")


###########################################################
# Function : Split Bayer Components
###########################################################
def split_n_save_bayer_raw(imgRaw, nbit, bayerCode):
    imgW, imgH = imgRaw.shape[1], imgRaw.shape[0]  # (int(width>>1))<<1, (int(height>>1)<<1)
    simgW, simgH =  int(imgW>>1), int(imgH>>1)
    bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4 = [np.zeros([simgH, simgW, 1], np.uint8) for x in range(4)]

    # print("width %d -> %d, height %d -> %d" % (imgW, simgW, imgH, simgH))
    bitshift = nbit-8

    if nbit > 8:
        bayerImgC1 = imgRaw[0:imgH+1:2, 0:imgW+1:2] >> bitshift
        bayerImgC2 = imgRaw[0:imgH+1:2, 1:imgW+1:2] >> bitshift
        bayerImgC3 = imgRaw[1:imgH+1:2, 0:imgW+1:2] >> bitshift
        bayerImgC4 = imgRaw[1:imgH+1:2, 1:imgW+1:2] >> bitshift
    else:
        bayerImgC1 = imgRaw[0:imgH+1, 0:imgW+1]
        bayerImgC2 = imgRaw[0:imgH+1, 1:imgW+1]
        bayerImgC3 = imgRaw[1:imgH+1, 0:imgW+1]
        bayerImgC4 = imgRaw[1:imgH+1, 1:imgW+1]


    save_bayer_img = {
        0:save_raw_RGrGbB_image,
        1:save_raw_GrRBGb_image,
        2:save_raw_GbBRGr_image,
        3:save_raw_BGbGrR_image
    }

    func = save_bayer_img.get(bayerCode, save_raw_XXXX_image)
    func(bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4)

    return



###########################################################
# Functions : saveRawGrayImage
###########################################################

def save_raw_images(rawImg, bayerCode, nbits):
    global gRawBaseName
    
    bayer2gray_code = {
        0: cv2.COLOR_BAYER_RG2GRAY,
        1: cv2.COLOR_BAYER_GR2GRAY,
        2: cv2.COLOR_BAYER_GB2GRAY,
        3: cv2.COLOR_BAYER_BG2GRAY
    }

    bayer2bgr_code = {
        0: cv2.COLOR_BAYER_RG2BGR,
        1: cv2.COLOR_BAYER_GR2BGR,
        2: cv2.COLOR_BAYER_GB2BGR,
        3: cv2.COLOR_BAYER_BG2BGR
    }

    if nbits > 8:
        matRaw = rawImg << (16-nbits)
    else:
        matRaw = rawImg

    ##-----------------------------
    ## Bayer2Gray
    ##-----------------------------
    cvtCode = bayer2gray_code.get(bayerCode, cv2.COLOR_BAYER_RG2GRAY)
    matGray = cv2.cvtColor(matRaw, cvtCode)
    if nbits > 8:
        matGray = matGray / 256
    matGray = matGray.astype(np.uint8)

    jpgGray = gRawBaseName + "_RawGray" + '.jpg'
    print("Saving {0} ...".format(jpgGray) )
    cv2.imwrite(jpgGray, matGray)

    ##-----------------------------
    ## Bayer2BGR
    ##-----------------------------
    cvtCode = bayer2bgr_code.get(bayerCode, cv2.COLOR_BAYER_RG2BGR)
    matBGR = cv2.cvtColor(matRaw, cvtCode)
    if nbits > 8:
        matBGR = matBGR / 256
    matBGR = matBGR.astype(np.uint8)

    jpgRGB = gRawBaseName + "_RawRGB" + '.jpg'
    print("Saving {0} ...".format(jpgRGB) )
    cv2.imwrite(jpgRGB, matBGR)

    return


###########################################################
# Parse RAW image
###########################################################
def parse_n_save_raw_jpeg(bayerRaw, nbit, bayerCode):
    save_raw_images(bayerRaw, bayerCode, nbit)
    split_n_save_bayer_raw(bayerRaw, nbit, bayerCode)
    return




###########################################################
# Open RAW image
###########################################################
def open_raw_image_file(rawImgFile, nbit):
    global gRawBaseName

    rawfname = rawImgFile
    try:
        if nbit > 8:
            rawBayer = np.fromfile(rawfname, dtype=np.uint16)
        else:
            rawBayer = np.fromfile(rawfname, dtype=np.uint8)
    except:
        print("Failed to open file : ", rawfname)
        return None

    # Create root repository folder for output images
    print(rawfname)
    gImgRepoRoot = os.path.dirname(rawfname)
    print(type(gImgRepoRoot))
    if "" == gImgRepoRoot:
        gImgRepoRoot = "."
    os.chdir(gImgRepoRoot)
    gImgRepoRoot = createImageRepoRoot(gImgRepoRoot, "/_imageRepo")
    # print(gImgRepoRoot)

    # Create folder to save output images for loaded RAW image
    baseName = os.path.basename(rawfname)

    base, ext = os.path.splitext(baseName)
    gImgRepoCurr = gImgRepoRoot + "/" + base
    #print("Target image repo ", gImgRepoCurr)
    if createDirectory(gImgRepoCurr):
        os.chdir(gImgRepoCurr)

    gRawBaseName = base
    return rawBayer


###########################################################
# RAW Format JSON Parser
###########################################################
def conf_json_load():
    import json
    global gRawFormat

    #jsonDict = {}
    conf_json = "./raw_conf.json"
    try:
        with open(conf_json, "r") as f:
            jsonDict = json.load(f)
    except:
        print("Error: failed to load configuration file ... ", conf_json)
        jsonDict = None

    #print(jsonDict)
    if jsonDict:
        gRawFormat["showBayerColor"] = jsonDict["showBayerColor"]
        gRawFormat["showRawGray"] = jsonDict["showRawGray"]
        gRawFormat["width"] = jsonDict["width"]
        gRawFormat["height"] = jsonDict["height"]
        gRawFormat["bits"] = jsonDict["bits"]
        gRawFormat["bayer"] = jsonDict["bayer"]

    return jsonDict




###########################################################
# Function: Parse file's path/basename/extname
###########################################################
def parse_file_path(fpath):

    print('Input filename: ', fpath)

    # Create root repository folder for output images
    fdir = os.path.dirname(fpath)
    ffile = os.path.basename(fpath)
    fbase, fext = os.path.splitext(ffile)
    # try:
    #     fdir = os.path.dirname(fpath)
    #     ffile = os.path.basename(fpath)
    #     fbase, fext = os.path.splitext(ffile)
    # except:
    #     print("Error: failed to parse file path, name.")
    #     return '', '', ''

    print('Directory: ', fdir)
    print("fbase= ", fbase, 'fext= ', fext)

    return fdir, fbase, fext


###########################################################
# MainEntry
###########################################################

gAppGlobs = {
    "srcImgFile"        : "",
    "width"             : 1600,
    "height"            : 1200,
}



def print_arguments():
    print("--- Program Arguments -----------------------------------------------")
    argstr = "srcImgFile"
    print(argstr, ": ", gAppGlobs[argstr])
    # argstr = "width"
    # print(argstr, ": ", gAppGlobs[argstr])
    # argstr = "height"
    # print(argstr, ": ", gAppGlobs[argstr])
    print("---------------------------------------------------------------------")
    print()



if __name__ == "__main__":
    import image_Shading as IS
    import cy_CvOSD as OSD
    import cy_debug as DP
    
    # #-------------------------------------
    # # Parse arguements
    # #-------------------------------------
    argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('srcImage', help="input RAW image file name")
    # parser.add_argument('--conf', help='JSON file for default RAW format.')
    # parser.add_argument("--width", type=int, help='the width of the image')
    # parser.add_argument("--height", type=int, help='the height of the image')
    # parser.add_argument("-b", "--bayer", choices=['R', 'Gr', 'Gb', 'B'], help='bayer type of starting pixel\navailable options:R, Gr, Gb, B.')
    # parser.add_argument("-n", "--bits", type=int, help='number of bits per pixel')
    # parser.add_argument("--scale", type=int, help="percentage to downscale while generating output images, e.g., 30 stands for 30%%.")
    # parser.add_argument("--ROI", help='+x+y*w+h to specify ROI of RAW image.')
    args = parser.parse_args()

    if args.srcImage:
        gAppGlobs["srcImgFile"] = args.srcImage 
    # # print(args.conf)
    # if args.conf:
    #     conf_json_load()
    # else:
    #     if args.width and args.height:
    #         gRawFormat["width"]     = args.width
    #         gRawFormat["height"]    = args.height
    #     elif args.bits:
    #         gRawFormat["bits"]      = args.bits
    #     elif args.bayer:
    #         gRawFormat["bayer"]     = args.bayer
    #     else:
    #         pass

    if True:    #-- Debug Only !!
        print_arguments()

    #-------------------------------------
    # Open Image
    #-------------------------------------
    gSrcImgFile = gAppGlobs["srcImgFile"]
    gSrcImgDir, gSrcImgBase, gSrcImgExt = parse_file_path(gSrcImgFile)
    gSrcImgName = gSrcImgBase + gSrcImgExt

    # -- Open and show image with CV2
    if "" == gSrcImgDir:
        gSrcImgDir = "."
    os.chdir(gSrcImgDir)

    try:
        gImgSrc = cv2.imread(gSrcImgFile)
        print('Image Size: ', gImgSrc.shape[1], '*', gImgSrc.shape[0])
        gWidth, gHeight = gImgSrc.shape[1], gImgSrc.shape[0]
        cv2.namedWindow(gSrcImgName, cv2.WINDOW_NORMAL)
    except:
        print("CV2 failed to load image file : ", gSrcImgFile)
        exit(-1)
    else:
        print('Image Size: ', gImgSrc.shape[1], '*', gImgSrc.shape[0])
        gWidth, gHeight = gImgSrc.shape[1], gImgSrc.shape[0]
        cv2.namedWindow(gSrcImgName, cv2.WINDOW_NORMAL)
        #-- resize window to 720p in image height
        resizeH = 480
        if gImgSrc.shape[1] > resizeH:
            w = int(resizeH*gImgSrc.shape[1]/gImgSrc.shape[0])
            h = resizeH
            cv2.resizeWindow(gSrcImgName, w, h)
            print('Output window resized to: ', w, '*', h)
            # cv2.imshow(gSrcImgName, gImgSrc)


    #-------------------------------------
    # Create Shading Calcualtion
    #-------------------------------------
    global gImageShading
    gImageShading = IS.ImageShading(gImgSrc.shape[1], gImgSrc.shape[0])

    #-- Enable shading blocks
    gImageShading.set_property(h_enable=True)
    gImageShading.set_property(v_enable=True)
    gImageShading.set_property(luma_enable=True)
    gImageShading.set_property(chroma_enable=True)

    #-- Update center rectangle size
    gImageShading.set_property(c_size_ratio=0.1)
    gImageShading.set_property(e_size_ratio=0.1)
    gImageShading.set_property(d_field=1.0))
    gImageShading.set_property(hv_field=1.0)

    gImgWC = gImgSrc.copy()
    global gShadingINFO
    gShadingINFO = gImageShading.update(gImgWC)

    #gImageShading.show(gSrcImgName, gImgWC)
    test_all_shadings(gSrcImgName, gImgWC)

    return



    # gRawBits = gRawFormat["bits"]
    # gRawBayerTye = gRawFormat["bayer"]

    # gIsShowBayerImage = gRawFormat["showBayerColor"]
    # gIsShowRawImage = gRawFormat["showRawGray"]
    # gIsShowRawRGB = gRawFormat["showRawRGB"]

    # if False:   #-- Debug only !!
    #     print_arguments()

    # # print(gRawWidth, " x ", gRawHeight)
    # gRawBayer = open_raw_image_file(gRawImgFile, gRawBits)
    # gRawBayer = gRawBayer.reshape(gRawHeight, gRawWidth)

    # parse_n_save_raw_jpeg(gRawBayer, gRawBits, gRawBayerTye)

