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
from cyTkGUI.cy_ViPanel import tkV3Frame
from cyTkGUI.cy_tkButtons import XsvButtonStack

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
	def __init__(self, url):
		self.thread = threading.Thread(target=self.Tk_mainloop, daemon=True, args=())
		self.lock = threading.Lock()


	def Tk_mainloop(self):
		self.root = TK.Tk()

		#---------------------------------
		#-- Main layout
		#---------------------------------
		self.L1_Frames = tkV3Frame(self.root).Frames

		#---------------------------------
		# Video Panel
		#---------------------------------
		#-- Use frame#0 (upper-left) to display feyeView
		self.View = tkViPanel(self.L1_Frames[2], osdScale=1.2, size=(1280, 720))	# (720, 540), (960, 720)

		#---------------------------------
		# Connection Page
		#---------------------------------
		#-- URL
		TK.Label(self.L1_Frames[0], text="URL: ").pack(side=TK.LEFT, fill=TK.Y)
		self.txtURL = TK.StringVar()
		self.entryURL = TK.Entry(self.L1_Frames[0], width=40, bd=2, textvariable=self.txtURL)
		self.entryURL.pack(side=TK.LEFT, expand=TK.YES)
		# self.txtHost.set("192.168.1.19")
		self.txtURL.set(self.url)

		#---------------------------------
		# Start/Stop Button
		#---------------------------------
		# #-- LabelFrame
		# self.calibFrame = TK.LabelFrame(self.quadFrames[3], text="Calibration")
		# self.calibFrame.pack(expand=TK.YES)

		#-- Start/Stop button
		self.btnStart = TK.Button(self.L1_Frames[1], width=20, text="START", state=TK.NORMAL, command=self.command_btnStart)
		self.btnStart.pack(expand=TK.YES)

		self.root.mainloop()


	def command_btnStart(self):
		if self.liveStart:
			# print("--- btnSTOP ---")
			self.liveStart = False
			self.btnStart.configure(text="START")
		else:
			# print("--- btnSTART ---")
			self.liveStart = True
			self.btnStart.configure(text="STOP")



#---------------------------------------------------------
# Main thread functions
#---------------------------------------------------------

def stream_get_jpeg(stream):
	# TS.SubStart()
	#----------------------------------------------
	# 向 server 提取影像
	#----------------------------------------------
	buff = bytearray(b'')
	while True:
		# buff.append(stream.read(1024)) #-- append() can only add one interger
		buff.extend(stream.read(1024))

		#----------------------------------------------
		if False: #-- DEBUG Only
			strm_bytes = buff
			print("Type[strm_bytes]: ", type(strm_bytes))
			sz =strm_bytes.decode('ascii')
			print("Type[sz]: ", type(sz))
			break

		#-- find Start of JPEG
		jpg_start = buff.find(b'\xff\xd8')
		if jpg_start == -1:
			# print("START: buff size= ", len(buff))
			buff = bytearray(b'')
			continue
		# print("Found JPG start@ ", jpg_start)
		buff = buff[jpg_start:]

		#-- find End of JPEG
		jpg_end = buff.find(b'\xff\xd9')
		if jpg_end == -1:
			# print("**END: buff size= ", len(buff))
			# print("**jpg_end= ", jpg_end)
			continue
		# print("Found JPG end@ ", jpg_end)

		jpg = buff[jpg_start:jpg_end+2]
		buff = buff[jpg_end+2:]

		img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), flags=1) #-- flags=1 for color image
		break

	return True, img


def url_open_stream(url):
	try:
		stream = url_request.urlopen(url)
	except:
		return None
	return stream


def calcualte_score(img):
	# lap = cv2.convertScaleAbs(cv2.Laplacian(img, cv2.CV_16S, ksize=3))
	lap = cv2.convertScaleAbs(cv2.Laplacian(img, cv2.CV_16S, ksize=3)) #-- use cv2.CV16S to prevent from overflow )negative value)
	score = np.sum(lap)/(img.shape[0]*img.shape[1])
	return score, lap


def crop_frame_roi(frame, Vt, Vb):
	rowStart, rowEnd = Vt[1], Vb[1]+1
	colStart, colEnd = Vt[0], Vb[0]+1
	# print(rowStart, rowEnd, colStart, colEnd)
	roi_img = frame[rowStart:rowEnd, colStart:colEnd,]
	return roi_img


def implant_frame_roi(frame, roi_img, Vt, Vb):
	rowStart, rowEnd = Vt[1], Vb[1]+1
	colStart, colEnd = Vt[0], Vb[0]+1
	# print(rowStart, rowEnd, colStart, colEnd)
	frame[rowStart:rowEnd, colStart:colEnd,] = roi_img
	# return roi_img

def focusing_scoring(frame, roi_rects):
	Debug = False
	roi_scores = []
	vertices = roi_rects.get_vertex_all()

	if Debug:
		cv2.imwrite("frame.jpg", frame)

	idx = 0
	for vtx in vertices:
		roi_score = []
		# print("Vertex: {}, {}-{}".format(vtx[0], vtx[1], vtx[2]))
		Vt, Vb = vtx[1], vtx[2]

		if Debug:
			print("Vt= {}, Vb= {}".format(Vt, Vb))

		roi_img = crop_frame_roi(frame, Vt, Vb)
		score, lap_img = calcualte_score(roi_img)

		if Debug: #-- DEBUG ONLY
			cv2.imwrite("roi_{}.jpg".format(idx), roi_img)
			cv2.imwrite("lap_{}.jpg".format(idx), lap_img)

		idx += 1
		roi_score.append(vtx[0]) #-- store roi name
		roi_score.append(score/100.0)	 # store roi's focusing score
		roi_scores.append(roi_score)

		#-- 鑲嵌 edge 影像
		implant_frame_roi(frame, lap_img, Vt, Vb)

	return roi_scores


def draw_focusing(frame, roi_rects, roi_scores):
	for roi in roi_scores:
		roi_name, score = roi
		# roi_rects.set_property(roi_name, fcolor=(0, 255, 255))
		roi_rects.draw(roi_name, frame, text="{:.2f}".format(score))


#---------- For callback draw
class appCallbackDraw:
	""" A Class giving a callback function to draw slanted guiding lines on dsiplay.
	"""
	def __init__(self):
		pass

	def draw(self, cv_img):
		# print("Type(cv_img): ", cv_img.shape)
		hh, ww = cv_img.shape[:2]
		hHalf, wHalf = hh/2.0, ww/2.0
		delta_hh = int((wHalf)*math.tan(5/180.0))
		delta_ww = int((hHalf)*math.tan(5/180.0))

		#---- 水平斜5度線
		p1 = (0, int(hHalf)+delta_hh)
		p2 = (ww-1, int(hHalf)-delta_hh)
		cv2.line(cv_img, p1, p2, (0, 0, 255), 4)

		#---- 垂直斜5度線
		p1 = (int(wHalf)-delta_ww, 0)
		p2 = (int(wHalf)+delta_ww, hh-1)
		cv2.line(cv_img, p1, p2, (0, 0, 255), 4)


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

szlocal = 'local:'
localImage = ""
useLocalImage = True if args.host[:len(szlocal)] == szlocal else False
if useLocalImage:
	localImage = args.host[len(szlocal):]

#----------------------------------------------------
# MainGUI Initialization
#----------------------------------------------------

if not useLocalImage:
	# url = 'http://192.168.7.1/frame.jpeg'
	url = "http://{}".format(args.host)
	if args.port > 0:
		url += ":{}".format(args.port)
	url += "/?action=stream"

mainGUI = MainGUI(localImage if useLocalImage else url)
mainGUI.thread.start()
time.sleep(0.01)

mainGUI.root.wm_protocol("WM_DELETE_WINDOW", onClose)

TS = TimeStamp(name="QCam", enable=False, csv="tmlog_qcam.csv")
TS.ProcStart()

#----------------------------------------------------
# 讀取影像初始參數
#----------------------------------------------------
mj_stream = None
if useLocalImage:
	print("Reading {} for initial configuration...".format(localImage))
	frame_ww, frame_hh = -1, -1
	frame_img = cv2.imread(localImage)
	if frame_img is None:
		raise RuntimeError("Failed reading image from: {}".fomat(localImage))
		exit()
else:
	print("Connecting {} for initial configuration...".format(mainGUI.url))
	mj_stream = url_open_stream(mainGUI.url)
	if mj_stream is None:
		raise RuntimeError("Failed openning URL stream: {}".format(mainGUI.url))
		exit()

	frame_ww, frame_hh = -1, -1
	succ, frame_img = stream_get_jpeg(mj_stream)
	if not succ:
		raise RuntimeError("Failed capturing jpeg from: {}".fomat(mainGUI.url))
		exit()

if False: #-- DEBUG ONLY
	while True:
		succ, frame_img = stream_get_jpeg(mj_stream)
		cv2.imshow("Test", frame_img)
		Key = cv2.waitKey(15)
		if Key == 27:
			cv2.destroyAllWindows()
			exit()

frame_hh, frame_ww = frame_img.shape[:2]
frame_Vt = (0, 0)		#-- image 左上頂點
frame_Vb = (frame_ww-1, frame_hh-1)	#-- image 右下頂點
if True:
	print("frame dimension: {} x {}".format(frame_ww, frame_hh))
	print("frame vertex: {} ~ {}".format(frame_Vt, frame_Vb))


#----------------------------------------------------
# Create ROI rectangles
#----------------------------------------------------
roi_size = (int(frame_ww/10.0), int(frame_hh/10.0))
frame_CC = (int(frame_ww/2.0), int(frame_hh/2.0))	#-- 畫面中心座標
roi_rects = ROIs(frame_ww, frame_hh)
corner_field = 1.0 - 0.65

#-- 中心 ROI (Cx)
roi_rects.add("Cx", frame_CC, roi_size)

#-- 左上 ROI (Q01), field @ 0.65
Qcc = interpolateXY(frame_Vt, frame_CC, corner_field)
roi_rects.add("Q00", Qcc, roi_size)

#-- 左下 ROI (Q10), field @ 0.65
Qcc = interpolateXY((0, frame_Vb[1]), frame_CC, corner_field)
roi_rects.add("Q10", Qcc, roi_size)

#-- 右上 ROI (Q01), field @ 0.65
Qcc = interpolateXY((frame_Vb[0], 0), frame_CC, corner_field)
roi_rects.add("Q01", Qcc, roi_size)

#-- 右下 ROI (Q11), field @ 0.65
Qcc = interpolateXY(frame_Vb, frame_CC, corner_field)
roi_rects.add("Q11", Qcc, roi_size)

#----------------------------------------------------
# 註冊 Callback class 畫斜5度導引線
# !! Callback 是對 ViPanel 註冊 !!
#----------------------------------------------------
callbackDraw = appCallbackDraw()
mainGUI.View.set_callbackObj(callbackDraw)

#----------------------------------------------------
# Main Loop
#----------------------------------------------------
frame_index = 0
while True:
	if evAckClose.isSet():
		break

	if not mainGUI.liveStart:
		time.sleep(0.5)
		print("-x-", end="")
		continue


	if useLocalImage:
		img = frame_img.copy()
	else:
		#----------------------------------------------
		# 向 server 提取影像
		#----------------------------------------------
		TS.SubStart()
		succ, frame_img = stream_get_jpeg(mj_stream)
		if not succ:
			continue
		TS.SubEnd("getIMG")

		TS.SubStart()
		# print("Type - content: ", type(resp.content))
		# img_array = np.frombuffer(resp.content, dtype=np.dtype('uint8'))
		# img = cv2.imdecode(frame_img, flags=cv2.IMREAD_UNCHANGED)
		img = frame_img
		TS.SubEnd("cvtJPG")

	if True: #-- DEBUG ONLY
		#--- 計算調焦分數
		TS.SubStart()
		scores = focusing_scoring(img, roi_rects)
		TS.SubEnd("scoring")

		#--- 畫框 and 分數
		draw_focusing(img, roi_rects, scores)


	mainGUI.View.show(img, name="#{:04d}".format(frame_index))

	if frame_index == 9999:
		frame_index = 0
	else:
		frame_index += 1
	pass #-- end of if mainGUI.connected == True

	#break

cv2.destroyAllWindows()
