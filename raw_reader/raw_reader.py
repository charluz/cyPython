#!/usr/bin/python

from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

'''
from tkFileDialog import askopenfilename

That code would have worked fine in Python 2.x, but it is no longer valid. 
In Python 3.x, tkFileDialog was renamed to filedialog.
'''

###########################################################
# Message Box with OK button
###########################################################
def messageBoxOK(title, msg):
    box = Toplevel()
    box.title(title)
    Label(box, text=msg).pack()
    Button(box, text='OK', command=box.destroy).pack()



###########################################################
# Function : Split Bayer Components
###########################################################
def cbfnButtonReset():
    cv2.destroyAllWindows()
    btnRaw.config(text='Load RAW', command=cbfnButtonOpenRaw, bg='LightGreen')


def select_Bayer_to_BGR(bayer):
    bayer2bgr = { 
        0:cv2.COLOR_BAYER_RG2BGR, 
        1:cv2.COLOR_BAYER_GR2BGR,
        2:cv2.COLOR_BAYER_GB2BGR,
        3:cv2.COLOR_BAYER_BG2BGR
    }

    code = bayer2bgr.get(bayer, cv2.COLOR_BAYER_RG2BGR)
    return code

###########################################################
# Button Function : LoadRAW
###########################################################
def cbfnButtonLoadRaw():
    global btnRaw, rawdata, rawfname, bayerSelect

    winPosRow, winPosCol = 300, 100
    # RAW image
    imgSize = int(txtlblRawHeight.get()), int(txtlblRawWidth.get())
    imgRaw = rawdata.reshape(imgSize)
    imgRaw *= 2**(16-int(txtlblRawBits.get()))
    '''
    cv2.namedWindow("RAW Image", cv2.WINDOW_NORMAL)
    cv2.moveWindow("RAW Image", winPosRow, winPosCol)
    cv2.imshow("RAW Image", imgRaw)
    '''

    # 
    # CV2 BGR image
    imgRaw = imgRaw / 256
    imgRaw = imgRaw.astype(np.uint8)
    tranCode = select_Bayer_to_BGR(bayerSelect.get())
    matBGR = cv2.cvtColor(imgRaw, tranCode)
    cv2.namedWindow("BGR Image", cv2.WINDOW_NORMAL)
    winPosCol += 20
    winPosRow += 40
    cv2.moveWindow("BGR Image", winPosRow, winPosCol)
    cv2.imshow("BGR Image", matBGR)
    basename = os.path.basename(rawfname)
    base, ext = os.path.splitext(basename)
    jpgName = base + '.jpg'
    cv2.imwrite(jpgName, matBGR)

    # CV2 Gray RAW image
    matGray = cv2.cvtColor(matBGR, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow("Gray U8 Image", cv2.WINDOW_NORMAL)
    winPosCol += 20
    winPosRow += 40
    cv2.moveWindow("Gray U8 Image", winPosRow, winPosCol)
    cv2.imshow("Gray U8 Image", matGray)
    jpgGray = base + '_GRAY.jpg'
    cv2.imwrite(jpgGray, matGray)

    btnRaw.config(text='RESET', command=cbfnButtonReset, bg='LightGray')


###########################################################
# Button Function : OpenRAW
###########################################################
def cbfnButtonOpenRaw():
    global winMain, winTitle, txtlblRawFName, btnRaw, rawdata, rawfname
    rawfname = filedialog.askopenfilename()
    #print(rawfname)
    try:
        # f = open(rawfname, 'rb')
        # rawdata = f.read()
        # f.close()
        rawdata = np.fromfile(rawfname, dtype=np.uint16)
    except:
        messageBoxOK('FileIO', 'Failed to open file :\n' + rawfname)

    baseName = os.path.basename(rawfname)
    winMain.title(winTitle+ ' -- ' + baseName)

    #btnRaw.config(text='Load RAW', command=cbfnButtonLoadRaw, bg='Yellow')
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

    winTitle = 'Raw Viewer'
    winMain = Tk()
    winMain.title(winTitle)
    winMain.geometry('400x150')

    curRow, curCol = 0, 0
    # Button : Open RAW 
    btnRaw = Button(winMain, text='Open RAW', command=cbfnButtonOpenRaw, bg='LightGreen')
    btnRaw.grid(row=curRow, column=curCol, pady=2)

    # Button : Exit
    btnExit = Button(winMain, text='Exit', command=cbfnButtonMainExit, bg='Red')
    btnExit.grid(row=curRow, column=7)

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



    winMain.mainloop()

