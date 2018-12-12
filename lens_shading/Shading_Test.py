#!/usr/bin/python

import os, sys
import _thread
import time

from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import cv2

import numpy as np
# import matplotlib.pyplot as plt
# from show_shading3D import show_RGB_shading3D

import image_ROI as ROI

'''
from tkFileDialog import askopenfilename

That code would have worked fine in Python 2.x, but it is no longer valid.
In Python 3.x, tkFileDialog was renamed to filedialog.
'''

gOpenFileName=''
gSrcImgName=''
gSrcImgDir=''
gSrcImgBase=''
gSrcImgExt=''
gIsImgOpened=False



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
# Function: Create shadingRect list
###########################################################
def calculate_shading_globals(matWC):
    global gImgH, gImgW, gImgXc, gImgYc
    global gRoiW, gRoiH

    gImgH = matWC.shape[0]
    gImgW = matWC.shape[1]
    gImgXc = int(gImgW / 2)
    gImgYc = int(gImgH / 2)
    print('image WxH = ', gImgW, '*', gImgH, " (Xc, Yc)= ", (gImgXc, gImgYc))

    wsize_ratio = scl_windowSize.get() / 100
    gRoiW = int(gImgW * wsize_ratio)
    gRoiH = int(gImgH * wsize_ratio)


def set_QHV_rect(rect_name, Po, Pv, fraction):
    x, y = ROI.interpolateXY(Po, Pv, fraction)
    print(rect_name, ": Po= ", Po, " Pv= ", Pv, " P= ", (x, y))
    rect = gShadingRECT.new_rect(rect_name)
    rect.set_center(x, y)
    rect.set_size(gRoiW, gRoiH)
    gShadingRECT.add(rect_name, rect)

def create_shadingRECT(nw, img):
    global gImgH, gImgW, gImgXc, gImgYc
    global gRoiW, gRoiH
    global gShadingRECT

    #-- Center: C0
    rect_name='C0'
    rect = gShadingRECT.new_rect(rect_name)
    rect.set_center(gImgXc, gImgYc)
    rect.set_size(gRoiW, gRoiH)
    gShadingRECT.add(rect_name, rect)

    #-- Quadrants: Q1, Q2, Q3, Q4
    fraction = scl_fieldDiag.get()
    Po = (gImgXc, gImgYc)
    Q1param = { 'name':'Q1', 'Pv':(gImgW, 0) }
    Q2param = { 'name':'Q2', 'Pv':(0, 0) }
    Q3param = { 'name':'Q3', 'Pv':(0, gImgH) }
    Q4param = { 'name':'Q4', 'Pv':(gImgW, gImgH) }
    Qplist = [ Q1param, Q2param, Q3param, Q4param ]
    for Qp in Qplist:
        set_QHV_rect(Qp['name'], Po, Qp['Pv'], fraction)

    #-- Latitude (Horizontal): Hr(right), Hl(left)
    fraction = scl_fieldHV.get()
    Hrparam = { 'name':'Hr', 'Pv':(gImgW, int(gImgH/2)) }
    Hlparam = { 'name':'Hl', 'Pv':(0, int(gImgH/2)) }
    Hplist = [ Hrparam, Hlparam ]
    for Hp in Hplist:
        set_QHV_rect(Hp['name'], Po, Hp['Pv'], fraction)

    #-- Longitude (Vertical): Vt(top), Vb(bottom)
    fraction = scl_fieldHV.get()
    Vtparam = { 'name':'Vt', 'Pv':(int(gImgW/2), 0) }
    Vbparam = { 'name':'Vb', 'Pv':(int(gImgW/2), gImgH) }
    Vplist = [ Vtparam, Vbparam ]
    for Vp in Vplist:
        set_QHV_rect(Vp['name'], Po, Vp['Pv'], fraction)



###########################################################
# Function : cbfn_Update()
###########################################################
def cbfn_Update():
    global scl_windowSize, scl_fieldDiag, scl_fieldHV
    global var_chkLuma, var_chkChroma
    global var_chkHori, var_chkVert

    if 1==var_chkHori.get() or 1==var_chkVert.get():
        scl_fieldHV.config(state= NORMAL)
    else:
        scl_fieldHV.config(state= DISABLED)

    #print("callBack: Update")
    return


###########################################################
# Button Function : SelectIMG
###########################################################
def cbfnButton_SelectIMG():
    global gOpenFileName, gSrcImgName, gSrcImgDir, gSrcImgBase, gSrcImgExt
    global gImgH, gImgW, gImgXc, gImgYc
    global gRoiW, gRoiH

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
        matImg = cv2.imread(gOpenFileName, cv2.IMREAD_UNCHANGED)
        cv2.namedWindow(gSrcImgName, cv2.WINDOW_NORMAL)
        # cv2.imshow(gSrcImgName, matImg)
    except:
        messageBoxOK('FileIO', 'CV2 failed to load image file :\n' + gOpenFileName)
        cbfnButtonReset()
        return

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
    global gShadingRECT
    matWorkCopy = matImg.copy()
    gShadingRECT  = ROI.ImageROI(gSrcImgName, matWorkCopy)
    calculate_shading_globals(matWorkCopy)
    create_shadingRECT(gSrcImgName, matWorkCopy)

    gShadingRECT.show()
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


if __name__ == "__main__":
    main()
