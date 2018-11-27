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
# Function : switch case dispatch to save R/Gr/Gb/B images
###########################################################
def save_raw_RGrGbB_image(img1, img2, img3, img4):
    plt.imsave('./raw_R_gray.jpg', img1)
    plt.imsave('./raw_Gr_gray.jpg', img2)
    plt.imsave('./raw_Gb_gray.jpg', img3)
    plt.imsave('./raw_B_gray.jpg', img4)

def save_raw_GrRBGb_image(img1, img2, img3, img4):
    winGrName = "RAW_Gr"
    cv2.namedWindow(winGrName, cv2.WINDOW_AUTOSIZE)
    img = img1.astype(np.uint8)
    matGr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.imshow(winGrName, matGr)
    # plt.imsave('./raw_Gr_gray.jpg', img1)
    # plt.imsave('./raw_Gr.jpg', img1)
    # plt.imsave('./raw_R_gray.jpg', img2)
    # plt.imsave('./raw_B_gray.jpg', img3)
    # plt.imsave('./raw_Gb_gray.jpg', img4)

def save_raw_GbBRGr_image(img1, img2, img3, img4):
    plt.imsave('./raw_Gb_gray.jpg', img1)
    plt.imsave('./raw_B_gray.jpg', img2)
    plt.imsave('./raw_R_gray.jpg', img3)
    plt.imsave('./raw_Gr_gray.jpg', img4)

def save_raw_BGbGrR_image(img1, img2, img3, img4):
    plt.imsave('./raw_B_gray.jpg', img1)
    plt.imsave('./raw_Gb_gray.jpg', img2)
    plt.imsave('./raw_Gr_gray.jpg', img3)
    plt.imsave('./raw_R_gray.jpg', img4)


def save_raw_XXXX_image(img1, img2, img3, img4):
    messageBoxOK('ERROR', 'Unknown bayer type !!')


###########################################################
# Function : Split Bayer Components
###########################################################
def splitBayerRawWord(bayerdata, width, height, rawBits, bayerType):
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
        simg1, simg2, simg3, simg4 : sub-images of R/Gr/Gb/B. 
            Size of sub-image is (widht/2, height/2).
    '''
    global simg1, simg2, simg3, simg4

    imgW, imgH = (int(width>>1))<<1, (int(height>>1)<<1)
    simgW, simgH =int(imgW>>1), int(imgH>>1)
    simg1, simg2, simg3, simg4 = [np.zeros([simgH, simgW, 1], np.uint8) for x in range(4)]

    print("width %d -> %d, height %d -> %d" % (imgW, simgW, imgH, simgH))
    btnRaw.config(bg='Coral')
    bitshift = rawBits-8

    imgRaw = bayerdata.reshape(imgH, imgW)
    simg1 = imgRaw[0:imgH+1:2, 0:imgW+1:2] >> bitshift
    simg2 = imgRaw[0:imgH+1:2, 1:imgW+1:2] >> bitshift
    simg3 = imgRaw[1:imgH+1:2, 0:imgW+1:2] >> bitshift
    simg4 = imgRaw[1:imgH+1:2, 1:imgW+1:2] >> bitshift

    # print("imgRaw ", end=''); print(imgRaw[320:322,570:572])
    # print("simg1 ", end=''); print(simg1[320:322,570:572])
    # print("simg2 ", end=''); print(simg2[320:322,570:572])
    # print("simg3 ", end=''); print(simg3[320:322,570:572])
    # print("simg4 ", end=''); print(simg4[320:322,570:572])
    # for rr in range (0, imgH, 2):       # process two rows at a time, R/Gr, Gb/B
    #     row_even_offset = rr * imgW     # 2 bytes per pixels
    #     row_odd_offset = row_even_offset + imgW
    #     for cc in range (0, imgW, 2):
    #         col_offset = cc
    #         rrow = rr>>1
    #         ccol = cc>>1
    #         ## color_1 (bayer top-left)
    #         # lbyte = bayerdata[row_even_offset+col_offset]
    #         # hbyte = bayerdata[row_even_offset+col_offset+1]
    #         # pix_v = (hbyte*256 + lbyte) >> (rawBits-8)
    #         pix_v = bayerdata[row_even_offset+col_offset] >> bitshift
    #         simg1[rrow,ccol] = [pix_v for x in range(3)]

    #         ## color_2 (bayer top-right)
    #         # lbyte = bayerdata[row_even_offset+col_offset+2]
    #         # hbyte = bayerdata[row_even_offset+col_offset+3]
    #         # pix_v = (hbyte*256 + lbyte)  >> (rawBits-8)
    #         pix_v = bayerdata[row_even_offset+col_offset+1] >> bitshift
    #         simg2[rrow,ccol] = [pix_v for x in range(3)]

    #         ## color_3 (bayer bottom-left)
    #         # lbyte = bayerdata[row_odd_offset+col_offset]
    #         # hbyte = bayerdata[row_odd_offset+col_offset+1]
    #         # pix_v = (hbyte*256 + lbyte)  >> (rawBits-8)
    #         pix_v = bayerdata[row_odd_offset+col_offset] >> bitshift
    #         simg3[rrow,ccol] = [pix_v for x in range(3)]

    #         ## color_4 (bayer bottom-right)
    #         # lbyte = bayerdata[row_odd_offset+col_offset+2]
    #         # hbyte = bayerdata[row_odd_offset+col_offset+3]
    #         # pix_v = (hbyte*256 + lbyte)  >> (rawBits-8)
    #         pix_v = bayerdata[row_odd_offset+col_offset+1] >> bitshift
    #         simg4[rrow,ccol] = [pix_v for x in range(3)]

    save_bayer_img = { 
        0:save_raw_RGrGbB_image, 
        1:save_raw_GrRBGb_image,
        2:save_raw_GbBRGr_image,
        3:save_raw_BGbGrR_image
    }

    func = save_bayer_img.get(bayerType, save_raw_XXXX_image)
    func(simg1, simg2, simg3, simg4)
    btnRaw.config(text='Load RAW', command=cbfnButtonOpenRaw, bg='LightGray')
    #print(simg4)
    # plt.imshow(simg4); plt.show()
    # plt.imshow(simg3); plt.show()
    # plt.imshow(simg2); plt.show()
    plt.imshow(simg1); plt.show()
    # plt.imshow(imgRaw); plt.show()
    # plt.imsave('./simg1.jpg', simg1)
    # plt.imsave('./simg2.jpg', simg2)
    # plt.imsave('./simg3.jpg', simg3)
    # plt.imsave('./simg4.jpg', simg4)

    return True


###########################################################
# Button Function : LoadRAW
###########################################################
def cbfnButtonLoadRaw():
    global btnRaw, rawdata
    # print("Button: Load RAW")
    splitBayerRawWord(rawdata, int(txtlblRawWidth.get()), 
                    int(txtlblRawHeight.get()), 
                    int(txtlblRawBits.get()),  
                    bayerSelect.get())

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

