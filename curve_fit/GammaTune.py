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

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#---- Use site-packages modules


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
	def __init__(self, tkRoot):
		self.Tk_mainloop(tkRoot)
		pass


	def Tk_mainloop(self, root):
		self.root = root

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

				self.curveForm = tkMatplotFigure(self.tuneH1Frames[1], figsize=(480, 480, 80), debug=True)
				self.curveFig = self.curveForm.get_current_subplot()

				self.xBar = TK.Scale(self.tuneFrames[1], orient='horizontal', from_=0, to=255, length=300)
				self.xBar.pack(fill=TK.BOTH, expand=TK.YES)



	def get_figure(self):
		return self.curveFig


#---------------------------------------------------------
# Class curvePoints
#---------------------------------------------------------
class curvePoints:
	"""
	"""
	def __init__(self, pt_file="", name="", debug=False):
		self.points= None	#-- the list of all points loaded
		self.debug = debug

		if pt_file:
			if debug:
				print("Loading curve points from file", pt_file)
			self.load_curve_points(pt_file)
		pass


	def _load_txt_points(self, pt_file):
		X = []
		Y = []
		with open(pt_file, "r")  as f:
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
		return len(X), X, Y


	def load_curve_points(self, pt_file):
		type = pt_file[-4:].lower()
		if type == '.txt':
			if self.debug:
				print("Curve points from TXT format.")
			n_points, X, Y = self._load_txt_points(pt_file)
		else:
			#-- for json file
			pass

		self.n_points = n_points
		self.raw_X	= X		#-- it's string type
		self.raw_Y = Y		#-- it's string type

		if self.points is None:
			self.points = list()	#-- create the list
		else:
			self.points[:] = []		#-- clear the list

		for i in range(0, n_points):
			x =  int(X[i]) if X[i].find('.') < 0 else float(X[i])	#-- (we only accept integer or float value)
			y =  int(Y[i]) if Y[i].find('.') < 0 else float(Y[i])
			self.points.append( (x, y) )
			pass


#---------------------------------------------------------
# Class CurveSplineFit
#---------------------------------------------------------
class CurveSplineFit:
	"""Fitting curve with cubic spline
	@param	X, Y		List containing values of coordinate X, Y.\n
						[Note]: The first and last elements of X list is considered
								as the beginning and end points of the fitted curve.
	@param	step		The increametal value on X coordinate while generating
						new curve point sequence.
	@param	deg			The degree of the spline curve
	"""
	def __init__(self, X, Y, step=1, deg=3):
		#--------------------------------------------------------------------
		#-- conduct sci cubic spline fitting
		#--------------------------------------------------------------------
		#-- 找出 spline 的 t(vector knots 節點), c(spline coefficients 係數), k(degree of spline 階數)
		self.degree = deg
		self.step = step
		self.new_x, self.new_y = self._fit_curve(X, Y, self.degree, self.step)
		pass

	def _fit_curve(self, X, Y, deg, step):
		tck = spi.splrep(X, Y, k=deg)

		#-- 用 PPoly.from_spline 來查看 spline 每個分段函數的係數
		if False: #-- for further understanding
			pp = spi.PPoly.from_spline(tck)
			print(pp.c.T)

		#-- 求出整條 curve 的值
		new_x = [x for x in range(X[0], X[-1]+step, step)]
		new_y = spi.splev(new_x, tck)
		return new_x, new_y

	def get_curve(self):
		return self.new_x, self.new_y

	def update_XY(self, X, Y, step=0, deg=0):
		self.degree = self.degree if deg == 0 else degree
		self.step = self.step if step == 0 else step
		self.new_x, self.new_y = self._fit_curve(X, Y, self.degree, self.step)
		return self.new_x, self.new_y



#---------------------------------------------------------
# Main thread functions
#---------------------------------------------------------
def onClose():
	global tkRoot
	tkRoot.quit()
	tkRoot.destroy()
	pass


#---------------------------------------------------------
# Main thread Entry
#---------------------------------------------------------

#----------------------------------------------------
# MainGUI Initialization
#----------------------------------------------------
print("[INFO] Starting main GUI...")
tkRoot = TK.Tk()
mainGUI = MainGUI(tkRoot)

tkRoot.wm_protocol("WM_DELETE_WINDOW", onClose)

#-- Load control points configuration
if sys.argv[1]:
	f_gma_points = sys.argv[1]
	curvePoints = curvePoints(pt_file=f_gma_points, debug=True)
	print("[INFO] Found and loaded gamma sample points ...")

#-- format the text list of the points
if curvePoints:
	ctrl_points = curvePoints.points


ctrl_buttons = mainGUI.ctrlButtons
texts = []
X = []
Y = []
for i, p in enumerate(ctrl_points):
	texts.append("P{:<2d}: X={:<3d}, Y={:<3d}".format(i, p[0], p[1]))
	X.append(p[0])
	Y.append(p[1])
ctrl_buttons.set_button_text(texts, idx=-1)

#-- fit curve
print("[INFO] Fitting curve ...")
curve_fit = CurveSplineFit(X, Y, 1)
curve_x, curve_y = curve_fit.get_curve()

print("[INFO] Plotting curve ...")
curve_fig = mainGUI.curveFig
if False:
	print("--- X: ",X)
	print("--- Y: ",Y)
	print("--- x: ",curve_x)
	print("--- y: ",curve_y)
# plt.plot()
curve_fig.plot(X, Y, 'o', curve_x, curve_y)
# curve_fig.xlim(0, 256)

print("[INFO] Updating figure ...")
curve_plt = mainGUI.curveForm
curve_plt.update_figure()

#----------------------------------------------------
# Main Loop
#----------------------------------------------------
tkRoot.mainloop()
