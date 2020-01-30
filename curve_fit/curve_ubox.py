# -*- encoding: utf-8 -*-

import scipy.interpolate as spi

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


#---------------------------------------------------------
# Class curvePoints
#---------------------------------------------------------
class curvePoints:
	""" A class to store all control points of the curve.
	@param	pt_file				the name-path of the file storing all control points

	= Attributes =
		- raw_X, raw_Y				x, y data in string
		- points							a list of all control points in tuple (x, y)

	= Functions =
		load_curve_points()		to load curve control points from a file.
		get_point()						get the point tuple (x, y) of the indexed point
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
		
		self.x_min, self.y_min = self.points[0][0], self.points[0][1]
		self.x_max, self.y_max = self.points[-1][0], self.points[-1][1]

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


