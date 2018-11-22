#!/usr/bin/python

from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    plt.imsave('./raw_Gr_gray.jpg', img1)
    img1[:,:][0] = 0
    img1[:,:][2] = 0
    plt.imsave('./raw_Gr.jpg', img1)
    plt.imsave('./raw_R_gray.jpg', img2)
    plt.imsave('./raw_B_gray.jpg', img3)
    plt.imsave('./raw_Gb_gray.jpg', img4)

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
    simg1, simg2, simg3, simg4 = [np.zeros([simgH, simgW, 3], np.uint8) for x in range(4)]

    print("width %d -> %d, height %d -> %d" % (imgW, simgW, imgH, simgH))
    btnRaw.config(bg='Coral')
    for rr in range (0, imgH, 2):       # process two rows at a time, R/Gr, Gb/B
        row_even_offset = rr * imgW * 2     # 2 bytes per pixels
        row_odd_offset = row_even_offset + (imgW * 2)
        for cc in range (0, imgW, 2):
            col_offset = cc * 2
            ## color_1 (bayer top-left)
            lbyte = bayerdata[row_even_offset+col_offset]
            hbyte = bayerdata[row_even_offset+col_offset+1]
            pix_v = (hbyte*256 + lbyte) >> (rawBits-8)
            simg1[rr>>1,cc>>1] = [pix_v for x in range(3)]

            ## color_2 (bayer top-right)
            lbyte = bayerdata[row_even_offset+col_offset+2]
            hbyte = bayerdata[row_even_offset+col_offset+3]
            pix_v = (hbyte*256 + lbyte)  >> (rawBits-8)
            simg2[rr>>1,cc>>1] = [pix_v for x in range(3)]

            ## color_3 (bayer bottom-left)
            lbyte = bayerdata[row_odd_offset+col_offset]
            hbyte = bayerdata[row_odd_offset+col_offset+1]
            pix_v = (hbyte*256 + lbyte)  >> (rawBits-8)
            simg3[rr>>1,cc>>1] = [pix_v for x in range(3)]

            ## color_4 (bayer bottom-right)
            lbyte = bayerdata[row_odd_offset+col_offset+2]
            hbyte = bayerdata[row_odd_offset+col_offset+3]
            pix_v = (hbyte*256 + lbyte)  >> (rawBits-8)
            simg4[rr>>1,cc>>1] = [pix_v for x in range(3)]

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
    # plt.imshow(simg4)
    # plt.show()
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
    print("Button: Load RAW")
    splitBayerRawWord(rawdata, int(txtlblRawWidth.get()), 
                    int(txtlblRawHeight.get()), 
                    int(txtlblRawBits.get()),  
                    bayerSelect.get())

###########################################################
# Button Function : OpenRAW
###########################################################
def cbfnButtonOpenRaw():
    global txtlblRawFName, btnRaw, rawdata
    txtlblRawFName.set(value=filedialog.askopenfilename() )
    rawfname = txtlblRawFName.get()
    #print(rawfname)
    try:
        # f = open(rawfname, 'rb')
        # rawdata = f.read()
        # f.close()
        rawdata = np.fromfile(rawfname, dtype=np.uint16)

    except:
        messageBoxOK('FileIO', 'Failed to open file :\n' + rawfname)



    imgSize = int(txtlblRawHeight.get()), int(txtlblRawWidth.get())
    imgRaw = np.array(rawdata, dtype=np.uint16).reshape(imgSize)
    matBGR = cv2.cvtColor(imgRaw, cv2.COLOR_BAYER_BG2BGR)


    imgRaw.converTo(imgRaw, -1, 1, 64,0)

    cv2.namedWindow("RAW Image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("BGR Image", cv2.WINDOW_NORMAL)
    cv2.imshow("RAW Image", imgRaw)
    cv2.imshow("BGR Image", matBGR)
    cv2.imwrite("xxx.jpg", matBGR)

    '''
    with open(rawfname, 'rb') as in_file:
        rawdata = in_file.read()
        btnRaw.config(text='Load RAW', command=cbfnButtonLoadRaw)
    '''

###########################################################
# MainEntry 
###########################################################

if __name__ == "__main__":
    winMain = Tk()
    winMain.title('Raw Viewer')
    #winMain.geometry('300x150')

    btnRaw = Button(winMain, text='Open RAW', command=cbfnButtonOpenRaw, bg='LightGreen')
    btnRaw.grid(row=0, column=0, pady=2)
    txtlblRawFName = StringVar()
    ##txtlblRawFName.set(value='test')
    lblRawFName = Label(winMain, width=48, textvariable=txtlblRawFName)
    lblRawFName.grid(row=0, column=1, columnspan=8)


    lblRawWidth = Label(winMain, text='Width')
    lblRawWidth.grid(row=1, column=0, pady=2)
    txtlblRawWidth = StringVar(value='2560') 
    entryRawWidth = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawWidth)
    entryRawWidth.grid(row=1, column=1, sticky=W)


    lblRawHeight = Label(winMain, text='Height')
    lblRawHeight.grid(row=2, column=0, pady=2)
    txtlblRawHeight = StringVar(value='1436')
    entryRawHeight = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawHeight)
    entryRawHeight.grid(row=2, column=1, sticky=W)


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

    lblRawBits = Label(winMain, text='Pixel Bits')
    lblRawBits.grid(row=3, column=0, padx=2, pady=2)
    txtlblRawBits = StringVar(value='10')
    entryRawBits = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawBits)
    entryRawBits.grid(row=3, column=1, sticky=W)

    varBytePack = IntVar(value=0)
    chkBytePack = Checkbutton(winMain, text='Packed', variable=varBytePack)
    chkBytePack.grid(row=4, column=1, sticky=W)

    winMain.mainloop()

