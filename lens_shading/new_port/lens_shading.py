#!/usr/bin/python

import os, sys

from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import cv2

import numpy as np
import matplotlib.pyplot as plt
from show_shading3D import show_RGB_shading3D


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
gMaxImgShowWidth = 640

bayer2gray_code = {
    0: cv2.COLOR_BAYER_RG2GRAY,
    1: cv2.COLOR_BAYER_GR2GRAY,
    2: cv2.COLOR_BAYER_GB2GRAY,
    3: cv2.COLOR_BAYER_BG2GRAY
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
# Message Box with OK button
###########################################################
def messageBoxOK(title, msg):
    box = Toplevel()
    box.title(title)
    Label(box, text=msg).pack()
    Button(box, text='OK', command=box.destroy).pack()



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



###########################################################
# Functions : saveRawGrayImage
###########################################################

def saveRawGrayImage(rawImg, bayerCode):
    matRaw = rawImg << (16-int(txtlblRawBits.get()))

    ## Bayer2Gray
    code = bayer2gray_code.get(bayerCode, cv2.COLOR_BAYER_RG2GRAY)
    matGray = cv2.cvtColor(matRaw, code)
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
    matBGR = matBGR / 256
    matBGR = matBGR.astype(np.uint8)

    win_title = "RAW_RGB"
    if gIsShowRawImage:
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

    # print("width %d -> %d, height %d -> %d" % (imgW, simgW, imgH, simgH))

    btnRaw.config(bg='Coral')
    bitshift = rawBits-8

    imgRaw = bayerdata.reshape(imgH, imgW)
    # saveRawGrayImage(imgRaw, bayerType)

    bayerImgC1 = imgRaw[0:imgH+1:2, 0:imgW+1:2] >> bitshift
    bayerImgC2 = imgRaw[0:imgH+1:2, 1:imgW+1:2] >> bitshift
    bayerImgC3 = imgRaw[1:imgH+1:2, 0:imgW+1:2] >> bitshift
    bayerImgC4 = imgRaw[1:imgH+1:2, 1:imgW+1:2] >> bitshift

    bayerColor_LUT = [
        { 'R':bayerImgC1, 'Gr':bayerImgC2, 'Gb':bayerImgC3, 'B':bayerImgC4 }, # Bayer-R
        { 'Gr':bayerImgC1, 'R':bayerImgC2, 'B':bayerImgC3, 'Gb':bayerImgC4 }, # Bayer-Gr
        { 'Gb':bayerImgC1, 'B':bayerImgC2, 'R':bayerImgC3, 'Gr':bayerImgC4 }, # Bayer-Gb
        { 'B':bayerImgC1, 'Gb':bayerImgC2, 'Gr':bayerImgC3, 'R':bayerImgC4 } # Bayer-B
    ]

    h, w = bayerImgC1.shape
    dictBayerImg = bayerColor_LUT[bayerType]
    imR = dictBayerImg.get('R')
    imG = dictBayerImg.get('Gr')
    imB =  dictBayerImg.get('B')
    show_RGB_shading3D(w, h, image_R=imR, image_G=imG, image_B=imB)

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
        splitBayerRawU16(rawdata, int(txtlblRawWidth.get()),
                        int(txtlblRawHeight.get()),
                        int(txtlblRawBits.get()),
                        bayerSelect.get())
    except:
        cbfnButtonReset()
        return

###########################################################
# Button Function : OpenRAW
###########################################################
def cbfnButtonOpenRaw():
    global winMain, winTitle, txtlblRawFName, btnRaw, btn
    global rawdata, rawfname, gRawBaseName
    global gIsShowBayerImage, chkShowBayerImg, gIsShowRawImage, chkShowRawImg

    rawfname = filedialog.askopenfilename()

    #print(rawfname)
    try:
        # f = open(rawfname, 'rb')
        # rawdata = f.read()
        # f.close()
        rawdata = np.fromfile(rawfname, dtype=np.uint16)
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
# MainEntry
###########################################################

if __name__ == "__main__":

    winTitle = 'Shading Viewer'
    winMain = Tk()
    winMain.title(winTitle)
    winMain.geometry('400x200')

    curRow, curCol = 0, 0
    # Button : Open RAW
    btnRaw = Button(winMain, text='Open RAW', command=cbfnButtonOpenRaw, bg='LightGreen')
    btnRaw.grid(row=curRow, column=curCol, pady=2)

    curRow +=1
    lblRawWidth = Label(winMain, text='Width')
    lblRawWidth.grid(row=curRow, column=0, pady=2)
    txtlblRawWidth = StringVar(value='2304')
    entryRawWidth = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawWidth)
    entryRawWidth.grid(row=curRow, column=1, sticky=W)

    curRow +=1
    lblRawHeight = Label(winMain, text='Height')
    lblRawHeight.grid(row=curRow, column=0, pady=2)
    txtlblRawHeight = StringVar(value='1296')
    entryRawHeight = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawHeight)
    entryRawHeight.grid(row=curRow, column=1, sticky=W)


    lblRawBayer = Label(winMain, text='Bayer')
    lblRawBayer.grid(row=1, column=3, pady=2)
    bayerSelect = IntVar(value=1)
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
    txtlblRawBits = StringVar(value='10')
    entryRawBits = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawBits)
    entryRawBits.grid(row=curRow, column=1, sticky=W)

    curRow += 1
    Label(winMain, text='ShowRAW').grid(row=curRow, column=0)
    chkShowBayerImg = IntVar()
    chkShowBayerImg.set(0)
    btnShowBayerImg = Checkbutton(winMain, text='BayerColors', variable=chkShowBayerImg)
    btnShowBayerImg.grid(row=curRow, column=1)

    chkShowRawImg = IntVar()
    chkShowRawImg.set(1)
    btnShowRawImg = Checkbutton(winMain, text='RawGray', variable=chkShowRawImg)
    btnShowRawImg.grid(row=curRow, column=2)

    curRow += 2
    # Button : Exit
    btnExit = Button(winMain, text='-- EXIT --', command=cbfnButtonMainExit, fg='Yellow', bg='Red')
    btnExit.grid(row=curRow, column=0)


    winMain.mainloop()

