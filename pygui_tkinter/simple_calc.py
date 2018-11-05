#!/usr/bin/python

'''
Reference : https://yunlinsong.blogspot.com/2018/02/python-tkintera-simple-calculator-with.html
'''


# 步驟一：匯入 tkinter 模組。
from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button

# 步驟二：建立主視窗。
winMain = Tk()
varShutter = StringVar(value="18e")
varGain = StringVar(value="5c")

# operation = [ '+', '-', '*', '/']


# 視窗標題
winMain.title("MTK 曝光計算機")
# 視窗大小
winMain.geometry("+200+200")


# 步驟三：建立視窗控制項元件。
# 建立標籤
txt60Hz="""
1/120" = 8.333ms  (0x201)  1/60" = 16.666ms (0x402)
1/30"  = 33.333ms (0x803)  1/15" = 66.666ms (0x1006)
"""
lbl60HzShutterTime = Label(winMain, text=txt60Hz).grid(row=4, column=0, columnspan=4)

lblShutter = Label(winMain, text="Shutter").grid(row=1, column=0)
lblGain = Label(winMain, text="Gain").grid(row=2, column=0)

lblHex = Label(winMain, text="HEX").grid(row=0, column=1)
lblDec = Label(winMain, text="DEC").grid(row=0, column=3)


# 建立文字輸入方塊
entryShutterHex = Entry(winMain, bd=2, justify=CENTER, textvariable=varShutter).grid(row=1, column=1)
entryGainHex = Entry(winMain, bd=2, justify=CENTER, textvariable=varGain).grid(row=2, column=1)

# 建立文字方塊
strLabelShutterDec = StringVar(value="                  ")
strLabelGainDec = StringVar(value="  ")
lblShutterDec = Label(winMain, textvariable=strLabelShutterDec).grid(row=1, column=3, padx=4)
lblGainDec = Label(winMain, textvariable=strLabelGainDec).grid(row=2, column=3, padx=4)

# 按鈕 Click 事件處理函式
def calc():
    # global entryShutterHex, entryGainHex
    ## Update Shutter Time in ms
    s = varShutter.get()
    v = int(s, base=16)
    # print("Shutter : %d" % v)
    s = str(v) + " --> " + str((16.25*v)/1000.) + " ms "
    strLabelShutterDec.set(value=s)

    ## Update Gain (uinty gain = 1024)
    s = varGain.get()
    v = int(s, base=16)
    #print("Gain : %d " % v)
    s = str(v) + " --> " + str(int((1024*v)/64))
    strLabelGainDec.set(value=s)



# 建立按鈕
btnCalc = Button(winMain, text=">", command=calc). grid(row=1, rowspan=2, column=2)


'''
# 建立單選按鈕 aBtn ==> addition, sBtn ==> subtraction, mBtn ==> multiplication, dBtn ==> division
aBtn = Radiobutton(winMain, text="+", variable=var, value=0, command=cal)
sBtn = Radiobutton(winMain, text="-", variable=var, value=1, command=cal)
mBtn = Radiobutton(winMain, text="*", variable=var, value=2, command=cal)
dBtn = Radiobutton(winMain, text="/", variable=var, value=3, command=cal)

# 版面配置
lblHex.grid(row=0, column=1)
lblDec.grid(row=0, column=3)
lblShutter.grid(row=1, column=0)
lblGain.grid(row=2, column=0)

entryShutterHex.grid(row=1, column=1)
entryGainHex.grid(row=2, column=1)
btnCalc.grid(row=1, rowspan=2, column=2)
lblShutterDec.grid(row=1, column=3)
lblGainDec.grid(row=2, column=3)
'''




# 步驟四： 進入事件處理迴圈。
winMain.mainloop()