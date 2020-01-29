# -*- encoding: utf-8 -*-

import math
import numpy as np
import time

import tkinter as TK
from PIL import Image
from PIL import ImageTk

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# mpl.rcParams['font.sans-serif'] = ['SimHei']		#-- 中文顯示
# mpl.rcParams['axes.unicode_minus']=False			#-- 顯示負號

# if __name__ == "__main__":
# 	from cy_ViPanel import tkRadioButton
# else:
# 	from cyTkGUI.cy_ViPanel import tkRadioButton

#---------------------------------------------------------------------------------------------------



class tkMatplotFigure:
	"""
	@param	figsize		A tuple (width, height, dpi) to specify the size of the figure.
						Be aware of both width and height are given in pixels.
						It is different from the matplot.figure() where figsize is given in inches.
	@param
	"""
	def __init__(self, root, figID=2, figsize=(240, 90, 20), n_sub=1, figname="", debug=False):
		self.debug = debug

		if self.debug:
			print("[tkMatplotFigure] figname={}, figsize={}x{}, dpi={}, subplot={}, figID={}".format(
						figname, figsize[0], figsize[1], figsize[2], n_sub, figID) )
	
		self.figname = "tkMatplotFigure" if figname ==""  else figname
		self.root=root						#-- 创建主窗体

		dpi = int(figsize[2])
		fig_w = figsize[0]/dpi
		fig_h = figsize[1]/dpi
		self.figID = figID

		if self.debug:
			print("[tkMatplotFigure] creating figure ... {}x{} inches, dpi={}".format(fig_w, fig_h, dpi) )
		self.figure = None
		self.figure = self.create_matplotlib(figsize=(fig_w, fig_h), dpi=int(figsize[2]))		#-- 返回matplotlib所画图形的figure对象

		self.fig_toolbar = None
		self.canvas = None
		self.create_figure_canvas()			#-- 将figure显示在tkinter窗体上面


	def get_figure(self):
		return self.figure

	def get_current_subplot(self):
		return self.figure.gca()


	def create_matplotlib(self, figsize=(3,3), dpi=80):
		#-- 创建绘图对象f
		f=plt.figure(num=2, figsize=figsize, dpi=80)		#-- , facecolor="pink", edgecolor='green', frameon=True)
		#创建一副子图
		self.ax1=plt.subplot(1,1,1)		#-- create a subfigure at (row=1, column=11, index=1)

		# x=np.arange(0,2*np.pi,0.1)
		# y1=np.sin(x)
		# y2=np.cos(x)

		# line1,=fig1.plot(x,y1,color='red',linewidth=3,linestyle='--')	#画第一条线
		# line2,=fig1.plot(x,y2)
		# plt.setp(line2,color='black',linewidth=8,linestyle='-',alpha=0.3)#华第二条线

		# fig1.set_title("这是第一幅图",loc='center',pad=20,fontsize='xx-large',color='red')	#设置标题
		# line1.set_label("正弦曲线")														   #确定图例
		# fig1.legend(['正弦','余弦'],loc='upper left',facecolor='green',frameon=True,shadow=True,framealpha=0.5,fontsize='xx-large')

		# fig1.set_xlabel('横坐标')															 #确定坐标轴标题
		# fig1.set_ylabel("纵坐标")
		# fig1.set_yticks([-1,-1/2,0,1/2,1])												   #设置坐标轴刻度
		# fig1.grid(which='major',axis='x',color='r', linestyle='-', linewidth=2)			  #设置网格

		return f


	def create_figure_canvas(self, toolbar=False):
		#把绘制的图形显示到tkinter窗口上
		if self.debug:
			print("[{}] creating tkinter-canvas for matplot-figure ...".format(self.figname) )

		if self.canvas is None:
			self.canvas=FigureCanvasTkAgg(self.figure, self.root)

		if self.canvas is None:
			print("[{}] Error, Null canvas !!".format(self.figname) )
			return 

		if self.debug:
			print("[{}] drawing canvas ... ".format(self.figname) )
		self.canvas.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
		self.canvas.get_tk_widget().pack(side=TK.TOP, fill=TK.BOTH, expand=TK.YES)

		#把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
		if toolbar is True and self.fig_toolbar is not None:
			self.fig_toolbar =NavigationToolbar2Tk(self.canvas, self.root) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
			self.fig_toolbar.update()

		self.canvas.get_tk_widget().pack(side=TK.TOP, fill=TK.BOTH, expand=TK.YES)
		pass


	def update_figure(self):
		#把绘制的图形显示到tkinter窗口上
		# self.canvas=FigureCanvasTkAgg(figure, self.root)
		if self.canvas is None:
			raise Exception('Error', 'Null canvas !!')
			exit()

		self.canvas.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
		# self.canvas.get_tk_widget().pack(side=TK.TOP, fill=TK.BOTH, expand=TK.YES)

		#把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
		# toolbar =NavigationToolbar2Tk(self.canvas, self.root) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
		# toolbar.update()
		# self.canvas._tkcanvas.pack(side=TK.TOP, fill=TK.BOTH, expand=1)
		pass


if __name__ == "__main__":
	#---------------------------------------------------------------------------------
	def onClose():
		global tkRoot

		tkRoot.quit()
		tkRoot.destroy()

	idx = 0
	def draw_curve(fig1):
		global idx

		x=np.arange(0,2*np.pi,0.1)
		y1=np.sin(x)
		y2=np.cos(x)

		if idx==0:
			line1,=fig1.plot(x,y1,color='red',linewidth=3,linestyle='--')	#画第一条线
			line1.set_label("sine")														   #确定图例
		else:
			line2,=fig1.plot(x,y2)
			plt.setp(line2,color='black',linewidth=8,linestyle='-',alpha=0.3)#华第二条线

		idx = 1 if idx == 0 else 0
		fig1.set_title("Figure 1",loc='center',pad=20,fontsize='xx-large',color='red')	#设置标题
		fig1.legend(['sin()','cos()'],loc='upper left',facecolor='green',frameon=True,shadow=True,framealpha=0.5)	#-- ,fontsize='xx-large'

		fig1.set_xlabel('X-axes')															 #确定坐标轴标题
		fig1.set_ylabel("Y-axes")
		fig1.set_yticks([-1,-1/2,0,1/2,1])												   #设置坐标轴刻度
		fig1.grid(which='major',axis='x',color='r', linestyle='-', linewidth=2)			  #设置网格


	def CMD_buttonUpdate(tkplt):
		print("Update plot ...")
		fig = tkplt.get_figure().gca()
		fig.clear()
		draw_curve(fig)
		tkplt.update_figure()
		pass
	#---------------------------------------------------------------------------------


	tkRoot = TK.Tk()
	tkRoot.wm_protocol("WM_DELETE_WINDOW", onClose)

	tkPlot = tkMatplotFigure(tkRoot)
	fig1 = tkPlot.get_figure().gca()

	if True:
		draw_curve(fig1)
		pass

	buttonUpdate = TK.Button(tkRoot, text="Update", command= lambda: CMD_buttonUpdate(tkPlot))
	buttonUpdate.pack(side=TK.TOP)
	tkRoot.mainloop()

	print("---aaa")
	pass
