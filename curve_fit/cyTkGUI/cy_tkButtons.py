# -*- encoding: utf-8 -*-

import cv2
import numpy as np
import six

import tkinter as TK
from PIL import Image
from PIL import ImageTk

if __name__ == "__main__":
	from cy_ViPanel import tkRadioButton
else:
	from cyTkGUI.cy_ViPanel import tkRadioButton

#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------
# CLASS: tkButtons
#---------------------------------------------------------
class tkButton:
	"""整合 Tkinter Buntton
	@param	root		Root TK object.
	@param	photo		Image file (GIF-formatted), default is not to use button image.
	@param	state		Button initial state (TK.NORMAL or TK.DISABLE)
	"""
	def __init__(self, root, label="", photo=None, state=TK.NORMAL):
		self.btnImg = TK.PhotoImage(file=photo) if photo is not None else photo
		self.button = TK.Button(root, text=label, image=self.btnImg, state=state)
		pass

	def pack(self, side=TK.LEFT, fill=TK.BOTH, expand=TK.NO):
		self.button.pack(expand=expand, side=side, fill=fill)
		pass

	def set_command(self, command_func):
		self.button.configure(command= command_func)
		pass

	def set_text(self, label):
		self.button.configure(text=label)
		pass

	def get_button(self):
		return self.button



#---------------------------------------------------------
# CLASS: XsvButtonStack
#---------------------------------------------------------
class XsvButtonStack:
	"""
	@param	num_btn			Button 的個數
	@param	orient			Button 排列方式: "H"、"V"、"GRID" 分別對應: 水平、垂直、棋盤。
	@param	column			如果排列方式設定為 "GRID"，必須同時設定 column=N 標示棋盤的橫向個數
	"""
	def __init__(self, rootwin, num_btn=16, orient="V", column=1,
					cls_name="XBStk", debug=False):
		self.rootwin = rootwin
		self.cls_name = cls_name
		self.debug = debug

		btn_labels = [ ("----", i) for i in range(0, num_btn-1)]
		self.num_btn = num_btn
		self.orient = "H" if orient=="H" else ("GRID" if orient=="GRID" else "V")
		self.buttonObject = tkRadioButton(rootwin, buttons=btn_labels,
				pack_type=self.orient, isRadio=False )
		self.Buttons = self.buttonObject.Buttons
		pass


	def set_button_text(self, text, idx=-1):
		if idx < 0:
			n_text = len(text)
			n_buttons = len(self.Buttons)

			if n_text <= n_buttons:
				for i, btn in enumerate(self.Buttons):
					if i < n_text:
						btn.configure(state=TK.NORMAL)
						btn.configure(text=text[i])
					else:
						btn.configure(state=TK.DISABLED)
						btn.configure(text="")
			else:
				#-- n_text > n_button
				for i, btn in enumerate(self.Buttons):
					btn.configure(state=TK.NORMAL)
					btn.configure(text=text[i])
				pass
		elif idx in range(0, len(self.Buttons)):
			self.Buttons[idx].configure(state=TK.NORMAL)
			self.Buttons[idx].configure(text=text)
		else:
			if self.debug:
				print("[{}] idx({}) is illegal!!".format(self.clsName, idx))
		pass

if __name__ == "__main__":

	#--------------------------------------------------------------------
	#-- Read Gamma points
	#--------------------------------------------------------------------
	def read_ctrl_points(f_ctrls):
		X = []
		Y = []
		with open(f_ctrls, "r")  as f:
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

	#-- Read control points
	cX, cY = read_ctrl_points("gamma_pt.txt")
	cX = [int(i) for i in cX]
	cY = [int(i) for i in cY]

	#-- create exclusive buttons stack
	tkRoot = TK.Tk()
	buttonStack = XsvButtonStack(tkRoot)

	#-- update button labels (text)
	labels = list()
	for i in range(0, len(cX)):
		labels.append("{:3d},  {:3d}".format(cX[i], cY[i]))

	buttonStack.set_button_text(labels)

	tkRoot.mainloop()
	pass
