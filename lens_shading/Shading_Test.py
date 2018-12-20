#!/usr/bin/python

import os, sys
import _thread
import time

import numpy as np
import cv2


# import matplotlib.pyplot as plt
# from show_shading3D import show_RGB_shading3D

import image_Shading as IS
import cy_CvOSD as OSD
import cy_debug as DP



gOpenFileName=''
gSrcImgName=''
gSrcImgDir=''
gSrcImgBase=''
gSrcImgExt=''
gIsImgOpened=False


color_pass = (0, 255, 0)
color_ng = (0, 0, 255)
lwidth = 2


###########################################################
# Function : cbfn_Update()
###########################################################

def test_shading(cv_img, rect_list, spec):
    """
    spec: list
        [centerY, lumaSpecRatioMin, lumaSpecDev, colorSpecDev, chkLuma, chkColor]
    """
    maxRect, minRect = [ '' for _ in range(2)]
    maxY = minY = 0
    rectY = []
    for k in rect_list:
        rect = gShadingINFO[k]
        # Vt = rect.get('Vt')
        # Vb = rect.get('Vb')
        _Y = rect['Y']
        rectY.append(_Y)
        if _Y > maxY:
            maxY = _Y
            maxRect = k
        elif _Y < minY:
            minY = _Y
            minRect = k
        else:
            pass
    meanRectY = sum(rectY)/len(rectY)

    centerY, specLumaMin, specLumaDev, specColorDev, chkLuma, chkColor = spec
    dprint.info('SPEC: ', spec)
    for k in rect_list:
        rect = gShadingINFO[k]
        Vt = rect.get('Vt')
        Vb = rect.get('Vb')
        _Y, _R, _G, _B = [rect[x] for x in ['Y', 'R', 'G', 'B']]
        dprint.info(k, ': ', _Y, ', ', _R, ', ', _G, ', ', _B)
        yC2C = _Y/centerY
        yDev = _Y/meanRectY
        r2g = _R/_G
        b2g = _B/_G

        dprint.info(yC2C, ' ', yDev, ' ', r2g, ' ', b2g)
        is_pass = True
        yDev_pass = True
        chroma_pass = True
        if chkLuma:
            #--- Luma C2C (corner to center)
            if yC2C > 1.0 or yC2C < specLumaMin/100.0:
                is_pass = False
            #--- Luma corner to cornerMean deviation
            if yDev > (100+specLumaDev)/100.0 or yDev < (100-specLumaDev)/100.0:
                # is_pass = False
                yDev_pass = False

        if chkColor:
            #--- R/G deviation
            if abs(r2g-1.0) > specColorDev/100.0:
                chroma_pass = False
            #--- B/G deviation
            if abs(b2g-1.0) > specColorDev/100.0:
                chroma_pass = False

        if is_pass:
            color = color_pass
        else:
            color = color_ng

        if chkLuma or chkColor:
            cv2.rectangle(cv_img, Vt, Vb, color, lwidth)
            dprint.info(k, ': ', is_pass, yDev_pass)
            if not yDev_pass:
                dprint.info(k, ': yDev failed !!')
                cv2.line(cv_img, Vt, Vb, color_ng, lwidth)
            if not chroma_pass:
                dprint.info(k, ': color failed !!')
                p0=(Vb[0], Vt[1])
                p1=(Vt[0], Vb[1])
                cv2.line(cv_img, p0, p1, (0,255,255), lwidth)

        #--- OSD
        osd = OSD.osdText()
        text = "%d, %.2f, %.2f" % (_Y, yC2C, yDev)
        w, h, pads = osd.get_textSize(text)
        osd.show(cv_img, text, Vt[0], Vt[1])
        text = "%.2f, %.2f" % (r2g, b2g)
        osd.show(cv_img, text, Vt[0], Vt[1]+(h+pads*2))


def test_all_shadings(cv_win, cv_img):
    """
    """
    global gShadingINFO
    global var_LumaSpecE2C, var_LumaSpecM2m, var_ColorDev
    global var_chkLuma, var_chkChroma, var_chkHori, var_chkVert

    lumaSpecC2C = var_LumaSpecE2C.get()
    lumaSpecDev = var_LumaSpecM2m.get()
    colorSpecDev = var_ColorDev.get()
    isChkLuma = var_chkLuma.get()
    isChkColor = var_chkChroma.get()
    isChkHorizontal = var_chkHori.get()
    isChkVertical = var_chkVert.get()

    centerY = gShadingINFO['Co'].get('Y')
    spec = [centerY, lumaSpecC2C, lumaSpecDev, colorSpecDev, isChkLuma, isChkColor]
    #-------------------------
    # Diagonal: Q1/Q2/Q3/Q4
    #-------------------------
    #dprint.set_level(DP.DEBUG_INFO)
    test_shading(cv_img, ['Q1', 'Q2', 'Q3', 'Q4'], spec)
    #dprint.set_level(DP.DEBUG_ERROR)

    #-------------------------
    # Horizontal: Hr, Hl
    #-------------------------
    if isChkHorizontal:
        test_shading(cv_img, ['Hr', 'Hl'], spec)

    #-------------------------
    # Horizontal: Vt, Vb
    #-------------------------
    if isChkVertical:
        test_shading(cv_img, ['Vb', 'Vt'], spec)

    #--- Display
    cv2.imshow(cv_win, cv_img)





###########################################################
# Function : cbfn_Update()
###########################################################
def cbfn_Update():
    global scl_windowSize, scl_fieldDiag, scl_fieldHV
    global var_chkLuma, var_chkChroma
    global var_chkHori, var_chkVert
    global gIsImgOpened

    if not gIsImgOpened:
        dprint.warning('image not opened yet!!')
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
    global gShadingINFO
    gShadingINFO = gImageShading.update(gImgWC)

    #gImageShading.show(gSrcImgName, gImgWC)
    test_all_shadings(gSrcImgName, gImgWC)

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

dprint = DP.DebugPrint('ShadingTEST')

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
    frmM11 = Frame(frmMid1)
    frmM11.pack(fill=X, padx=frame_padx, pady=frame_pady)
    var_chkLuma = IntVar(value=1)
    chkbtn_Luma = Checkbutton(frmM11, variable=var_chkLuma, text='Luma', command=cbfn_Update)
    chkbtn_Luma.pack(side=LEFT)

    global var_LumaSpecE2C, var_LumaSpecM2m
    Label(frmM11, anchor=W, text="Corner/Center, %").pack(side=LEFT, padx=8)
    var_LumaSpecE2C = IntVar(value=85)
    entry_LumaSpecE2C = Entry(frmM11, textvariable=var_LumaSpecE2C, validate="focusout", validatecommand=cbfn_Update, width=5)   #-- ratio of Edge(corner) to Center
    entry_LumaSpecE2C.pack(side=LEFT)

    Label(frmM11, anchor=W, text="Corner Deviation, %").pack(side=LEFT, padx=8)
    var_LumaSpecM2m = IntVar(value=10)
    entry_LumaSpecM2m = Entry(frmM11, textvariable=var_LumaSpecM2m, validate="focusout", validatecommand=cbfn_Update, width=5)   #-- Avg(edge) +/- M2m %
    entry_LumaSpecM2m.pack(side=LEFT)


    frmM12 = Frame(frmMid1)
    frmM12.pack(fill=X, padx=frame_padx, pady=frame_pady)
    var_chkChroma = IntVar(value=1)
    chkbtn_Chroma = Checkbutton(frmM12, variable=var_chkChroma, text='Chroma', command=cbfn_Update)
    chkbtn_Chroma.pack(side=LEFT)

    global var_ColorDev
    Label(frmM12, anchor=W, text="Color Deviation, %").pack(side=LEFT, padx=8)
    var_ColorDev = IntVar(value=10)
    entry_ColorDev = Entry(frmM12, textvariable=var_ColorDev, validate="focusout", validatecommand=cbfn_Update, width=5)   #-- Avg(edge) +/- M2m %
    entry_ColorDev.pack(side=LEFT)


    frmM13 = Frame(frmMid1)
    frmM13.pack(fill=X, padx=frame_padx, pady=frame_pady)
    def cbfnScale_WinSize(val):
        cbfn_Update()
        return
    scl_windowSize = Scale(frmM13, label="Window Size (ratio): ", orient=HORIZONTAL, from_=0.02, to=0.2, resolution=0.01, command=cbfnScale_WinSize)
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
