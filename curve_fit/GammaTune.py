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
from curve_ubox import CurveCXP, CurveSplineFit

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



#------------------------------------------------------------------------------------
# class CallbackCXPMGR
#------------------------------------------------------------------------------------
class CallbackCXPMGR:
	"""This is the class defined as a callback object to MainGUI curve control points.
	@param 
	"""
	def __init__(self, debug=False):
		pass

	def button_callback(self, btn_name):
		"""The callback of the requested (btn_name) button.
		@param	btn_name		'add', 'prev', 'next', del'
		"""
		print("Button {} is pressed.".format(btn_name) )
		pass

#############################################
# Main thread functions
#############################################

#------------------------------------------------------------------------------------
# onClose()
#------------------------------------------------------------------------------------
def onClose():
	global tkRoot
	tkRoot.quit()
	tkRoot.destroy()
	pass



#------------------------------------------------------------------------------------
# initialize_active_point()
#------------------------------------------------------------------------------------
def initialize_active_point():
	global ctrl_buttons, curveCXP, mainGUI, curve_fig

	#-- get current control point
	index = ctrl_buttons.get_active_index()
	point = curveCXP.get_point(index)

	#-- set x-bar, y-bar accordingly
	mainGUI.xBar.set(point[0])
	mainGUI.yBar.set(point[1])

	#-- draw cross line at current control point
	x_range = range(curveCXP.x_min, curveCXP.x_max)
	y_range = range(curveCXP.y_min, curveCXP.y_max)
	_draw_cross_line(curve_fig, point,  x_range, y_range)

	pass

#------------------------------------------------------------------------------------
# update_active_point()
#------------------------------------------------------------------------------------
def update_active_point(ctrlButtons, curveCXP):
	# print(ctrlButtons.buttonObject.get_value())
	# print(ctrlButtons.get_active_index())
	active_index = ctrlButtons.get_active_index()
	pass


###########################################
# Main thread Entry
###########################################

#----------------------------------------------------
# MainGUI Initialization
#----------------------------------------------------
print("[INFO] Starting main GUI...")
tkRoot = TK.Tk()
tkRoot.wm_protocol("WM_DELETE_WINDOW", onClose)
mainGUI = MainGUI(tkRoot)

#-- Load control points configuration
if sys.argv[1]:
	f_gma_file = sys.argv[1]
	mainGUI.load_curveCXP(f_gma_file)
	# curveCXP = CurveCXP(pt_file=f_gma_points, debug=True)
	print("[INFO] Found and loaded gamma sample points ...")

# #-- format the text list of the points
# if curveCXP:
# 	cxpPoints = curveCXP.points

print("[INFO] Updating CXP buttons ...")
mainGUI.update_CXP_buttons()
# ctrl_buttons = mainGUI.ctrlButtons
# texts = []
# X = []
# Y = []
# for i, p in enumerate(cxpPoints):
# 	texts.append("P{:<2d}: X={:<3d}, Y={:<3d}".format(i, p[0], p[1]))
# 	X.append(p[0])
# 	Y.append(p[1])
# ctrl_buttons.set_button_text(texts, idx=-1)

#-- fit curve
print("[INFO] Fitting curve ...")
mainGUI.fit_spline_curve()
# curve_fit = CurveSplineFit(X, Y, deg=3)
# curve_x, curve_y = curve_fit.get_curve()

print("[INFO] Plotting curve ...")
mainGUI.plot_fitted_curve()
# curve_fig = mainGUI.curveFig
# if False:
# 	print("--- X: ",X)
# 	print("--- Y: ",Y)
# 	print("--- x: ",curve_x)
# 	print("--- y: ",curve_y)
# curve_fig.plot(X, Y, 'o', curve_x, curve_y)

#----------------------------------------------------------------------
# Draw cross line on current active point
#----------------------------------------------------------------------
mainGUI.update_active_cxp(set_xyBar=True)
# initialize_active_point()

#-- register CXPMGR button command callback
CxpMGR = CallbackCXPMGR()
mainGUI.set_CXPMGR_callback(CxpMGR)

print("[INFO] Updating figure ...")
curve_plt = mainGUI.curveForm
curve_plt.update_figure()

#----------------------------------------------------
# Main Loop
#----------------------------------------------------
tkRoot.mainloop()
