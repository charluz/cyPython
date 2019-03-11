# -*- coding: utf-8 -*-
import cv2
import time;

# ip camera 的擷取路徑
URL = "rtsp://192.168.1.67:554/stream1"

# 建立 VideoCapture 物件
ipcam = cv2.VideoCapture("TESR9166.MP4")

current_milli_time = 0
# 使用無窮迴圈擷取影像，直到按下Esc鍵結束
stat, I = ipcam.read()
stat, last_I = ipcam.read()
while True:
    # 使用 read 方法取回影像
    stat, I = ipcam.read()



    image_th = cv2.absdiff(last_I,I);
    ret,image_th = cv2.threshold(image_th,15,255,cv2.THRESH_BINARY)
    gray_image = cv2.cvtColor(image_th, cv2.COLOR_BGR2GRAY)
    cunt_value = cv2.countNonZero(gray_image)
    print(cunt_value)
    last_I = I
    # 加上一些影像處理...

    # imshow 和 waitkey 需搭配使用才能展示影像
    #if stat == True:
    #    cv2.imshow('Image', I)

    #if stat == False:
    #    print("ERROR FRAME")
    last_milli_time = current_milli_time
    current_milli_time = int(round(time.time() * 1000))
    spend_time = current_milli_time - last_milli_time
    #print(spend_time)

    if cv2.waitKey(1) == 27:
        ipcam.release()
        cv2.destroyAllWindows()
        break