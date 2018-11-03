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

def messageBoxOK(title, msg):
    box = Toplevel()
    box.title(title)
    Label(box, text=msg).pack()
    Button(box, text='OK', command=box.destroy).pack()



def splitBayerRawWord(bayerdata, width, height, rawBits):
    # if isPacked == True:
    #     messageBox('Error', 'Packed Raw Image is yet supported !!')
    #     return False

    w2 = (int(width>>1)<<1)<<1 # 2 bytes per pixel
    h = int(height>>1)<<1
    print("width %d -> %d, height %d -> %d" % (width, w2>>1, height, h))

    for rr in range (0, h, 2):   # process two rows at a time, R/Gr, Gb/B
        offset = rr * w2
        for cc in range (0, w2, 2):
            lbyte = bayerdata[offset+cc]
            hbyte = bayerdata[offset+cc+1]
            pix_v = hbyte*256 + lbyte

    return True

def cbfnButtonLoadRaw():
    global btnRaw, rawdata
    print("Button: Load RAW")
    splitBayerRawWord(rawdata, int(txtlblRawWidth.get()), 
                    int(txtlblRawHeight.get()), 
                    int(txtlblRawBits.get()) )

def cbfnButtonOpenRaw():
    global txtlblRawFName, btnRaw, rawdata
    txtlblRawFName.set(value=filedialog.askopenfilename() )
    rawfname = txtlblRawFName.get()
    #print(rawfname)
    try:
        f = open(rawfname, 'rb')
        rawdata = f.read()
        btnRaw.config(text='Load RAW', command=cbfnButtonLoadRaw)
    except:
        messageBoxOK('FileIO', 'Failed to open file :\n' + rawfname)
    '''
    with open(rawfname, 'rb') as in_file:
        rawdata = in_file.read()
        btnRaw.config(text='Load RAW', command=cbfnButtonLoadRaw)
    '''


btnRaw = Button(winMain, text='Open RAW', command=cbfnButtonOpenRaw)
btnRaw.grid(row=0, column=0, pady=2)
txtlblRawFName = StringVar()
##txtlblRawFName.set(value='test')
lblRawFName = Label(winMain, width=48, textvariable=txtlblRawFName)
lblRawFName.grid(row=0, column=1, columnspan=8)


lblRawWidth = Label(winMain, text='Width')
lblRawWidth.grid(row=1, column=0, pady=2)
txtlblRawWidth = StringVar(value='1920')
entryRawWidth = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawWidth)
entryRawWidth.grid(row=1, column=1, sticky=W)

lblRawHeight = Label(winMain, text='Height')
lblRawHeight.grid(row=2, column=0, pady=2)
txtlblRawHeight = StringVar(value='1080')
entryRawHeight = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawHeight)
entryRawHeight.grid(row=2, column=1, sticky=W)


def ShowChoice():
    global bayerSelect
    print(bayerSelect.get())

lblRawBayer = Label(winMain, text='Bayer')
lblRawBayer.grid(row=1, column=3, pady=2)
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

lblRawBits = Label(winMain, text='Pixel Bits')
lblRawBits.grid(row=3, column=0, padx=2, pady=2)
txtlblRawBits = StringVar(value='10')
entryRawBits = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawBits)
entryRawBits.grid(row=3, column=1, sticky=W)

varBytePack = IntVar(value=0)
chkBytePack = Checkbutton(winMain, text='Packed', variable=varBytePack)
chkBytePack.grid(row=4, column=1, sticky=W)



winMain.mainloop()

