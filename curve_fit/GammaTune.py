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
# from cyTkGUI.cy_tkButtons import XsvButtonStack

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
				self.actionFrames = tkH3Frame(self.cxFrames[0]).Frames
				# self.pointsFrames = XsvButtonStack(self.cxFrames[1])

			self.tuneFrames = tkV2Frame(self.multiFrames[1]).Frames
			if self.tuneFrames:
				self.tuneH1Frames = tkH2Frame(self.tuneFrames[0]).Frames
				self.yBar = TK.Scale(self.tuneH1Frames[0], from_=0, to=255)
				# self.graph = 

				self.tuneH2Frames = tkH2Frame(self.tuneFrames[1]).Frames
				self.xBar = TK.Scale(self.tuneH2Frames[1], orient='horizontal', from_=0, to=255)

			print("---> ")
			self.root.mainloop()




#---------------------------------------------------------
# Main thread functions
#---------------------------------------------------------


def onClose():
	global evAckClose
	evAckClose.set()
	# print("---- Set ----")

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

#----------------------------------------------------
# Main Loop
#----------------------------------------------------
while True:
	if evAckClose.isSet():
		break


cv2.destroyAllWindows()
