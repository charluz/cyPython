# -*- encoding: utf-8 -*-

import tkinter as TK
from cy_ViPanel import *


def test_tkQuadFrame(tkRoot):
	QFrames = tkQuadFrame(tkRoot).Frames

	panel_TopLeft = tkViPanel(QFrames[QUAD_1])
	panel_TopLeft.show(cv2.imread("charles_001.jpg"))

	panel_BottomRight = tkViPanel(QFrames[QUAD_2])
	panel_BottomRight.show(cv2.imread("TestPic.jpg"))

	panel_TopRight = tkViPanel(QFrames[QUAD_3])
	panel_TopRight.show(cv2.imread("charles_001.jpg"))

	panel_BottomLeft = tkViPanel(QFrames[QUAD_4])
	panel_BottomLeft.show(cv2.imread("TestPic.jpg"))

	tkRoot.mainloop()
	cv2.destroyAllWindows()


def test_H2Frame(tkRoot):
	Frames = tkH2Frame(tkRoot).Frames

	imgPanel_1 = tkViPanel(Frames[LEFT])
	imgPanel_2 = tkViPanel(Frames[RIGHT])

	imgPanel_1.show(cv2.imread("charles_001.jpg"))
	imgPanel_2.show(cv2.imread("TestPic.jpg"))

	tkRoot.mainloop()
	cv2.destroyAllWindows()


def test_V2Frame(tkRoot):
	Frames = tkV2Frame(tkRoot).Frames

	imgPanel_1 = tkViPanel(Frames[TOP])
	imgPanel_2 = tkViPanel(Frames[BOTTOM])

	imgPanel_1.show(cv2.imread("charles_001.jpg"))
	imgPanel_2.show(cv2.imread("TestPic.jpg"))

	tkRoot.mainloop()
	cv2.destroyAllWindows()



def test_TriFrame(tkRoot):
	Frames = tkTriFrame(tkRoot).Frames

	imgPanel_1 = tkViPanel(Frames[TRI_TOP])
	imgPanel_2 = tkViPanel(Frames[TRI_LEFT])
	imgPanel_3 = tkViPanel(Frames[TRI_RIGHT])

	imgPanel_1.show(cv2.imread("charles_001.jpg"))
	imgPanel_2.show(cv2.imread("TestPic.jpg"))
	imgPanel_3.show(cv2.imread("charles_001.jpg"))

	tkRoot.mainloop()
	cv2.destroyAllWindows()


def test_tkViPanel(tkRoot):

	topFrame = TK.Frame(tkRoot)
	topFrame.pack()

	bottomFrame = TK.Frame(tkRoot)
	bottomFrame.pack()

	imgPanel_1 = tkViPanel(topFrame)
	imgPanel_2 = tkViPanel(bottomFrame)

	imgPanel_1.show(cv2.imread("charles_001.jpg"))
	imgPanel_2.show(cv2.imread("TestPic.jpg"))

	tkRoot.mainloop()
	cv2.destroyAllWindows()


def test_tkScale(root):
	h_bar = tkScale(root)
	h_bar.set_label("New Label")
	h_bar.set_value(300)
	root.mainloop()


def test_tkRadioButton(root):
	def radioCmd():
		print("radioBtn: {} selected.".format(radioButton.get_value()))
	# radioPair = [("item-1", 111), ("item-2", 222)]
	# radioBtn = tkRadioButton(root, label="My RadioButton", buttons=radioPair)
	# radioBtn.set_command(radioCmd)
	# radioBtn.set_value(222)

	radioButton = tkRadioButton(root, label="My RadioButton", isRadio=True)
	buttons = []
	for i in range(0, 9):
		txt = "item-{:1d}".format(i)
		b = (txt, i)
		buttons.append(b)
	radioButton.add_buttons(buttons)
	radioButton.pack_buttons("GRID", 5)

	radioButton.set_command(radioCmd)
	root.mainloop()


if __name__ == "__main__":
	rootWin = TK.Tk()

	# test_tkViPanel(rootWin)
	# test_tkQuadFrame(rootWin)
	# test_V2Frame(rootWin)
	# test_H2Frame(rootWin)
	# test_TriFrame(rootWin)
	# test_tkScale(rootWin)
	test_tkRadioButton(rootWin)
