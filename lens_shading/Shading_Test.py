#!/usr/bin/python

import os, sys
import _thread
import time

import numpy as np
import cv2


# import matplotlib.pyplot as plt
# from show_shading3D import show_RGB_shading3D

#import image_ROI as ROI
import image_Shading as IS



gOpenFileName=''
gSrcImgName=''
gSrcImgDir=''
gSrcImgBase=''
gSrcImgExt=''
gIsImgOpened=False




###########################################################
# Function : cbfn_Update()
###########################################################
def cbfn_Update():
    global scl_windowSize, scl_fieldDiag, scl_fieldHV
    global var_chkLuma, var_chkChroma
    global var_chkHori, var_chkVert
    global gIsImgOpened

    if not gIsImgOpened:
        print('Error: image not opened yet!!')
        return

    gImageShading.set_property(h_enable=False)
    gImageShading.set_property(v_enable=False)
    if 1==var_chkHori.get() or 1==var_chkVert.get():
        scl_fieldHV.config(state= NORMAL)
        if 1==var_chkHori.get():
            gImageShading.set_property(h_enable=True)
        if 1==var_chkVert.get():
            gImageShading.set_property(v_enable=True)
    else:
        scl_fieldHV.config(state= DISABLED)

    if 1==var_chkLuma.get():
        gImageShading.set_property(luma_enable=True)
    else:
        gImageShading.set_property(luma_enable=False)

    if 1==var_chkChroma.get():
        gImageShading.set_property(chroma_enable=True)
    else:
        gImageShading.set_property(chroma_enable=False)

    #-- Update center rectangle size
    gImageShading.set_property(c_size_ratio=scl_windowSize.get())
    gImageShading.set_property(e_size_ratio=scl_windowSize.get())
    gImageShading.set_property(d_field=scl_fieldDiag.get())
    gImageShading.set_property(hv_field=scl_fieldHV.get())

    gImgWC = gImgSrc.copy()
    gImageShading.update(gImgWC)

    gImageShading.show(gSrcImgName, gImgWC)

    return



###########################################################
# Message Box with OK button
###########################################################
def messageBoxOK(title, msg):
    box = Toplevel()
    box.title(title)
    Label(box, text=msg).pack()
    Button(box, text='OK', command=box.destroy).pack()


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
# Function : Callback of Button RESET
###########################################################
def cbfnButtonReset():
    cv2.destroyAllWindows()
    btnSelectIMG.config(text='Select Image', command=cbfnButton_SelectIMG, bg='LightGreen')


###########################################################
# Button Function : SelectIMG
###########################################################
def cbfnButton_SelectIMG():
    global gOpenFileName, gSrcImgName, gSrcImgDir, gSrcImgBase, gSrcImgExt
    global gImgH, gImgW, gImgXc, gImgYc
    global gRoiW, gRoiH
    global gShadingRECT
    global gImgWC, gImgSrc

    gOpenFileName = filedialog.askopenfilename()

    #gSrcImgDir, gSrcImgBase, gSrcImgExt = parse_file_path(gOpenFileName)
    try:
        # f = open(gOpenFileName, 'rb')
        # rawdata = f.read()
        # f.close()
        # rawdata = np.fromfile(gOpenFileName, dtype=np.uint16)
        gSrcImgDir, gSrcImgBase, gSrcImgExt = parse_file_path(gOpenFileName)
    except:
        messageBoxOK('FileIO', 'Failed to open file :\n' + gOpenFileName)
        cbfnButtonReset()
        return

    # -- modify title of main window, change button to RESET
    gSrcImgName = gSrcImgBase + gSrcImgExt
    winRoot.title(winTitle+ ' -- ' + gSrcImgName)
    btnSelectIMG.config(text='RESET', command=cbfnButtonReset, bg='Yellow')

    # -- Open and show image with CV2
    os.chdir(gSrcImgDir)
    # matImg = cv2.imread(gSrcImgName)
    # print(matImg.shape)
    try:
        gImgSrc = cv2.imread(gOpenFileName)
        print('Image Size: ', gImgSrc.shape[1], '*', gImgSrc.shape[0])
        cv2.namedWindow(gSrcImgName, cv2.WINDOW_NORMAL)
    except:
        messageBoxOK('FileIO', 'CV2 failed to load image file :\n' + gOpenFileName)
        cbfnButtonReset()
        return

    #-- resize window to 720p in image height
    resizeH = 480
    if gImgSrc.shape[1] > resizeH:
        w = int(resizeH*gImgSrc.shape[1]/gImgSrc.shape[0])
        h = resizeH
        cv2.resizeWindow(gSrcImgName, w, h)
        print('Output window resized to: ', w, '*', h)
        # cv2.imshow(gSrcImgName, gImgSrc)

    # -- Now, create a thread to watch the status of the window
    def PROC_check_window_status(namedWin, slp_time):
        while True:
            if cv2.getWindowProperty(namedWin, 1) < 0:
                cbfnButtonReset()
                break
            time.sleep(slp_time)

    try:
        _thread.start_new_thread(PROC_check_window_status, (gSrcImgName, 0.2))
    except:
        print("Error, failed to create new thread to watch named window: ", gSrcImgName)
        return


    #-------------------------------------------
    # Create shading Rectangles
    #-------------------------------------------
    global gIsImgOpened
    gIsImgOpened = True

    global gImageShading
    gImageShading = IS.ImageShading(gImgSrc.shape[1], gImgSrc.shape[0])
    cbfn_Update()
    return


###########################################################
# Button Function : Exit Main Window
###########################################################
def cbfnButtonMainExit():
    global winRoot

    cv2.destroyAllWindows()
    winRoot.destroy()




###########################################################
# MainEntry
###########################################################

from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog

def main():
    global winTitle, winRoot
    global scl_windowSize, scl_fieldDiag, scl_fieldHV
    global var_chkLuma, var_chkChroma
    global var_chkHori, var_chkVert
    global gOpenFileName, gSrcImgName, gSrcImgDir, gSrcImgBase, gSrcImgExt
    global btnSelectIMG

    winTitle = 'Shading Test'
    winRoot = Tk()
    winRoot.title(winTitle)
    winRoot.geometry('400x300+150+100')

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
    chkbtn_Luma = Checkbutton(frmMid1, variable=var_chkLuma, text='Luma', command=cbfn_Update)
    chkbtn_Luma.pack(side=LEFT)

    var_chkChroma = IntVar(value=1)
    chkbtn_Chroma = Checkbutton(frmMid1, variable=var_chkChroma, text='Chroma', command=cbfn_Update)
    chkbtn_Chroma.pack(side=LEFT)

    def cbfnScale_WinSize(val):
        cbfn_Update()
        return
    scl_windowSize = Scale(frmMid1, label="Window Size (ratio): ", orient=HORIZONTAL, from_=0.02, to=0.2, resolution=0.01, command=cbfnScale_WinSize)
    scl_windowSize.pack(expand=True, side=RIGHT, fill=X, padx=16)
    scl_windowSize.set(0.1)

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
    scl_fieldDiag = Scale(frmMidLeft, label='Diagnal: ', orient=HORIZONTAL, from_=0.1, to=1.0, resolution=0.05, command=cbfnScale_DiagImgField)
    scl_fieldDiag.pack(expand=True, fill=X)
    scl_fieldDiag.set(1.0)

    def cbfnScale_HvImgField(val):
        cbfn_Update()
        return
    scl_fieldHV = Scale(frmMidLeft, label='H/V: ', orient=HORIZONTAL, from_=0.1, to=1.0, resolution=0.05, command=cbfnScale_HvImgField)
    scl_fieldHV.pack(expand=True, fill=X)
    scl_fieldHV.set(1.0)

    # -- Frame: MidRight
    var_chkHori = IntVar(value=0)
    chkbtn_Hori = Checkbutton(frmMidRight, anchor=W, variable=var_chkHori, text='Horizontal', command=cbfn_Update)
    chkbtn_Hori.pack(side=TOP, expand=True, fill=X)

    var_chkVert = IntVar(value=0)
    chkbtn_Vert = Checkbutton(frmMidRight, anchor=W, variable=var_chkVert, text='Vertical', command=cbfn_Update)
    chkbtn_Vert.pack(side=TOP, expand=True, fill=X)

    winRoot.mainloop()


if __name__ == "__main__":
    main()
