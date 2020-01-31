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
	"""
	def __init__(self, tkRoot):
		self.Tk_mainloop(tkRoot)

		self.CurveCXP = None
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

	def set_CXPMGR_callback(self, cxpmgr):
		self.cxpmgr_callback = cxpmgr.button_callback
		pass


	def btnCommand_CXPMGR(self, btn_name):
		if self.cxpmgr_callback is None:
			print("[ERROR] cxpmgr_callback is not defined !!")
			return
		
		self.cxpmgr_callback(btn_name)
		pass


	def get_figure(self):
		return self.curveFig

