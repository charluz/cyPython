#!/usr/bin/python

import os, sys, platform
import numpy as np
import cv2

if __name__ == "__main__":
    import Add_cyModules
else:
    import cyPyModules.Add_cyModules

import cy_OSUTIL as cyOS
import cy_CvOSD as OSD
import cy_debug as DP


color_pass = (0, 255, 0)
color_ng = (0, 0, 255)
lwidth = 2

dprint = DP.DebugPrint('scfunc')

###########################################################
# Function : cbfn_Update()
###########################################################

def test_shading(cv_img, shadingINFO, rect_list, spec):
    """
    spec: list
        [centerY, lumaSpecRatioMin, lumaSpecDev, colorSpecDev, chkLuma, chkColor]
    """
    maxRect, minRect = [ '' for _ in range(2)]
    maxY = minY = 0
    rectY = []
    for k in rect_list:
        rect = shadingINFO[k]
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
        rect = shadingINFO[k]
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
            if yC2C > 1.0 or yC2C < specLumaMin:
                is_pass = False
            #--- Luma corner to cornerMean deviation
            if yDev > (1.0+specLumaDev) or yDev < (1.0-specLumaDev):
                # is_pass = False
                yDev_pass = False

        if chkColor:
            #--- R/G deviation
            if abs(r2g-1.0) > specColorDev:
                chroma_pass = False
            #--- B/G deviation
            if abs(b2g-1.0) > specColorDev:
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

    return
