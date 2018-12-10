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
    0: cv2.COLOR_BAYER_RG2BGR,
    1: cv2.COLOR_BAYER_GR2BGR,
    2: cv2.COLOR_BAYER_GB2BGR,
    3: cv2.COLOR_BAYER_BG2BGR
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
# Function : Callback of Button RESET
###########################################################
def cbfnButtonReset():
    cv2.destroyAllWindows()
    btnSelectIMG.config(text='Open RAW', command=cbfnButton_SelectIMG, bg='LightGreen')


###########################################################
# Button Function : SelectIMG
###########################################################
def cbfn_Update():
    global scl_windowSize, scl_fieldDiag, scl_fieldHV
    global var_chkLuma, var_chkChroma

    global var_chkHori, var_chkVert

    # -- 
    if 1==var_chkHori.get() or 1==var_chkVert.get():
        print("I am here: True")
        scl_fieldHV.config(state= NORMAL)
    else:
        print("I am here: False")
        scl_fieldHV.config(state= DISABLED)

    print("callBack: Update")


###########################################################
# Button Function : SelectIMG
###########################################################
def cbfnButton_SelectIMG():
    '''
    global winRoot, winTitle, txtlblRawFName, btnSelectIMG, btn
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
    winRoot.title(winTitle+ ' -- ' + baseName)

    #btnSelectIMG.config(text='Load RAW', command=cbfnButtonLoadRaw, bg='Yellow')
    gIsShowBayerImage = chkShowBayerImg.get()
    gIsShowRawImage = chkShowRawImg.get()

    # to Load and Parse RAW images
    cbfnButtonLoadRaw()
    '''
    print("Button: SelectIMG")

    return

 
###########################################################
# Button Function : Exit Main Window
###########################################################
def cbfnButtonMainExit():
    cv2.destroyAllWindows()
    winRoot.destroy()
    return



###########################################################
# MainEntry 
###########################################################

if __name__ == "__main__":

    winTitle = 'Shading Test'
    winRoot = Tk()
    winRoot.title(winTitle)
    winRoot.geometry('400x300')

    # -- Create Top/Mid/Buttom frames
    frame_padx = 2
    frame_pady = 2
    frmTop = Frame(winRoot)
    frmTop.pack(fill=X, padx=frame_padx, pady=frame_pady)
    
    frmMid1 = Frame(winRoot)
    frmMid1.pack(fill=X, padx=frame_padx, pady=frame_pady)

    frmMid2 = Frame(winRoot)
    frmMid2.pack(fill=X, padx=frame_padx, pady=frame_pady)

    # frmButtom = Frame(winRoot)
    # frmButtom.pack(fill=X, padx=frame_padx, pady=frame_pady)

    #------------------------------------
    # Frame Top
    #------------------------------------
    # -- Button : SelectIMG
    btnSelectIMG = Button(frmTop, text='Select Image', command=cbfnButton_SelectIMG, bg='LightGreen')
    btnSelectIMG.pack(fill=X)

    #------------------------------------
    # Frame Mid1
    #------------------------------------
    var_chkLuma = IntVar(value=1)
    chkbtn_Luma = Checkbutton(frmMid1, text='Luma')
    chkbtn_Luma.pack(side=LEFT)
    
    var_chkChroma = IntVar(value=1)
    chkbtn_Chroma = Checkbutton(frmMid1, text='Chroma')
    chkbtn_Chroma.pack(side=LEFT)

    def cbfnScale_WinSize(val):
        cbfn_Update()
        return
    scl_windowSize = Scale(frmMid1, label="Window Size (%): ", orient=HORIZONTAL, from_=0, to=20, resolution=1, command=cbfnScale_WinSize)
    scl_windowSize.pack(expand=True, side=RIGHT, fill=X, padx=16)
    scl_windowSize.set(10)

    #------------------------------------
    # Frame Mid2
    #------------------------------------
    frmMidLeft = Frame(frmMid2, bg='Red')
    frmMidLeft.pack(expand=True, fill=X, side=LEFT)
    frmMidRight = Frame(frmMid2, bg='Yellow')
    frmMidRight.pack(side=LEFT, padx=24)

    
    # -- Frame: MidLeft
    lbl_t = Label(frmMidLeft, anchor=W, text="Image Field:").pack(expand=True, fill=X)

    def cbfnScale_DiagImgField(val):
        cbfn_Update()
        return
    scl_fieldDiag = Scale(frmMidLeft, label='Diagnal: ', orient=HORIZONTAL, from_=0.0, to=1.0, resolution=0.05, command=cbfnScale_DiagImgField)
    scl_fieldDiag.pack(expand=True, fill=X)
    scl_fieldDiag.set(0.7)

    def cbfnScale_HvImgField(val):
        cbfn_Update()
        return
    scl_fieldHV = Scale(frmMidLeft, label='H/V: ', orient=HORIZONTAL, from_=0.0, to=1.0, resolution=0.05, command=cbfnScale_HvImgField)
    scl_fieldHV.pack(expand=True, fill=X)
    scl_fieldHV.set(0.7)

    # -- Frame: MidRight
    var_chkHori = IntVar(value=0)
    chkbtn_Hori = Checkbutton(frmMidRight, anchor=W, variable=var_chkHori, text='Horizontal', command=cbfn_Update)
    chkbtn_Hori.pack(side=TOP, expand=True, fill=X)
    
    var_chkVert = IntVar(value=0)
    chkbtn_Vert = Checkbutton(frmMidRight, anchor=W, variable=var_chkVert, text='Vertical', command=cbfn_Update)
    chkbtn_Vert.pack(side=TOP, expand=True, fill=X)


    cbfn_Update()

    winRoot.mainloop()

