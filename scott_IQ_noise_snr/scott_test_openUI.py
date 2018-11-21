#!/usr/bin/python
#coding:utf-8

import threading
import math
import time
from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import cv2  


drawing = False  
mode = True  
ix, iy = -1, -1  

def messageBoxOK(title, msg):
    box = Toplevel()
    box.title(title)
    Label(box, text=msg).pack()
    Button(box, text='OK', command=box.destroy).pack()


def cbfnButtonOpenRaw():
    global txtlblRawFName, btnRaw, rawdata,load_img_en
    global img,re_img,img2
    txtlblRawFName.set(value=filedialog.askopenfilename() )
    rawfname = txtlblRawFName.get()
    #print("11233455844",rawfname)
    img = cv2.imread(rawfname)
    #cv2.imshow('image', img)
    re_img = cv2.resize(img,(960,540),interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(img,(960,540),interpolation=cv2.INTER_CUBIC)
    cv2.namedWindow('image')  
    cv2.setMouseCallback('image', draw_circle)  
    load_img_en = 1
    try:
        f = open(rawfname, 'rb')
        rawdata = f.read()
        btnRaw.config(text='Load RAW', command=cbfnButtonLoadRaw, bg='Yellow')
        f.close()
    except:
        messageBoxOK('FileIO', 'Failed to open file :\n' + rawfname)
    '''
    with open(rawfname, 'rb') as in_file:
        rawdata = in_file.read()
        btnRaw.config(text='Load RAW', command=cbfnButtonLoadRaw)
    
'''

def draw_circle(event, x, y, flags, param):  
    global ix, iy, drawing, mode 
    global img,img2,re_img
  
    if event == cv2.EVENT_LBUTTONDOWN:  
        print("left button down")  
        #img = img2.copy()
        re_img = img2.copy()
        drawing = True  
        ix, iy = x,y  
    #elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:  
    elif event == cv2.EVENT_MOUSEMOVE:  
        #print('mouse move')  
        if drawing == True:  
            if mode == True: 
                if x < ix :
                    print("nono")
                else:
                    print("nono")
                    cv2.rectangle(re_img, (ix, iy), (x,y), (255,255,255), -1)  
                   #cv2.rectangle(re_img, (ix, iy), (x,y), (255,255,255), -1)
            else:  
                cv2.circle(re_img, (x, y), 10, (255,0,0), -1)  
                #cv2.circle(img, (x, y), 10, (255,0,0), -1)  
    elif event == cv2.EVENT_LBUTTONUP:  
        print('left button up')  
        print("ix,iy,x,y",ix,iy,x,y);
        drawing = False  
     
        img_w_ratio = img.shape[0]/re_img.shape[0]
        img_h_ratio = img.shape[1]/re_img.shape[1]

        y_start= int(img_h_ratio*iy)
        y_end= int(img_h_ratio*y)
        x_start= int(img_w_ratio*ix)
        x_end= int(img_w_ratio*x)

        print("img_w img_h",img_w_ratio,img_h_ratio)
        test_img = img[y_start:y_end, x_start:x_end]
        test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

        value = 0
        count_add = 0
        for i in range(test_img.shape[0]):
            for j in range(test_img.shape[1]):
                count_add += 1
                value += test_img[i, j]

        mean, std = cv2.meanStdDev(test_img)

        SNR_step1 = (mean*mean)/(std*std)
        SNR_step2 = math.log10(SNR_step1)
        SNR =SNR_step2*10
        print("SNR",SNR)

        print(mean,std)

        
        text2 = str(SNR)
        text = str(std)
        messageBoxOK('cul noise std', 'SNR:\n'+text2 +'DB \n'+'STD \n'+text)
        #text = 'Hello, OpenCV!'
        # 使用各種字體
        cv2.putText(test_img, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
        1, (255, 255, 255), 1, cv2.LINE_AA)
        print("Value",value)
        print("count_add",count_add)
        print("W , H",test_img.shape[0],test_img.shape[1])
        cv2.imshow('test_img',test_img)

def job():
  global load_img_en
  global img

  while(True):  
    
    k = cv2.waitKey(1)&0xff  

    if load_img_en == 1:
        cv2.imshow('image', re_img)
    
    if k == ord('m'):  
        print('you typed key m')  
        mode = not mode  
    elif k == 27:  
        break


  #for i in range(5):
   # print("Child thread:", i)
    #time.sleep(1)

# 建立一個子執行緒
load_img_en = 0
img = cv2.imread("D65.png") # init opencv info
img2 = img.copy() # init opencv info
re_img = img.copy() # init opencv info
t = threading.Thread(target = job)

#cv2.namedWindow('image')  
#cv2.setMouseCallback('image', draw_circle)  

# 執行該子執行緒
t.start()

winMain = Tk()
winMain.title('noise tool')
btnRaw = Button(winMain, text='Open cul noise', command=cbfnButtonOpenRaw, bg='LightGreen')
btnRaw.grid(row=0, column=0, pady=2)

txtlblRawFName = StringVar()
lblRawFName = Label(winMain, width=48, textvariable=txtlblRawFName)
lblRawFName.grid(row=0, column=1, columnspan=8)

winMain.mainloop()

