#!/usr/bin/python

import os, sys

from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import cv2

import numpy as np
# import matplotlib.pyplot as plt

'''
from tkFileDialog import askopenfilename

That code would have worked fine in Python 2.x, but it is no longer valid.
In Python 3.x, tkFileDialog was renamed to filedialog.
'''

gImgRepoRoot = repr(os.getcwd())
gImgRepoCurr = gImgRepoRoot
gRawBaseName = ""
gIsShowBayerImage = 0
gIsShowRawImage = 1
gIsShowRawRGB = 0
gMaxImgShowWidth = 640

bayerCode_Table = {
    'bayerR':  0,
    'bayerGr': 1,
    'bayerGb': 2,
    'bayerB':  3
}

bayer2gray_code = {
    0: cv2.COLOR_BAYER_BG2GRAY,
    1: cv2.COLOR_BAYER_GB2GRAY,
    2: cv2.COLOR_BAYER_GR2GRAY,
    3: cv2.COLOR_BAYER_RG2GRAY
}


bayer2bgr_code = {
    0: cv2.COLOR_BAYER_BG2BGR,
    1: cv2.COLOR_BAYER_GB2BGR,
    2: cv2.COLOR_BAYER_GR2BGR,
    3: cv2.COLOR_BAYER_RG2BGR
}


bayerImg_geometric = { # (X, Y)
    0: (300, 140),  # R
    1: (340, 170),  # Gr
    2: (380, 200),  # Gb
    3: (420, 230),  # B
    100: (300, 300), # RawGray
    101: (330, 330) # RawRGB
}


###########################################################
# Bayer Color lookup functions
###########################################################
def bayerCode_Name2ID(szName):
    return bayerCode_Table.get(szName, 0)


###########################################################
# Message Box with OK button
###########################################################
def messageBoxOK(title, msg):
    global textvarStatusBar
    if False:
        box = Toplevel()
        box.title(title)
        Label(box, text=msg).pack()
        Button(box, text='OK', command=box.destroy).pack()
    else:
        sz = title+': '+msg
        print(sz)
        textvarStatusBar.set(sz)



###########################################################
# Functions : Create working folders
###########################################################
def createDirectory(name):
    if not os.path.exists(name):
        try:
            os.mkdir(name)
        except:
            messageBoxOK("Error", "Can't create folder : \n"+repr(name))
            return ""
        print("Directory ", name, " created.")
    else:
        print("Directory ", name, " already exists.")

    return name



def createImageRepoRoot(cwd, name):
    # print(cwd + name)
    return createDirectory(cwd+name)


###########################################################
# Function : Callback of Button RESET
###########################################################
def cbfnButtonReset():
    cv2.destroyAllWindows()
    btnRaw.config(text='Open RAW', command=cbfnButtonOpenRaw, bg='LightGreen')
    textvarStatusBar.set("")



###########################################################
# Functions : saveRawGrayImage
###########################################################

def saveRawGrayImage(rawImg, bayerCode):
    bits = int(txtlblRawBits.get())
    if bits > 8:
        matRaw = rawImg << (16-bits)
    else:
        matRaw = rawImg

    ## Bayer2Gray
    code = bayer2gray_code.get(bayerCode, cv2.COLOR_BAYER_RG2GRAY)
    matGray = cv2.cvtColor(matRaw, code)
    if bits > 8:
        matGray = matGray / 256
    matGray = matGray.astype(np.uint8)

    # print(matGray)
    win_title = "RAW_Gray"
    if gIsShowRawImage:
        cv2.namedWindow(win_title, cv2.WINDOW_NORMAL)
        x, y = bayerImg_geometric.get(100)
        cv2.moveWindow(win_title, x, y)
        h, w = matGray.shape
        if w > gMaxImgShowWidth:
            h = int( (h * gMaxImgShowWidth) / w)
            w = gMaxImgShowWidth
        cv2.resizeWindow(win_title, w, h)
        cv2.imshow(win_title, matGray)

    jpgGray = gRawBaseName + "_" + win_title + '.jpg'
    cv2.imwrite(jpgGray, matGray)

    ## Bayer2BGR
    code = bayer2bgr_code.get(bayerCode, cv2.COLOR_BAYER_RG2BGR)
    matBGR = cv2.cvtColor(matRaw, code)
    if bits > 8:
        matBGR = matBGR / 256
    matBGR = matBGR.astype(np.uint8)

    win_title = "RAW_RGB"
    if gIsShowRawRGB:
        cv2.namedWindow(win_title, cv2.WINDOW_NORMAL)
        x, y = bayerImg_geometric.get(101)
        cv2.moveWindow(win_title, x, y)

        print(matBGR.shape)
        h, w, c = matBGR.shape
        if w > gMaxImgShowWidth:
            h = int( (h * gMaxImgShowWidth) / w)
            w = gMaxImgShowWidth
        cv2.resizeWindow(win_title, w, h)
        cv2.imshow(win_title, matBGR)

    jpgRGB = gRawBaseName + "_" + win_title + '.jpg'
    cv2.imwrite(jpgRGB, matBGR)

    return


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

    if isShowImg:
        cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
        w = matImg.shape[1]
        h = matImg.shape[0]
        if w > gMaxImgShowWidth:
            h = int((h * gMaxImgShowWidth) / w)
            w = gMaxImgShowWidth
        cv2.resizeWindow(winName, w, h)
        x, y = bayerImg_geometric.get(bayerCode)
        cv2.moveWindow(winName, x, y)
        cv2.imshow(winName, matImg)

    return matImg

def save_raw_RGrGbB_image(img1, img2, img3, img4):
    global gbayerMean
    saveSplitedImage(img1, 0, gIsShowBayerImage, "RAW_R")
    saveSplitedImage(img2, 1, gIsShowBayerImage, "RAW_Gr")
    saveSplitedImage(img3, 2, gIsShowBayerImage, "RAW_Gb")
    saveSplitedImage(img4, 3, gIsShowBayerImage, "RAW_B")
    szRawMean="Raw Mean (R/Gr/Gb/B): ({:.1f}, {:.1f}, {:.1f}, {:.1f})".format(gbayerMean[0], gbayerMean[1], gbayerMean[2], gbayerMean[3])
    return szRawMean

def save_raw_GrRBGb_image(img1, img2, img3, img4):
    global gbayerMean
    saveSplitedImage(img1, 1, gIsShowBayerImage, "RAW_Gr")
    saveSplitedImage(img2, 0, gIsShowBayerImage, "RAW_R")
    saveSplitedImage(img3, 3, gIsShowBayerImage, "RAW_B")
    saveSplitedImage(img4, 2, gIsShowBayerImage, "RAW_Gb")
    szRawMean="Raw Mean (R/Gr/Gb/B): ({:.1f}, {:.1f}, {:.1f}, {:.1f})".format(gbayerMean[1], gbayerMean[0], gbayerMean[3], gbayerMean[2])
    return szRawMean

def save_raw_GbBRGr_image(img1, img2, img3, img4):
    global gbayerMean
    saveSplitedImage(img1, 2, gIsShowBayerImage, "RAW_Gb")
    saveSplitedImage(img2, 3, gIsShowBayerImage, "RAW_B")
    saveSplitedImage(img3, 0, gIsShowBayerImage, "RAW_R")
    saveSplitedImage(img4, 1, gIsShowBayerImage, "RAW_Gr")
    szRawMean="Raw Mean (R/Gr/Gb/B): ({:.1f}, {:.1f}, {:.1f}, {:.1f})".format(gbayerMean[2], gbayerMean[3], gbayerMean[0], gbayerMean[1])
    return szRawMean

def save_raw_BGbGrR_image(img1, img2, img3, img4):
    global gbayerMean
    saveSplitedImage(img1, 3, gIsShowBayerImage, "RAW_B")
    saveSplitedImage(img2, 2, gIsShowBayerImage, "RAW_Gb")
    saveSplitedImage(img3, 1, gIsShowBayerImage, "RAW_Gr")
    saveSplitedImage(img4, 0, gIsShowBayerImage, "RAW_R")
    szRawMean="Raw Mean (R/Gr/Gb/B): ({:.1f}, {:.1f}, {:.1f}, {:.1f})".format(gbayerMean[3], gbayerMean[2], gbayerMean[1], gbayerMean[0])
    return szRawMean


def save_raw_XXXX_image(img1, img2, img3, img4):
    messageBoxOK('ERROR', 'Unknown bayer type !!')


###########################################################
# Function : Split Bayer Components
###########################################################
def splitBayerRawU16(bayerdata, width, height, rawBits, bayerType):
    '''
    @Brief
        To split R/Gr/Gb/B components from Bayer Raw image input.
    @In
        bayerdata   : Raw image input (from io.open/io.read)
        width, height   : size of Raw image
        rawBits     : number of bits per pixel
    @Out
        boolean : indicating success/failure
    @Globals
        bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4 : sub-images of R/Gr/Gb/B.
            Size of sub-image is (widht/2, height/2).
    '''
    global bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4

    imgW, imgH = (int(width>>1))<<1, (int(height>>1)<<1)
    simgW, simgH =int(imgW>>1), int(imgH>>1)
    bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4 = [np.zeros([simgH, simgW, 1], np.uint8) for x in range(4)]

    print("width %d -> %d, height %d -> %d" % (imgW, simgW, imgH, simgH))

    btnRaw.config(bg='Coral')
    bitshift = rawBits-8

    #print("--- 1 ---")
    imgRaw = bayerdata.reshape(imgH, imgW)
    #print("--- 1-1 ---")
    saveRawGrayImage(imgRaw, bayerType)
    #print("--- 2 ---")

    global gbayerMean
    gbayerMean = np.zeros(4, dtype=np.float)
    if rawBits > 8:
        bayerImg = imgRaw[0:imgH+1:2, 0:imgW+1:2]
        gbayerMean[0] = bayerImg.mean()
        bayerImgC1 = bayerImg >> bitshift

        bayerImg = imgRaw[0:imgH+1:2, 1:imgW+1:2]
        gbayerMean[1] = bayerImg.mean()
        bayerImgC2 = bayerImg >> bitshift

        bayerImg = imgRaw[1:imgH+1:2, 0:imgW+1:2]
        gbayerMean[2] = bayerImg.mean()
        bayerImgC3 = bayerImg >> bitshift

        bayerImg = imgRaw[1:imgH+1:2, 1:imgW+1:2]
        gbayerMean[3] = bayerImg.mean()
        bayerImgC4 = bayerImg >> bitshift

        #print("Bayer mean: {:.2f}".format(gbayerMean[0]))
    else:
        bayerImgC1 = imgRaw[0:imgH+1:2, 0:imgW+1:2]
        gbayerMean[0] = bayerImgC1.mean()
        print("Bayer mean: {:.2f}".format(gbayerMean[0]))
        #print(bayImgC1[476:497, 612:633])

        bayerImgC2 = imgRaw[0:imgH+1:2, 1:imgW+1:2]
        gbayerMean[1] = bayerImgC2.mean()
        print("Bayer mean: {:.2f}".format(gbayerMean[1]))
        #print(bayImgC2[476:497, 612:633])

        bayerImgC3 = imgRaw[1:imgH+1:2, 0:imgW+1:2]
        gbayerMean[2] = bayerImgC3.mean()
        print("Bayer mean: {:.2f}".format(gbayerMean[2]))
        #print(bayImgC3[476:497, 612:633])

        bayerImgC4 = imgRaw[1:imgH+1:2, 1:imgW+1:2]
        gbayerMean[3] = bayerImgC4.mean()
        print("Bayer mean: {:.2f}".format(gbayerMean[3]))
        #print(bayImgC4[476:497, 612:633])



    save_bayer_img = {
        0:save_raw_RGrGbB_image,
        1:save_raw_GrRBGb_image,
        2:save_raw_GbBRGr_image,
        3:save_raw_BGbGrR_image
    }

    func = save_bayer_img.get(bayerType, save_raw_XXXX_image)
    szMean = func(bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4)
    textvarStatusBar.set(szMean)    #-- show Bayer mean values
    btnRaw.config(text='RESET', command=cbfnButtonReset, bg='LightBlue')


    # plt.imshow(bayerImgC4); plt.show()
    # plt.imshow(bayerImgC3); plt.show()
    # plt.imshow(bayerImgC2); plt.show()
    # plt.imshow(bayerImgC1); plt.show()
    # plt.imshow(imgRaw); plt.show()
    # plt.imsave('./bayerImgC1.jpg', bayerImgC1)
    # plt.imsave('./bayerImgC2.jpg', bayerImgC2)
    # plt.imsave('./bayerImgC3.jpg', bayerImgC3)
    # plt.imsave('./bayerImgC4.jpg', bayerImgC4)
    return True


###########################################################
# Button Function : LoadRAW
###########################################################
def cbfnButtonLoadRaw():
    global btnRaw, rawdata
    # print("Button: Load RAW")
    try:
        #print("--- A ---")
        splitBayerRawU16(rawdata, int(txtlblRawWidth.get()),
                        int(txtlblRawHeight.get()),
                        int(txtlblRawBits.get()),
                        bayerSelect.get())
        #print("--- B ---")
    except:
        cbfnButtonReset()
        return

###########################################################
# Button Function : OpenRAW
###########################################################
def cbfnButtonOpenRaw():
    global winMain, winTitle, txtlblRawFName, btnRaw, btn
    global rawdata, rawfname, gRawBaseName
    global gIsShowBayerImage, chkShowBayerImg
    global gIsShowRawImage, chkShowRawImg
    global gIsShowRawRGB, chkShowRawRGB

    rawfname = filedialog.askopenfilename()
    bits = int(txtlblRawBits.get())
    #print(rawfname)
    try:
        # f = open(rawfname, 'rb')
        # rawdata = f.read()
        # f.close()
        if bits > 8:
            rawdata = np.fromfile(rawfname, dtype=np.uint16)
        else:
            rawdata = np.fromfile(rawfname, dtype=np.uint8)
    except:
        messageBoxOK('FileIO', 'Failed to open file :\n' + rawfname)
        cbfnButtonReset()
        return

    # Create root repository folder for output images
    gImgRepoRoot = os.path.dirname(rawfname)
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
    #print(gRawBaseName)

    # modify title of main window
    winMain.title(winTitle+ ' -- ' + baseName)

    #btnRaw.config(text='Load RAW', command=cbfnButtonLoadRaw, bg='Yellow')
    gIsShowBayerImage = chkShowBayerImg.get()
    gIsShowRawImage = chkShowRawImg.get()
    gIsShowRawRGB = chkShowRawRGB.get()

    # to Load and Parse RAW images
    cbfnButtonLoadRaw()

    return


###########################################################
# Button Function : Exit Main Window
###########################################################
def cbfnButtonMainExit():
    cv2.destroyAllWindows()
    winMain.destroy()
    return

###########################################################
# Button Function : Set Project RAW format
###########################################################
def update_RawFmtButtonColor(activeID):
    btnRawFmt1.config( fg='Black', bg="#D0D0D0")
    btnRawFmt2.config( fg='Black', bg="#D0D0D0")
    btnRawFmt3.config( fg='Black', bg="#D0D0D0")
    btnRawFmt4.config( fg='Black', bg="#D0D0D0")
    if activeID == 1:
        btnRawFmt1.config(fg='Yellow', bg="#0000FF")
    elif activeID == 2:
        btnRawFmt2.config(fg='Yellow', bg="#0000FF")
    elif activeID == 3:
        btnRawFmt3.config(fg='Yellow', bg="#0000FF")
    elif activeID == 4:
        btnRawFmt4.config(fg='Yellow', bg="#0000FF")


def config_raw_image_format(szWidth, szHeight, szBits, szBayeName):
    txtlblRawWidth.set(szWidth)
    txtlblRawHeight.set(szHeight)
    txtlblRawBits.set(szBits)
    bayerSelect.set(szBayeName)


def cbfnButtonConfigAntmanOS05A20():
    config_raw_image_format(gRawFmtTable["format_1"]["width"],
                                gRawFmtTable["format_1"]["height"],
                                gRawFmtTable["format_1"]["pixel_bits"],
                                gRawFmtTable["format_1"]["bayer"])
    update_RawFmtButtonColor(1)

def cbfnButtonConfigTheiaOS05A20():
    config_raw_image_format(gRawFmtTable["format_2"]["width"],
                                gRawFmtTable["format_2"]["height"],
                                gRawFmtTable["format_2"]["pixel_bits"],
                                gRawFmtTable["format_2"]["bayer"])
    update_RawFmtButtonColor(2)

def cbfnButtonConfigAntmanAR0330():
    config_raw_image_format(gRawFmtTable["format_3"]["width"],
                                gRawFmtTable["format_3"]["height"],
                                gRawFmtTable["format_3"]["pixel_bits"],
                                gRawFmtTable["format_3"]["bayer"])
    update_RawFmtButtonColor(3)

def cbfnButtonConfigHawkeye():
    config_raw_image_format(gRawFmtTable["format_4"]["width"],
                                gRawFmtTable["format_4"]["height"],
                                gRawFmtTable["format_4"]["pixel_bits"],
                                gRawFmtTable["format_4"]["bayer"])
    update_RawFmtButtonColor(4)


###########################################################
# RAW Format JSON Parser
###########################################################
def raw_format_json_load():
    import json
    global gRawFmtTable

    #jsonDict = {}
    try:
        with open("./raw_format.json") as f:
            jsonDict = json.load(f)
    except:
        jsonDict = None

    if jsonDict:
        gRawFmtTable["showBayerColor"] = jsonDict["showBayerColor"]
        gRawFmtTable["showRawGray"] = jsonDict["showRawGray"]
        gRawFmtTable["width"] = jsonDict["width"]
        gRawFmtTable["height"] = jsonDict["height"]
        gRawFmtTable["bits"] = jsonDict["bits"]
        gRawFmtTable["bayer"] = jsonDict["bayer"]

        gRawFmtTable["format_1"]["name"] = jsonDict["format_1"]["name"]
        gRawFmtTable["format_1"]["color"] = jsonDict["format_1"]["color"]
        gRawFmtTable["format_1"]["width"] = jsonDict["format_1"]["width"]
        gRawFmtTable["format_1"]["height"] = jsonDict["format_1"]["height"]
        gRawFmtTable["format_1"]["pixel_bits"] = jsonDict["format_1"]["pixel_bits"]
        gRawFmtTable["format_1"]["bayer"] = jsonDict["format_1"]["bayer"]

        gRawFmtTable["format_2"]["name"] = jsonDict["format_2"]["name"]
        gRawFmtTable["format_2"]["color"] = jsonDict["format_2"]["color"]
        gRawFmtTable["format_2"]["width"] = jsonDict["format_2"]["width"]
        gRawFmtTable["format_2"]["height"] = jsonDict["format_2"]["height"]
        gRawFmtTable["format_2"]["pixel_bits"] = jsonDict["format_2"]["pixel_bits"]
        gRawFmtTable["format_2"]["bayer"] = jsonDict["format_2"]["bayer"]

        gRawFmtTable["format_3"]["name"] = jsonDict["format_3"]["name"]
        gRawFmtTable["format_3"]["color"] = jsonDict["format_3"]["color"]
        gRawFmtTable["format_3"]["width"] = jsonDict["format_3"]["width"]
        gRawFmtTable["format_3"]["height"] = jsonDict["format_3"]["height"]
        gRawFmtTable["format_3"]["pixel_bits"] = jsonDict["format_3"]["pixel_bits"]
        gRawFmtTable["format_3"]["bayer"] = jsonDict["format_3"]["bayer"]

        gRawFmtTable["format_4"]["name"] = jsonDict["format_4"]["name"]
        gRawFmtTable["format_4"]["color"] = jsonDict["format_4"]["color"]
        gRawFmtTable["format_4"]["width"] = jsonDict["format_4"]["width"]
        gRawFmtTable["format_4"]["height"] = jsonDict["format_4"]["height"]
        gRawFmtTable["format_4"]["pixel_bits"] = jsonDict["format_4"]["pixel_bits"]
        gRawFmtTable["format_4"]["bayer"] = jsonDict["format_4"]["bayer"]

    return jsonDict

###########################################################
# MainEntry
###########################################################

if __name__ == "__main__":
    global textvarStatusBar

    winTitle = 'Raw Viewer'
    winMain = Tk()
    winMain.title(winTitle)
    #winMain.geometry('500x200')

    curRow, curCol = 0, 0
    #####################################
    # Button : Open RAW
    #####################################
    btnRaw = Button(winMain, text='Open RAW', command=cbfnButtonOpenRaw, bg='LightGreen')
    btnRaw.grid(row=curRow, column=0, pady=2)

    #####################################
    # Buttons : Platform RAW Config
    #####################################
    gRawFmtTable = {
        "showBayerColor"    : False,
        "showRawGray"       : True,
        "showRawRGB"        : False,
        "width"         : 1600,
        "height"        : 1200,
        "bits"          : 8,
        "bayer"         : 3,
    "format_1": {
            "name"          : "antOS05A20",
            "color"         : "Yellow",
            "width"         : 2560,
            "height"        : 1440,
            "pixel_bits"    : 10,
            "bayer"         : 3,
                "//a": "bayer cdoe: R=0, Gr=1, Gb=2, B=3"
        },
        "format_2": {
            "name"          : "theiaTuning",
            "color"         : "LightYellow",
            "width"         : 1600,
            "height"        : 1200,
            "pixel_bits"    : 8,
            "bayer"         : 3,
                "//a": "bayer cdoe: R=0, Gr=1, Gb=2, B=3"
        },
        "format_3": {
            "name"          : "antAR0330",
            "color"         : "SlateGray1",
            "width"         : 2304,
            "height"        : 1296,
            "pixel_bits"    : 10,
            "bayer"         : 1,
                "//a": "bayer cdoe: R=0, Gr=1, Gb=2, B=3"
        },
        "format_4": {
            "name"          : "Hawkeye",
            "color"         : "PaleGreen",
            "width"         : 1920,
            "height"        : 1080,
            "pixel_bits"    : 14,
            "bayer"         : 0,
                "//a": "bayer cdoe: R=0, Gr=1, Gb=2, B=3"
        }
    }

    raw_format_json_load()

    btnRawFmt1 = Button(winMain, text=gRawFmtTable["format_1"]["name"], command=cbfnButtonConfigAntmanOS05A20, bg="#D0D0D0")
    btnRawFmt1.grid(row=curRow, column=2, pady=2)

    btnRawFmt2 = Button(winMain, text=gRawFmtTable["format_2"]["name"], command=cbfnButtonConfigTheiaOS05A20, bg="#D0D0D0")
    btnRawFmt2.grid(row=curRow, column=3, pady=2)

    btnRawFmt3 = Button(winMain, text=gRawFmtTable["format_3"]["name"], command=cbfnButtonConfigAntmanAR0330, bg="#D0D0D0")
    btnRawFmt3.grid(row=curRow, column=4, pady=2)

    btnRawFmt4 = Button(winMain, text=gRawFmtTable["format_4"]["name"], command=cbfnButtonConfigHawkeye, bg="#D0D0D0")
    btnRawFmt4.grid(row=curRow, column=5, pady=2)

    curRow +=1
    lblRawWidth = Label(winMain, text='Width')
    lblRawWidth.grid(row=curRow, column=0, pady=2)
    txtlblRawWidth = StringVar(value=gRawFmtTable["width"])
    entryRawWidth = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawWidth)
    entryRawWidth.grid(row=curRow, column=1, sticky=W)

    curRow +=1
    lblRawHeight = Label(winMain, text='Height')
    lblRawHeight.grid(row=curRow, column=0, pady=2)
    txtlblRawHeight = StringVar(value=gRawFmtTable["height"])
    entryRawHeight = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawHeight)
    entryRawHeight.grid(row=curRow, column=1, sticky=W)


    lblRawBayer = Label(winMain, text='Bayer')
    lblRawBayer.grid(row=1, column=3, pady=2)
    bayerSelect = IntVar(value=gRawFmtTable["bayer"])
    bayer_config = [ ('R', 0, 2, 3), ('Gr', 1, 2, 4), ('Gb', 2, 3, 3), ('B', 3, 3, 4) ]
    #bayer_config = [ ('R', 0), ('Gr', 1), ('Gb', 2), ('B', 3) ]
    for bayer, val, row, col in bayer_config:
        btn = Radiobutton(winMain, text=bayer,
                    padx = 20,
                    variable=bayerSelect,
                    #command=ShowChoice,
                    value=val)
        btn.grid(row=row, column=col)
        btn.config(anchor=W, justify=LEFT, width=2)
        #print("Bayer= %s, Row= %d, Column= %d" % (bayer, row, col) )

    curRow +=1
    lblRawBits = Label(winMain, text='Pixel Bits')
    lblRawBits.grid(row=curRow, column=0, padx=2, pady=2)
    txtlblRawBits = StringVar(value=gRawFmtTable["bits"])
    entryRawBits = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawBits)
    entryRawBits.grid(row=curRow, column=1, sticky=W)

    curRow += 1
    Label(winMain, text='ShowRAW').grid(row=curRow, column=0)
    chkShowBayerImg = IntVar()
    chkShowBayerImg.set(gRawFmtTable["showBayerColor"])
    btnShowBayerImg = Checkbutton(winMain, text='BayerColors', variable=chkShowBayerImg)
    btnShowBayerImg.grid(row=curRow, column=1)

    chkShowRawImg = IntVar()
    chkShowRawImg.set(gRawFmtTable["showRawGray"])
    btnShowRawImg = Checkbutton(winMain, text='RawGray', variable=chkShowRawImg)
    btnShowRawImg.grid(row=curRow, column=2)

    chkShowRawRGB = IntVar()
    chkShowRawRGB.set(gRawFmtTable["showRawRGB"])
    btnShowRawRGB = Checkbutton(winMain, text='RawRGB', variable=chkShowRawRGB)
    btnShowRawRGB.grid(row=curRow, column=3)

    curRow += 2
    # Button : Exit
    btnExit = Button(winMain, text='-- EXIT --', command=cbfnButtonMainExit, fg='Yellow', bg='Red')
    btnExit.grid(row=curRow, column=0)

    curRow += 2
    textvarStatusBar = StringVar(value="")
    statusBar = Label(winMain, textvariable=textvarStatusBar, relief=SUNKEN, bd=2, anchor=W)
    statusBar.grid(row=curRow, column=0, columnspan=8, sticky=W+E, padx=4, pady=4)

    winMain.mainloop()
