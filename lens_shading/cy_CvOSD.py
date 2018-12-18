#!/usr/bin/env python

import numpy as np
import cv2

#--------------------------------------
# Class: CvOSD
#--------------------------------------
class osdText():
    """
    """
    def __init__(self, text='', fface=cv2.FONT_HERSHEY_SIMPLEX, fcolor=(255, 255, 255), fscale=1, fthick=2):
        """
        """
        self.fontFace       = fface
        self.fontScale      = fscale
        self.fontColor      = fcolor
        self.fontThickness  = fthick
        self.text           = text
        self._update_dirty  = True

    def set_property(self, **kwargs):
        """
        """
        for kw, val in kwargs.items():
            if kw == 'fontColor':
                self.fontColor = val
            elif kw == 'fontScale':
                self.fontScale = val
            elif kw == 'fontFace':
                self.fontFace = val
            elif kw == 'fontThickness':
                self.fontThickness = val
            else:
                pass
        self._update_dirty = True

    def set_text(self, text):
        self.text = text
        self._update_dirty = True

    def update(self, force_update=False):
        """
        """
        if self._update_dirty == False and force_update == False:
            return

        #-- get size of text
        ((tw, th),tpad) = cv2.getTextSize(  text=self.text,
                                            fontFace=self.fontFace,
                                            fontScale=self.fontScale,
                                            thickness=self.fontThickness)

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

#---------------------------------------------------------------
# Module Test
#---------------------------------------------------------------

def main():
    print('I am in!')
    dprint = DebugPrint('main')
    print('Setting debug level: DEBUG_WARNING')
    dprint.set_level(DEBUG_WARNING)

    dprint.info('You won\'t see this!!')
    dprint.error('a error')
    dprint.warning('a warning')



if __name__ == "__main__":
    main()
