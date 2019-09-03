#!/usr/bin/python

import os, sys

from tkinter import *  # Tk, Label, Entry, Radiobutton, IntVar, Button
from tkinter import filedialog
import cv2

import numpy as np
# import matplotlib.pyplot as plt

'''
from tkFileDialog import askopenfilename

That code would have worked fine in Python 2.x, but it is no longer valid.
In Python 3.x, tkFileDialog was renamed to filedialog.
'''

gImgRepoRoot = repr(os.getcwd())
gImgRepoCurr = gImgRepoRoot
gRawBaseName = ""




###########################################################
# Message Box with OK button
###########################################################
def messageBoxOK(title, msg):
	global textvarStatusBar
	if False:
		box = Toplevel()
		box.title(title)
		Label(box, text=msg).pack()
		Button(box, text='OK', command=box.destroy).pack()
	else:
		sz = title+': '+msg
		print(sz)
		textvarStatusBar.set(sz)



###########################################################
# Functions : Create working folders
###########################################################
def createDirectory(name):
	if not os.path.exists(name):
		try:
			os.mkdir(name)
		except:
			messageBoxOK("Error", "Can't create folder : \n"+repr(name))
			return ""
		print("Directory ", name, " created.")
	else:
		print("Directory ", name, " already exists.")

	return name



def createImageRepoRoot(cwd, name):
	# print(cwd + name)
	return createDirectory(cwd+name)


###########################################################
# Function : Callback of Button RESET
###########################################################
def cbfnButtonReset():
	cv2.destroyAllWindows()
	btnRaw.config(text='Open RAW', command=cbfnButtonOpenRaw, bg='LightGreen')
	textvarStatusBar.set("")



def save_raw_XXXX_image(img1, img2, img3, img4):
	messageBoxOK('ERROR', 'Unknown bayer type !!')


###########################################################
# Function : Split Bayer Components
###########################################################
def showBenImage(bayerdata, width, height):
	'''
	@Brief
		To split R/Gr/Gb/B components from Bayer Raw image input.
	@In
		bayerdata   : Raw image input (from io.open/io.read)
		width, height   : size of Raw image
		rawBits	 : number of bits per pixel
	@Out
		boolean : indicating success/failure
	@Globals
		bayerImgC1, bayerImgC2, bayerImgC3, bayerImgC4 : sub-images of R/Gr/Gb/B.
			Size of sub-image is (widht/2, height/2).
	'''
	imgW, imgH = int(width), int(height)
	if False:
		#-- to create a test array
		size = imgW * imgH * 3
		bayerdata = bayerdata[:size]

	benImage = bayerdata.reshape((imgH, imgW, 3))
	benImage = cv2.cvtColor(benImage, cv2.COLOR_RGB2BGR)
	cv2.imshow("benImage", benImage)

	btnRaw.config(bg='Coral')


	btnRaw.config(text='RESET', command=cbfnButtonReset, bg='LightBlue')

	return True


###########################################################
# Button Function : LoadRAW
###########################################################
def cbfnButtonLoadRaw():
	global btnRaw, rawdata
	print("Button: Load RAW")
	try:
		#print("--- A ---")
		showBenImage(rawdata, int(txtlblRawWidth.get()), int(txtlblRawHeight.get()))
		#print("--- B ---")
	except:
		cbfnButtonReset()
		return

###########################################################
# Button Function : OpenRAW
###########################################################
def cbfnButtonOpenRaw():
	global winMain, winTitle, txtlblRawFName, btnRaw, btn
	global rawdata, rawfname, gRawBaseName
	global gIsShowBayerImage, chkShowBayerImg
	global gIsShowRawImage, chkShowRawImg
	global gIsShowRawRGB, chkShowRawRGB

	rawfname = filedialog.askopenfilename()
	#print(rawfname)
	try:
		# f = open(rawfname, 'rb')
		# rawdata = f.read()
		# f.close()
		rawdata = np.fromfile(rawfname, dtype=np.uint8)
	except:
		messageBoxOK('FileIO', 'Failed to open file :\n' + rawfname)
		cbfnButtonReset()
		return

	# Create root repository folder for output images
	gImgRepoRoot = os.path.dirname(rawfname)
	os.chdir(gImgRepoRoot)
	gImgRepoRoot = createImageRepoRoot(gImgRepoRoot, "/_imageRepo")
	# print(gImgRepoRoot)

	# Create folder to save output images for loaded RAW image
	baseName = os.path.basename(rawfname)

	base, ext = os.path.splitext(baseName)
	gImgRepoCurr = gImgRepoRoot + "/" + base
	#print("Target image repo ", gImgRepoCurr)
	if createDirectory(gImgRepoCurr):
		os.chdir(gImgRepoCurr)

	gRawBaseName = base
	#print(gRawBaseName)

	# modify title of main window
	winMain.title(winTitle+ ' -- ' + baseName)

	# to Load and Parse RAW images
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
# RAW Format JSON Parser
###########################################################
def raw_format_json_load():
	import json
	global gRawFmtTable

	#jsonDict = {}
	try:
		with open("./raw_format.json") as f:
			jsonDict = json.load(f)
	except:
		jsonDict = None

	if jsonDict:
		gRawFmtTable["showBayerColor"] = jsonDict["showBayerColor"]
		gRawFmtTable["showRawGray"] = jsonDict["showRawGray"]
		gRawFmtTable["width"] = jsonDict["width"]
		gRawFmtTable["height"] = jsonDict["height"]
		gRawFmtTable["bits"] = jsonDict["bits"]
		gRawFmtTable["bayer"] = jsonDict["bayer"]

	return jsonDict

###########################################################
# MainEntry
###########################################################

if __name__ == "__main__":
	global textvarStatusBar

	winTitle = 'Raw Viewer'
	winMain = Tk()
	winMain.title(winTitle)
	#winMain.geometry('500x200')

	curRow, curCol = 0, 0
	#####################################
	# Button : Open RAW
	#####################################
	btnRaw = Button(winMain, text='Open RAW', command=cbfnButtonOpenRaw, bg='LightGreen')
	btnRaw.grid(row=curRow, column=0, pady=2)

	#####################################
	# Buttons : Platform RAW Config
	#####################################
	gRawFmtTable = {
		"showBayerColor"	: False,
		"showRawGray"	   : True,
		"showRawRGB"		: False,
		"width"		 : 1600,
		"height"		: 1200,
		"bits"		  : 8,
		"bayer"		 : 3,
	}

	raw_format_json_load()

	curRow +=1
	lblRawWidth = Label(winMain, text='Width')
	lblRawWidth.grid(row=curRow, column=0, pady=2)
	txtlblRawWidth = StringVar(value=gRawFmtTable["width"])
	entryRawWidth = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawWidth)
	entryRawWidth.grid(row=curRow, column=1, sticky=W)

	curRow +=1
	lblRawHeight = Label(winMain, text='Height')
	lblRawHeight.grid(row=curRow, column=0, pady=2)
	txtlblRawHeight = StringVar(value=gRawFmtTable["height"])
	entryRawHeight = Entry(winMain, bd=2, justify=LEFT, width=10, textvariable=txtlblRawHeight)
	entryRawHeight.grid(row=curRow, column=1, sticky=W)

	curRow += 2
	# Button : Exit
	btnExit = Button(winMain, text='-- EXIT --', command=cbfnButtonMainExit, fg='Yellow', bg='Red')
	btnExit.grid(row=curRow, column=0)

	curRow += 2
	textvarStatusBar = StringVar(value="")
	statusBar = Label(winMain, textvariable=textvarStatusBar, relief=SUNKEN, bd=2, anchor=W)
	statusBar.grid(row=curRow, column=0, columnspan=8, sticky=W+E, padx=4, pady=4)

	winMain.mainloop()
