# -*- encode: utf-8 -*-
import tkinter as TK
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


from cyTkGUI.cy_ViPanel import tkViPanel
from cyTkGUI.cy_ViPanel import tkV3Frame, tkH3Frame,  tkH2Frame, tkV2Frame
from cyTkGUI.cy_tkButtons import XsvButtonStack, tkButton
from cyTkGUI.cy_tkMatplot import tkMatplotFigure
from cy_Utils.cy_TimeStamp import TimeStamp

from curve_ubox import CurveCXP, CurveSplineFit



#----------------------------------------------------------------------
# Main GUI
#----------------------------------------------------------------------
class MainGUI:
	"""
	Atrributes:
		@param	curveCXP		the curve control points class (CurveCXP) object

	"""
	def __init__(self, tkRoot):
		self.Tk_mainloop(tkRoot)

		self.curveCXP = CurveCXP()
		self.cxpPoints = None
		self.cxp_min_Xstep = 4
		self.cxp_min_Ystep = 4

		self.fitted_X = None
		self.fitted_Y = None

		self.cxpmgr_callback  = None
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
				self.button_AddPoint.set_command(lambda: self.btnCommand_CXPMGR('add'))
				self.button_AddPoint.pack()

				#-- MoveUp button
				self.button_MoveUp = tkButton(self.cxFrames[0], photo="images/BTN_up.gif")
				self.button_MoveUp.set_command(lambda: self.btnCommand_CXPMGR('prev'))
				self.button_MoveUp.pack()

				#-- MoveDown button
				self.button_MoveDown = tkButton(self.cxFrames[0], photo="images/BTN_down.gif")
				self.button_MoveDown.set_command(lambda: self.btnCommand_CXPMGR('next'))
				self.button_MoveDown.pack()

				#-- DelPoint button
				self.button_DelPoint = tkButton(self.cxFrames[0], photo="images/BTN_minus.gif")
				self.button_DelPoint.set_command(lambda: self.btnCommand_CXPMGR('del'))
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

	def load_curveCXP(self, cxpFile):
		"""@brief	to load the control points of the curve from the input file.
		@param	cxpFile		name/path of the file (txt or json)
		"""
		self.cxpPoints =  self.curveCXP.load_curve_points(cxpFile)
		pass


	def update_CXP_buttons(self):
		"""@brief	to update the CXP buttons.
		"""
		if self.cxpPoints is None:
			raise Exception('Failed to load curve CXP!!')
			return

		texts = []
		for i, p in enumerate(self.cxpPoints):
			texts.append("P{:<2d}: X={:<3d}, Y={:<3d}".format(i, p[0], p[1]))
			pass

		buttons = self.ctrlButtons
		buttons.set_button_text(texts, idx=-1)
		pass


	def fit_spline_curve(self):
		"""@brief	to fit the curve on the CXP with spline fitting.
		"""
		if self.curveCXP.cxp_X is None or self.curveCXP.cxp_Y is None:
			raise Exception('Curve CXP does not exist!!')
			return

		cxpX, cxpY = self.curveCXP.cxp_X, self.curveCXP.cxp_Y
		splineFit = CurveSplineFit(cxpX, cxpY, deg=3)
		self.fitted_X, self.fitted_Y = splineFit.get_curve()
		pass


	def plot_fitted_curve(self):
		"""@brief		to draw the fitting curve
		"""
		cxpX, cxpY = self.curveCXP.cxp_X, self.curveCXP.cxp_Y
		fittedX, fittedY = self.fitted_X, self.fitted_Y
		self.curveFig.plot(cxpX, cxpY, 'o', fittedX, fittedY)
		pass


	def _draw_cross_line(self, fig, point, x_range, y_range):
		"""
		@param	fig										the figure to draw cross lines
		@param	point								the control point in (x, y) tuple
		@param	x_range, y_range		python range object.
		"""
		vline_x = [point[0] for i in y_range]
		vline_y = [i for i in y_range]

		hline_x = [i for i in x_range]
		hline_y = [point[1] for i in x_range]

		fig.plot(point[0], point[1], 'o',  color='red')
		fig.plot(vline_x, vline_y, color='red', linewidth=2, linestyle='dotted')
		fig.plot(hline_x, hline_y, color='red', linewidth=2, linestyle='dotted')
		pass


	def update_active_cxp(self, set_xyBar=False):
		"""
		"""
		index = self.ctrlButtons.get_active_index()
		x, y = self.cxpPoints[index]

		#-- set x-bar, y-bar accordingly
		if set_xyBar:
			self.xBar.set(x)
			self.yBar.set(y)

		#-- draw cross line at current control point
		x_range = range(self.curveCXP.x_min, self.curveCXP.x_max)
		y_range = range(self.curveCXP.y_min, self.curveCXP.y_max)
		self._draw_cross_line(self.curveFig, (x, y),  x_range, y_range)
		pass


		def btnCommand_CXP_add(self):
			""" """
			index = self.ctrlButtons.get_active_index()
			#-- Validate Add operation.
			if self.ctrlButtons.num_active == self.ctrlButtons.num_btn:
				print("Warning, no more space to add another ponit!!")
				return

			if index == self.ctrlButtons.num_active-1:
				print("Warning, it's the last point !!")
				return

			cur_p = self.cxpPoints[index]
			next_p = self.cxpPoints[index+1]

			cur_x, cur_y = cur_p
			next_x, next_y = next_p


			pass

	def btnCommand_CXPMGR(self, btn_name):
		"""
		@param	btn_name		'add', 'prev', 'next', 'del' correspond to CXPMGR buttons.
		"""
		print("Button {} is pressed.".format(btn_name) )

		if btn_name == 'add':

			pass
		elif btn_name == 'del':
			pass
		elif btn_name == 'prev':
			pass
		elif btn_name == 'next':
			pass
		else:
			print("ERROR, illegal button ID {} !!".format(btn_name))
			return

		pass


	def get_figure(self):
		return self.curveFig

