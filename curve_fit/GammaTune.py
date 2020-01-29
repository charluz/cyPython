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

from mainGUI import MainGUI

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

	def get_point(self, index):
		override = 1
		idx = index
		if index < 0 :
			idx = 0
		elif index >= self.n_points:
			idx = self.n_points -1
		else:
			override = 0
		
		if override:
			print("Warning: illegal index {}, overriden to {}".format(index, idx))

		return self.points[idx]


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
		print("[SplineFit] step={}, degree={}".format(step, deg))
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


def initialize_active_point():
	global ctrl_buttons, curvePoints, mainGUI

	#-- get current control pont
	index = ctrl_buttons.get_active_index()
	point = curvePoints.get_point(index)

	#-- set x-bar, y-bar accordingly
	mainGUI.xBar.set(point[0])
	mainGUI.yBar.set(point[1])
	pass

def update_active_point(ctrlButtons, curvePoints):
	# print(ctrlButtons.buttonObject.get_value())
	# print(ctrlButtons.get_active_index())
	active_index = ctrlButtons.get_active_index()


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
curve_fit = CurveSplineFit(X, Y, deg=3)
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

#----------------------------------------------------------------------
# Draw cross line on current active point
#----------------------------------------------------------------------
initialize_active_point()


print("[INFO] Updating figure ...")
curve_plt = mainGUI.curveForm
curve_plt.update_figure()

#----------------------------------------------------
# Main Loop
#----------------------------------------------------
tkRoot.mainloop()
