# -*- encoding: utf-8 -*-
"""
Gamma Tuning Tool
"""
import sys
import numpy as np
import math
import cv2, time

import tkinter as TK
import threading
# import socket
import argparse
import scipy.interpolate as spi

# import requests as req

#---- Use site-packages modules
from cyCvBox.image_ROIs import ImageROIs as ROIs
from cyCvBox.image_ROIs import interpolateXY

from cyTkGUI.cy_ViPanel import tkViPanel
from cyTkGUI.cy_ViPanel import tkV3Frame, tkH3Frame,  tkH2Frame, tkV2Frame
from cyTkGUI.cy_tkButtons import XsvButtonStack, tkButton
from cyTkGUI.cy_tkMatplot import tkMatplotFigure

from cy_Utils.cy_TimeStamp import TimeStamp


###########################################################
# Argument Parser
###########################################################
# parser = argparse.ArgumentParser()
# parser.add_argument("-m", '--host', type=str, default='192.168.137.87',
# 	help='The host machine: localhost or IP of remote machine, \
# 			or local:xxxx.jpg to use local test image file.')
# parser.add_argument("-p", '--port', type=int, default=8080,
# 	help='The port on which to connect the host')
# parser.add_argument("-j", '--jpg', type=str, default='test001.jpg',
# 	help='The jpeg file to display')
# # parser.add_argument('--jpeg_quality', type=int, help='The JPEG quality for compressing the reply', default=70)
# args = parser.parse_args()


#----------------------------------------------------------------------
# Main GUI
#----------------------------------------------------------------------
class MainGUI:
	"""
	"""
	def __init__(self):
		self.thread = threading.Thread(target=self.Tk_mainloop, daemon=True, args=())
		self.lock = threading.Lock()
		pass


	def Tk_mainloop(self):
		self.root = TK.Tk()

		#---------------------------------
		#-- Main layout
		#---------------------------------
		self.mainFrames = tkV3Frame(self.root).Frames

		#---------------------------------
		# L1-V1 fame: Menu
		#---------------------------------
		self.menubar = TK.Menu(self.mainFrames[0])
		self.root.configure(menu=self.menubar)

		#---------------------------------
		# L2-V2 frame: multi function frame (button stack, tuning panel)
		#---------------------------------
		self.multiFrames = tkH2Frame(self.mainFrames[2]).Frames
		if self.multiFrames:
			#---------------------------------
			# Action buttons and Curve control point button stack
			#---------------------------------
			self.cxFrames = tkV2Frame(self.multiFrames[0]).Frames
			if self.cxFrames:
				#-- AddPoint button
				self.button_AddPoint = tkButton(self.cxFrames[0], photo="images/BTN_plus.gif")
				self.button_AddPoint.pack()

				#-- MoveUp button
				self.button_MoveUp = tkButton(self.cxFrames[0], photo="images/BTN_up.gif")
				self.button_MoveUp.pack()

				#-- MoveDown button
				self.button_MoveDown = tkButton(self.cxFrames[0], photo="images/BTN_down.gif")
				self.button_MoveDown.pack()

				#-- DelPoint button
				self.button_DelPoint = tkButton(self.cxFrames[0], photo="images/BTN_minus.gif")
				self.button_DelPoint.pack()

				#-- Curve Control Point buttons
				self.ctrlButtons = XsvButtonStack(self.cxFrames[1])

			#---------------------------------
			# Curve graph panel and X-Y scale bar
			#---------------------------------
			self.tuneFrames = tkV2Frame(self.multiFrames[1]).Frames
			if self.tuneFrames:
				self.tuneH1Frames = tkH2Frame(self.tuneFrames[0]).Frames
				self.yBar = TK.Scale(self.tuneH1Frames[0], from_=0, to=255, length=300)
				self.yBar.pack(side=TK.LEFT, fill=TK.Y)

				self.curveForm = tkMatplotFigure(self.tuneH1Frames[1], figsize=(480, 480, 80))
				self.curveFig = self.curveForm.get_current_subplot()

				self.xBar = TK.Scale(self.tuneFrames[1], orient='horizontal', from_=0, to=255, length=300)
				self.xBar.pack(fill=TK.BOTH, expand=TK.YES)

			self.root.mainloop()


	def get_figure(self):
		return self.curveFig


#---------------------------------------------------------
# Main thread functions
#---------------------------------------------------------
def onClose():
	global evAckClose
	evAckClose.set()
	# print("---- Set ----")


def load_curve_conf(conf_file):
	X = []
	Y = []
	f_gma = conf_file
	with open(f_gma, "r")  as f:
		# for line in f.readlines():
		# 	print(line.strip())
		line = f.readline()
		while line:
			x, y = line.strip().split()
			# print(x, y)
			X.append(x)
			Y.append(y)
			line = f.readline()
	f.close()
	return X, Y

#---------------------------------------------------------
# Main thread Entry
#---------------------------------------------------------

""" ----- Initiate Main GUI ------------------------------
"""
evAckClose = threading.Event()
evAckClose.clear()

#----------------------------------------------------
# MainGUI Initialization
#----------------------------------------------------
mainGUI = MainGUI()
mainGUI.thread.start()
time.sleep(0.01)

mainGUI.root.wm_protocol("WM_DELETE_WINDOW", onClose)

#-- Load control points configuration
if sys.argv[1]:
	ctrlPoints = load_curve_conf(sys.argv[1])

#----------------------------------------------------
# Main Loop
#----------------------------------------------------
while True:
	if evAckClose.isSet():
		break
