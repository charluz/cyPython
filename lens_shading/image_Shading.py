#!/usr/bin/python

import os, sys
import _thread
import time

import numpy as np
import cv2


# import matplotlib.pyplot as plt
# from show_shading3D import show_RGB_shading3D

import image_ROI as ROI



gOpenFileName=''
gSrcImgName=''
gSrcImgDir=''
gSrcImgBase=''
gSrcImgExt=''
gIsImgOpened=False



#--------------------------------------
# Class: roiRect
#--------------------------------------
class ImageShading():
    """A class to define the Luma/Chroma shading operation of an given image.

    Attributes
    --------------
    gShadingINFO: dict
        A dictionary acting as a list to store information of each shading rectangle.
        The shading rectangles have been named as:
        * Co: the center rectangle
        * Q1/Q2/Q3/Q3: the diagonal rectangles, where Q1 represents the 1st quadrant.
        * Hr/Hl: the horizontal rectangles, where Hr:right, Hl:left
        * Vt/Vb: the vertical rectangles, where Vt:top, Vb:bottom
        The format of gShadingINFO is defined:
            { nameID:gShadingRect, }
    Methods
    ---------------
    set_property()
    """
    def __init__(self, imgW, imgH):
        """Initialize all shading rectangles

        Arguments
        ------------
        imgW, imgH: integer
            the size of the source image

        Returns
        --------------
        None
        """
        self._property = {
            'c_size_ratio'      : 0.1,
            'e_size_ratio'      : 0.1,
            'd_field'           : 1.0,
            'hv_field'          : 1.0,
        }
        #-- store global variables
        self.gImgW = imgW
        self.gImgH = imgH
        self.gShadingINFO = {}

        #-- derive image center coordinate
        self.gImgXc = int(imgW / 2)
        self.gImgYc = int(imgH / 2)
        self.gCRoiW = int(imgW * self._property['c_size_ratio'])
        self.gCRoiH = int(imgH * self._property['c_size_ratio'])
        self.gERoiW = int(imgW * self._property['e_size_ratio'])
        self.gERoiH = int(imgH * self._property['e_size_ratio'])
        #-- create the ROI list
        self.gShadingRECT  = ROI.ImageROI(imgW, imgH)

        self._create_shading_rectangles()


    def set_property(self, **kwargs):
        """Set properities of the image shading.

        The property is specified with the format: propt_name=value
        For example, c_size=0.1

        Arguments
        --------------
        c_size_ratio: float
            * the value is specified as the proportional value of the center rectangle to the image
            * value = (width/height of the center rectangle) / (width/height of the image)
            * ranges from 0.05 to 0.3 (5% to 30%)
        e_size_ratio: float
            * the proportional value of the edge (diagonal, top/bottom, left/right) rectangle to the image
            * reanges from 0.05 to 0.2 (5% to 20%)
        d_field: float
            * the image field of the diagonal rectangles
            * ranges from 0.3 to 1.0
        hv_field: float
            * the image field of the horizontal/vertical rectangles
            * ranges from 0.3 to 1.0
        """
        for argkey, argval in kwargs.items():
            #print(argkey, '= ', argval)
            if argkey == 'c_size_ratio':
                self._property[argkey] = argval   # size proportional value of center rectangle to source image
            elif argkey == 'e_size_ratio':
                self._property[argkey] = argval   # size proportional value of corner rectangles to source image
            elif argkey == 'd_field':
                self._property[argkey] = argval   # the image field ratio of the diagonal rectangles to the center's
            elif argkey == 'hv_field':
                self._property[argkey] = argval   # the image field ratio of the H/V rectangles to the center's
            else:
                pass


    def _set_QHV_rect(self, rect_name, Po, Pv, fraction):
        """
        """
        x, y = ROI.interpolateXY(Po, Pv, fraction)
        #print(rect_name, ": Po= ", Po, " Pv= ", Pv, " P= ", (x, y))
        self.gShadingRECT.add(rect_name, (x, y), (self.gERoiW, self.gERoiH))


    def _create_shading_rectangles(self):
        """To initialize all shadning rectangles
        """
        #-- Center: Co
        rect_name='Co'
        self.gShadingRECT.add(rect_name, (self.gImgXc, self.gImgYc), (self.gCRoiW, self.gCRoiH))

        Po = (self.gImgXc, self.gImgYc)

        #-- Quadrants: Q1, Q2, Q3, Q4
        fraction = self._property['d_field']
        Q1param = { 'name':'Q1', 'Pv':(self.gImgW, 0) }
        Q2param = { 'name':'Q2', 'Pv':(0, 0) }
        Q3param = { 'name':'Q3', 'Pv':(0, self.gImgH) }
        Q4param = { 'name':'Q4', 'Pv':(self.gImgW, self.gImgH) }
        Qplist = [ Q1param, Q2param, Q3param, Q4param ]
        for Qp in Qplist:
            self._set_QHV_rect(Qp['name'], Po, Qp['Pv'], fraction)

        #-- Latitude (Horizontal): Hr(right), Hl(left)
        fraction = self._property['hv_field']
        Hrparam = { 'name':'Hr', 'Pv':(self.gImgW, int(self.gImgH/2)) }
        Hlparam = { 'name':'Hl', 'Pv':(0, int(self.gImgH/2)) }
        Hplist = [ Hrparam, Hlparam ]
        for Hp in Hplist:
            self._set_QHV_rect(Hp['name'], Po, Hp['Pv'], fraction)

        #-- Longitude (Vertical): Vt(top), Vb(bottom)
        Vtparam = { 'name':'Vt', 'Pv':(int(self.gImgW/2), 0) }
        Vbparam = { 'name':'Vb', 'Pv':(int(self.gImgW/2), self.gImgH) }
        Vplist = [ Vtparam, Vbparam ]
        for Vp in Vplist:
            self._set_QHV_rect(Vp['name'], Po, Vp['Pv'], fraction)


    def _update_QHV_rect(self, rect_name, Po, Pv, fraction):
        """
        """
        x, y = ROI.interpolateXY(Po, Pv, fraction)
        #print(rect_name, ": Po= ", Po, " Pv= ", Pv, " P= ", (x, y))
        self.gShadingRECT.set_center(rect_name, x, y)
        self.gShadingRECT.set_size(rect_name, self.gERoiW, self.gERoiH)


    def _update_all_rectangles(self):
        """To update vertexes of all shading rectangles
        """
        rect_name='Co'
        #self.gShadingRECT.set_center(rect_name, self.gImgXc, self.gImgYc)
        self.gCRoiW = int(self.gImgW * self._property['c_size_ratio'])
        self.gCRoiH = int(self.gImgH * self._property['c_size_ratio'])
        self.gShadingRECT.set_size(rect_name, self.gCRoiW, self.gCRoiH)

        Po = (self.gImgXc, self.gImgYc)

        self.gERoiW = int(self.gImgW * self._property['e_size_ratio'])
        self.gERoiH = int(self.gImgH * self._property['e_size_ratio'])

        #-- Quadrants: Q1, Q2, Q3, Q4
        fraction = self._property['d_field']
        Q1param = { 'name':'Q1', 'Pv':(self.gImgW, 0) }
        Q2param = { 'name':'Q2', 'Pv':(0, 0) }
        Q3param = { 'name':'Q3', 'Pv':(0, self.gImgH) }
        Q4param = { 'name':'Q4', 'Pv':(self.gImgW, self.gImgH) }
        Qplist = [ Q1param, Q2param, Q3param, Q4param ]
        for Qp in Qplist:
            rect_name = Qp['name']
            self._update_QHV_rect(rect_name, Po, Qp['Pv'], fraction)

        #-- Latitude (Horizontal): Hr(right), Hl(left)
        fraction = self._property['hv_field']
        Hrparam = { 'name':'Hr', 'Pv':(self.gImgW, int(self.gImgH/2)) }
        Hlparam = { 'name':'Hl', 'Pv':(0, int(self.gImgH/2)) }
        Hplist = [ Hrparam, Hlparam ]
        for Hp in Hplist:
            rect_name = Hp['name']
            self._update_QHV_rect(rect_name, Po, Hp['Pv'], fraction)

        #-- Longitude (Vertical): Vt(top), Vb(bottom)
        Vtparam = { 'name':'Vt', 'Pv':(int(self.gImgW/2), 0) }
        Vbparam = { 'name':'Vb', 'Pv':(int(self.gImgW/2), self.gImgH) }
        Vplist = [ Vtparam, Vbparam ]
        for Vp in Vplist:
            rect_name = Vp['name']
            self._update_QHV_rect(rect_name, Po, Vp['Pv'], fraction)



    def _calculate_all_shadings(self, cvSrcImg):
        """To calculate the luma/chroma shading of each shading rectangles.

        The calculated result is saved in self.gShadingINFO which is a dictionary of the following format:
            e.g., { 'Co':shadingDict, 'Q1':shadingDict, ... }
                where shadingDict specifies the Luma/Chroma and Vertexes of the named shading rectangle

        Arguments
        --------------
        cvSrcImg: cv Mat
            the source image to get sub-image of each shading rectangle
        """
        #-- clear the shading info list
        self.gShadingINFO.clear()

        #-- get vertexes of all shading rectangles
        allRect = self.gShadingRECT.get_vertex_all()
        #print(allRect)

        #-- calculate Y, R/G/B of each sub-image
        for rect in allRect:
            nameID = rect[0]
            VPt = rect[1]
            VPb = rect[2]

            subimg = cvSrcImg[VPt[1]:VPb[1], VPt[0]:VPb[0]]
            subGray = cv2.cvtColor(subimg, cv2.COLOR_BGR2GRAY)

            Bmean = int(np.mean(subimg[:,:,0]))
            Gmean = int(np.mean(subimg[:,:,1]))
            Rmean = int(np.mean(subimg[:,:,2]))
            Ymean = int(np.mean(subGray))

            Rratio = Rmean/Gmean
            Bratio = Bmean/Gmean

            if False:
                #print(nameID, ": shape= ", subGray.shape, shading rect 的 an= ", Ymean, " Gmean= ", Gmean)
                Ytext = "Y= "+str(Ymean)
                RGtext = "R/G= "+ "{:.2f}%".format(Rratio)
                BGtext = "B/G= "+ "{:.2f}%".format(Bratio)
                print(Ytext, ' ', RGtext, ' ', BGtext)

                text = Ytext
                fface = cv2.FONT_HERSHEY_SIMPLEX
                fscale=1
                fthick=2
                ((tw, th),tpad) = cv2.getTextSize(text=Ytext, fontFace=fface, fontScale=fscale, thickness=fthick)
                cv2.putText(cv_img, text, (VPt[0], VPb[1]+(th+tpad*2)), fface, fscale, (0, 0, 200), fthick, 255)
                #text = nameID + ": Y= " + str(Ymean) + " (R,G,B)= " + str(Rmean) + ", " + str(Gmean) + ", " + str(Bmean)
                #print(text, ' @ ', (VPt[0], VPb[1]+10))
                #font = cv2.FONT_HERSHEY_SIMPLEX
                #fontScale=1
                #fontThinckness=1
                #cv2.putText(cv_img, text, (VPt[0], VPb[1]+20), font, 1, (0, 0, 200), 2, 255)
                #cv2.putText(gImgWC, text, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2, 255)
            shadingDict = { "Y":Ymean, "R":Rmean, "G":Gmean, "B":Bmean, "Vt":VPt, "Vb":VPb }
            self.gShadingINFO.setdefault(nameID, shadingDict)


    def update(self, cvSrcImg):
        """To update vertexes and Y, R/G/B values of all shading rectangles

        Call this method to update vertexes and sub-image values if the properties are changed.

        Arguments
        --------------
        cvSrcImg: cv2 Mat
            The source image which is used to get sub-image of each shading rectangle to calculate
            the luma/chroma information.
        """
        #-- Update vertexes of each shading rectangles
        self._update_all_rectangles()
        self.gShadingRECT.update()

        #-- Recalculate Y, R/G/B values of each shading rectangles
        self._calculate_all_shadings(cvSrcImg)

        return self.gShadingINFO

    def show(self, cv_win, cv_img):
        """To show all rectangles. (elaborate how to use gShadingINFO)

        Arguments
        --------------
        cv_win: cv2 window name
            The window to display the image with shading rectangles

        cv_img: cv2 Mat
            The image to draw shading rectangles on
        """
        color_pass = (0, 255, 0)
        color_ng = (0, 0, 255)
        Co = self.gShadingINFO['Co']
        Co_Y = Co['Y']
        Co_R = Co['R']
        Co_G = Co['G']
        Co_B = Co['B']
        lwidth = 2
        for k in self.gShadingINFO:

            shadingRect = self.gShadingINFO[k]
            Vt = shadingRect.get('Vt')
            Vb = shadingRect.get('Vb')
            _Y = shadingRect['Y']
            _R = shadingRect['R']
            _G = shadingRect['G']
            _B = shadingRect['B']

            #-- check Luma shading
            Y_ratio = _Y/Co_Y
            R_ratio = _R/_G
            B_ratio = _B/_G
            # print(k, ': Y_ratio= ', Y_ratio)
            # print(k, ': R_ratio= ', R_ratio)
            # print(k, ': B_ratio= ', B_ratio)
            if Y_ratio < 0.8 or Y_ratio > 1.2:
                is_pass = False
            elif R_ratio < 0.9 or R_ratio > 1.1:
                is_pass = False
            elif B_ratio < 0.9 or B_ratio > 1.1:
                is_pass = False
            else:
                is_pass = True

            if is_pass or k == 'Co':
                color = color_pass
            else:
                color = color_ng

            cv2.rectangle(cv_img, Vt, Vb, color, lwidth)

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
        print('Error: image not opened yet!!')
        return

    if 1==var_chkHori.get() or 1==var_chkVert.get():
        scl_fieldHV.config(state= NORMAL)
    else:
        scl_fieldHV.config(state= DISABLED)

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
    #gImgWC = gImgSrc.copy()
    #cv2.imshow(gSrcImgName, gImgWC)

    global gIsImgOpened
    gIsImgOpened = True

    global gImageShading
    gImageShading = ImageShading(gImgSrc.shape[1], gImgSrc.shape[0])
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
    chkbtn_Luma = Checkbutton(frmMid1, text='Luma')
    chkbtn_Luma.pack(side=LEFT)

    var_chkChroma = IntVar(value=1)
    chkbtn_Chroma = Checkbutton(frmMid1, text='Chroma')
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
    scl_fieldDiag.set(0.7)

    def cbfnScale_HvImgField(val):
        cbfn_Update()
        return
    scl_fieldHV = Scale(frmMidLeft, label='H/V: ', orient=HORIZONTAL, from_=0.1, to=1.0, resolution=0.05, command=cbfnScale_HvImgField)
    scl_fieldHV.pack(expand=True, fill=X)
    scl_fieldHV.set(0.7)

    # -- Frame: MidRight
    var_chkHori = IntVar(value=0)
    chkbtn_Hori = Checkbutton(frmMidRight, anchor=W, variable=var_chkHori, text='Horizontal', command=cbfn_Update)
    chkbtn_Hori.pack(side=TOP, expand=True, fill=X)

    var_chkVert = IntVar(value=0)
    chkbtn_Vert = Checkbutton(frmMidRight, anchor=W, variable=var_chkVert, text='Vertical', command=cbfn_Update)
    chkbtn_Vert.pack(side=TOP, expand=True, fill=X)


    #cbfn_Update()

    winRoot.mainloop()


if __name__ == "__main__":
    main()
