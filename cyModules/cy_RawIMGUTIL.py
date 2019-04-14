#!/usr/bin/python
#-- encoding: utf-8 --

import os, sys, platform

import argparse
import cv2
import numpy as np

import cy_OSUTIL as cyOS

debug_ctrl = False

bayerImg_geometric = { # (X, Y)
    0: (300, 140),  # R
    1: (340, 170),  # Gr
    2: (380, 200),  # Gb
    3: (420, 230),  # B
    100: (300, 300), # RawGray
    101: (330, 330) # RawRGB
}


SelAB = lambda A_true, B_false, CondSt : A_true if CondSt else B_false


###########################################################
# Functions : _cyRawPrint
###########################################################
def _cyRawPrint(*args):
    if debug_ctrl:
        print(' '.join(map(str,args)))




###########################################################
# Functions : _load_raw_image_file
###########################################################
def rawBayer_Type_To_Code(bayerType):
    bayerCodeTable = {'R':0, 'Gr':1, 'Gb':2, 'B':3 }
    return bayerCodeTable.get(bayerType, 99)



###########################################################
# Functions : _load_raw_image_file
###########################################################
def load_raw_file(rawFileName, nbits, packed):
    '''
    Read and load raw file into an numpy array.

    Arguments:
    ---------------
    rawFileName: str
        the file name of the raw image

    nbits: int, number of bits per pixel

    packed: boolean, tell if target is a packed raw image.

    Returns:
    ---------------
    (nparry, fl_dir, fl_base, fl_ext)
    '''
    #-------------------------------------------------
    # Load raw image into an np array
    #-------------------------------------------------
    #_cyRawPrint("load_raw_file(): rawFileName: {}, nbits: {}, packed: {}".format(rawFileName, nbits, packed))
    try:
        if nbits > 8 or not packed:
            raw_array = np.fromfile(rawFileName, dtype=np.uint16)
        else:
            raw_array = np.fromfile(rawFileName, dtype=np.uint8)
    except:
        print('ERROR: Failed to open file : ', rawFileName)
        return np.empty(1), "", "", ""

    #-------------------------------------------------
    # Parse directory path, basename, extname of the file
    #-------------------------------------------------
    fl_dir, fl_base, fl_ext = cyOS.parse_path(rawFileName)

    return raw_array, fl_dir, fl_base, fl_ext



###########################################################
# Function : reshape_raw_image
###########################################################
def reshape_raw_image(raw_arry, width, height, nbits):
    '''
    @Brief
        To convert UNACKED bayer array into shaped image

    @Returns
        the reshaped raw image, or None if fails
    '''
    imgW, imgH = (int(width>>1))<<1, (int(height>>1)<<1)
    #---------------------
    # Convert to shaped Raw Image
    #---------------------
    _cyRawPrint("--- Reshaping raw array {} to imag {}x{}".format(raw_arry.shape[0], imgW, imgH))
    expected_size = imgW * imgH

    if len(raw_arry) != expected_size:
        _cyRawPrint("expSize= {}, len(arry)= {}".format(expected_size, len(raw_arry)))
        _cyRawPrint("ERROR:reshape_raw_image(): Incorrect size !!")
        return None

    imgRaw = raw_arry.reshape(imgH, imgW)
    return imgRaw



###########################################################
# Function : _reorder_R_Gr_Gb_B
###########################################################
def _reorder_R_Gr_Gb_B(bayerCode, imgC1, imgC2, imgC3, imgC4):
    bayerCode_RGrGbB_LUT = {
        0: (imgC1, imgC2, imgC3, imgC4),
        1: (imgC2, imgC1, imgC4, imgC3),
        2: (imgC3, imgC4, imgC1, imgC2),
        3: (imgC4, imgC3, imgC2, imgC1),
    }
    return bayerCode_RGrGbB_LUT.get(bayerCode)


###########################################################
# Function : split_bayer_raw16
###########################################################
def split_bayer_raw16(imgRaw, width, height, rawBits, bayerCode):
    """
    """
    imgW, imgH = (int(width>>1))<<1, (int(height>>1)<<1)

    bitshift = 16-rawBits   #-- align to 16-bit domain

    bayerImg = imgRaw[0:imgH+1:2, 0:imgW+1:2]
    bayerImgC1 = bayerImg << bitshift

    bayerImg = imgRaw[0:imgH+1:2, 1:imgW+1:2]
    bayerImgC2 = bayerImg << bitshift

    bayerImg = imgRaw[1:imgH+1:2, 0:imgW+1:2]
    bayerImgC3 = bayerImg << bitshift

    bayerImg = imgRaw[1:imgH+1:2, 1:imgW+1:2]
    bayerImgC4 = bayerImg << bitshift

    imgR, imgGr, imgGb, imgB = \
        _reorder_R_Gr_Gb_B(bayerCode, bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4)

    return imgR, imgGr, imgGb, imgB


###########################################################
# Function : split_bayer_raw8
###########################################################
def split_bayer_raw8(imgRaw, width, height, rawBits, bayerCode):
    """
    """
    imgW, imgH = (int(width>>1))<<1, (int(height>>1)<<1)

    bayerImgC1 = imgRaw[0:imgH+1:2, 0:imgW+1:2]
    bayerImgC2 = imgRaw[0:imgH+1:2, 1:imgW+1:2]
    bayerImgC3 = imgRaw[1:imgH+1:2, 0:imgW+1:2]
    bayerImgC4 = imgRaw[1:imgH+1:2, 1:imgW+1:2]

    imgR, imgGr, imgGb, imgB = \
        _reorder_R_Gr_Gb_B(bayerCode, bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4)

    return imgR, imgGr, imgGb, imgB


###########################################################
# CLASS : cySoCRaw
###########################################################
class cySoCRaw():
    """
    Object of processing camera SoC RAW image.
    """

    #--------------------------------------------
    # __init__
    #--------------------------------------------
    def __init__(self, rawFile, rawShape, rawBayer, packed=False, debug=False):
        '''
        Arguments:
        ----------
            rawFile: str
                Name of the Raw image.

            rawShape: triple
                Specify (width, height, nbits) of the raw image.

            rawBayer: str
                Specify the bayer color of starting pixle, 'R'/'Gr'/'Gb'/'B'

            packed: boolean
                Tell if it is a packed raw file.
                Optional, default is unpacked.

            debug: boolean
                Debug print control.
                Optional, default is disabled.

        @Return
        -----------
            the shaped raw image, or None if fails
        '''
        global debug_ctrl
        debug_ctrl = debug

        #-------------------------------------------------
        # load raw file into a raw array
        #-------------------------------------------------
        _cyRawPrint("Loading RAW file ...")
        raw_arry, raw_root, raw_base, raw_ext = load_raw_file(rawFile, rawShape[2], packed)

        if raw_root == "" and raw_base == "":
            print("FATAL: Failed to load raw file, {} !".format(rawFile))
            return

        _cyRawPrint("Raw file, {}, loaded...".format(rawFile))

        #---- save raw globals
        self.gRawImgFile = rawFile
        self.gRawWidth = rawShape[0]
        self.gRawHeight = rawShape[1]
        self.gRawBits = rawShape[2]
        self.gRawBayerType = rawBayer
        self.gRawBayerCode = rawBayer_Type_To_Code(rawBayer)
        self.gRawPacked = packed

        if True:
            print("-------------------------------------------------------")
            print("RawFile: ", self.gRawImgFile)
            print("RawSize: {}x{}, nbits= {}".format(self.gRawWidth, self.gRawHeight, self.gRawBits))
            print("BayerType/Code= {}/{}, packed= {}".format(rawBayer, self.gRawBayerCode, self.gRawPacked))
            print("-------------------------------------------------------")

        self.gRawArray = raw_arry
        self.gRawRootDir = raw_root
        self.gRawBaseName = raw_base
        self.gRawExtName = raw_ext

        self.gImgR  = None
        self.gImgGr = None
        self.gImgGb = None
        self.gImgB  = None

        #-------------------------------------------------
        # Convert raw array into shaped raw image
        #-------------------------------------------------
        _cyRawPrint("Reshaping RAW array to Raw image ...")
        if self.gRawPacked:
            print("Yet to spport packed raw !")
        else:
            imgRaw = reshape_raw_image(self.gRawArray, self.gRawWidth, self.gRawHeight, self.gRawBits)
            if not imgRaw.any():
                print("ERROR: failed to reshape image array!")
                return
            self.gImgRaw = imgRaw

        #--------------------------------
        # save gMatRaw: shift to 8-bit domain
        #--------------------------------
        _cyRawPrint("Converting matRaw ...")
        nbits = self.gRawBits
        if nbits > 8:
            matRaw = imgRaw >> (self.gRawBits-8)
            self.gMatRaw = matRaw.astype(np.uint8)
        else:
            self.gMatRaw = imgRaw

        matRaw = self.gMatRaw
        #-----------------------------------------------------
        # convert gMatGray
        #-----------------------------------------------------
        _cyRawPrint("Converting matGray ...")
        bayer2gray_code = {
            0: cv2.COLOR_BAYER_RG2GRAY,
            1: cv2.COLOR_BAYER_GR2GRAY,
            2: cv2.COLOR_BAYER_GB2GRAY,
            3: cv2.COLOR_BAYER_BG2GRAY
        }

        code = bayer2gray_code.get(self.gRawBayerCode, cv2.COLOR_BAYER_RG2GRAY)
        self.gMatGray = cv2.cvtColor(matRaw, code)

        #-----------------------------------------------------
        # convert gMatBGR (for cv2)
        #-----------------------------------------------------
        _cyRawPrint("Converting matBGR ...")
        bayer2bgr_code = {
            0: cv2.COLOR_BAYER_RG2BGR,
            1: cv2.COLOR_BAYER_GR2BGR,
            2: cv2.COLOR_BAYER_GB2BGR,
            3: cv2.COLOR_BAYER_BG2BGR
        }

        code = bayer2bgr_code.get(self.gRawBayerCode, cv2.COLOR_BAYER_RG2BGR)
        self.gMatBGR = cv2.cvtColor(matRaw, code)



    #--------------------------------------------
    # save_rawGray
    #--------------------------------------------
    def save_rawGray(self, outDir='default', outBase='default', outExt='.jpg'):
        #----------------------------
        # format output filename
        #----------------------------
        out_root, out_base = self.format_output_dir(outDir, outBase, "_Gray")

        #_cyRawPrint("out_root= ", out_root)
        cyOS.create_dir(out_root)

        out_filename = out_root + "/" +out_base + outExt
        _cyRawPrint("output file: {}".format(out_filename))

        #-------------------------------------
        # save raw gray image
        #-------------------------------------
        cv2.imwrite(out_filename, self.gMatGray)


    #--------------------------------------------
    # save_rawRGB
    #--------------------------------------------
    def save_rawRGB(self, outDir='default', outBase='default', outExt='.jpg'):
        #----------------------------
        # format output filename
        #----------------------------
        out_root, out_base = self.format_output_dir(outDir, outBase, "_RGB")

        cyOS.create_dir(out_root)

        out_filename = out_root + "/" + out_base + outExt
        _cyRawPrint("output file: {}".format(out_filename))

        #-------------------------------------
        # save raw color image
        #-------------------------------------
        cv2.imwrite(out_filename, self.gMatBGR)


    #--------------------------------------------
    # display_rawGray
    #--------------------------------------------
    def display_rawGray(self, gMaxImgShowWidth=640):
        win_title = self.gRawBaseName + "_GRAY"
        _cyRawPrint("Display {} ...".format(win_title))
        cv2.namedWindow(win_title, cv2.WINDOW_NORMAL)
        x, y = bayerImg_geometric.get(100)
        cv2.moveWindow(win_title, x, y)
        h, w = self.gMatGray.shape
        if w > gMaxImgShowWidth:
            h = int( (h * gMaxImgShowWidth) / w)
            w = gMaxImgShowWidth
        cv2.resizeWindow(win_title, w, h)
        cv2.imshow(win_title, self.gMatGray)


    #--------------------------------------------
    # display_rawRGB
    #--------------------------------------------
    def display_rawRGB(self, gMaxImgShowWidth=640):
        win_title = self.gRawBaseName + "_RGB"
        _cyRawPrint("Display {} ...".format(win_title))
        cv2.namedWindow(win_title, cv2.WINDOW_NORMAL)
        x, y = bayerImg_geometric.get(101)
        cv2.moveWindow(win_title, x, y)
        h, w, _ = self.gMatBGR.shape
        if w > gMaxImgShowWidth:
            h = int( (h * gMaxImgShowWidth) / w)
            w = gMaxImgShowWidth
        cv2.resizeWindow(win_title, w, h)
        cv2.imshow(win_title, self.gMatBGR)



    #--------------------------------------------
    # split_raw_bayer_image
    #--------------------------------------------
    def split_raw_bayer_image(self):
        """
        @Returns:
            the splited sub-images: imgR, imgGr, imgGb, imgB
        """
        width, height = self.gRawWidth, self.gRawHeight
        raw_img = self.gImgRaw
        rawBits = self.gRawBits
        bayerCode = self.gRawBayerCode

        if rawBits > 8:
            imgR, imgGr, imgGb, imgB = \
                split_bayer_raw16(raw_img, width, height, rawBits, bayerCode)
        else:
            imgR, imgGr, imgGb, imgB = \
                split_bayer_ra18(raw_img, width, height, rawBits, bayerCode)

        self.gImgR  = imgR
        self.gImgGr = imgGr
        self.gImgGb = imgGb
        self.gImgB  = imgB

        return self.gImgR, self.gImgGr, self.gImgGb, self.gImgB



    #--------------------------------------------
    # save_raw_bayer_image
    #--------------------------------------------
    def save_raw_bayer_image(self, outDir='default', outBase='default', outExt='.jpg'):
        #----------------------------
        # format output filename
        #----------------------------
        out_root, out_base = self.format_output_dir(outDir, outBase)

        cyOS.create_dir(out_root)

        #-----------------
        # imgR
        #-----------------
        out_filename = out_root + "/" + out_base + "_R" + outExt
        _cyRawPrint("output file: {}".format(out_filename))
        img = self.gImgR.astype(np.uint8)
        matImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        matImg[:,:,0] = 0
        matImg[:,:,1] = 0
        cv2.imwrite(out_filename, matImg)

        #-----------------
        # imgGr
        #-----------------
        out_filename = out_root + "/" + out_base + "_Gr" + outExt
        _cyRawPrint("output file: {}".format(out_filename))
        img = self.gImgGr.astype(np.uint8)
        matImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        matImg[:,:,0] = 0
        matImg[:,:,2] = 0
        cv2.imwrite(out_filename, matImg)

        #-----------------
        # imgGb
        #-----------------
        out_filename = out_root + "/" + out_base + "_Gb" + outExt
        _cyRawPrint("output file: {}".format(out_filename))
        img = self.gImgGb.astype(np.uint8)
        matImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        matImg[:,:,0] = 0
        matImg[:,:,2] = 0
        cv2.imwrite(out_filename, matImg)

        #-----------------
        # imgB
        #-----------------
        out_filename = out_root + "/" + out_base + "_B" + outExt
        _cyRawPrint("output file: {}".format(out_filename))
        img = self.gImgB.astype(np.uint8)
        matImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        matImg[:,:,1] = 0
        matImg[:,:,2] = 0
        cv2.imwrite(out_filename, matImg)


    #--------------------------------------------
    # print_statistics
    #--------------------------------------------
    def print_statistics(self, outDir='default', outBase='default', saveOutput=False, outExt='.csv'):
        outText = "Filename: {}, BayerType: {}, nBits: {}\n".format(self.gRawImgFile, self.gRawBayerType, self.gRawBits)
        meanR   = self.gImgR.mean()
        meanGr  = self.gImgGr.mean()
        meanGb  = self.gImgGb.mean()
        meanB   = self.gImgB.mean()
        outText += "Raw Mean (R/Gr/Gb/B): {:.1f} {:.1f} {:.1f} {:.1f}\n".format(meanR, meanGr, meanGb, meanB)
        print(outText)

        if saveOutput:
            out_root, out_base = self.format_output_dir(outDir, outBase)
            out_filename = out_root + "/" + out_base + outExt
            with open(out_filename, "w") as outfile:
                outfile.write(outText)

    #--------------------------------------------
    # format_output_dir
    #--------------------------------------------
    def format_output_dir(self, outDir='default', outBase='default', baseSubfix=""):
        if outBase == 'default':
            out_base = self.gRawBaseName + baseSubfix
        else:
            out_base = outBase

        if outDir == 'default':
            out_root = self.gRawRootDir + '/_imageRepo/' + self.gRawBaseName
        else:
            out_root = outDir

        return out_root, out_base

