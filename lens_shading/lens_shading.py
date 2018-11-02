#!/usr/bin/python

from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog

'''
from tkFileDialog import askopenfilename

That code would have worked fine in Python 2.x, but it is no longer valid. 
In Python 3.x, tkFileDialog was renamed to filedialog.
'''

winMain = Tk()
winMain.title('Lens Shading Viewer')
#winMain.geometry('300x150')


def cbfnButtonOpenRaw():
    global txtlblRawFName, btnOpenRaw
    txtlblRawFName.set(value=filedialog.askopenfilename() )
    print(txtlblRawFName.get())


btnOpenRaw = Button(winMain, text='Open RAW', command=cbfnButtonOpenRaw)
btnOpenRaw.grid(row=0, column=0, pady=2)
txtlblRawFName = StringVar()
##txtlblRawFName.set(value='test')
lblRawFName = Label(winMain, width=48, textvariable=txtlblRawFName)
lblRawFName.grid(row=0, column=1, columnspan=8)


lblRawWidth = Label(winMain, text='Width').grid(row=1, column=0, pady=2)
txtlblRawWidth = StringVar()
entryRawWidth = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawWidth)
entryRawWidth.grid(row=1, column=1, sticky=W)

lblRawHeight = Label(winMain, text='Height').grid(row=2, column=0, pady=2)
txtlblRawHeight = StringVar()
entryRawHeight = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawHeight)
entryRawHeight.grid(row=2, column=1, sticky=W)


def ShowChoice():
    global bayerSelect
    print(bayerSelect.get())

lblRawBayer = Label(winMain, text='Bayer').grid(row=1, column=3, pady=2)
bayerSelect = IntVar(value=3)
bayer_config = [ ('R', 0, 2, 3), ('Gr', 1, 2, 4), ('Gb', 2, 3, 3), ('B', 3, 3, 4) ]
#bayer_config = [ ('R', 0), ('Gr', 1), ('Gb', 2), ('B', 3) ]
for bayer, val, row, col in bayer_config:
    btn = Radiobutton(winMain, text=bayer,
                  padx = 20, 
                  variable=bayerSelect, 
                  command=ShowChoice,
                  value=val)
    btn.grid(row=row, column=col)
    btn.config(anchor=W, justify=LEFT, width=2)
    print("Bayer= %s, Row= %d, Column= %d" % (bayer, row, col) )

lblRawBits = Label(winMain, text='Pixel Bits').grid(row=3, column=0, padx=2, pady=2)
txtlblRawBits = StringVar()
entryRawBits = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawBits)
entryRawBits.grid(row=3, column=1, sticky=W)

varBytePack = IntVar(value=0)
chkBytePack = Checkbutton(winMain, text='Packed', variable=varBytePack)
chkBytePack.grid(row=4, column=1, sticky=W)



winMain.mainloop()

