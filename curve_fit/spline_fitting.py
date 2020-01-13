# -*- encoding: utf-8 -*-

import argparse
import numpy as np
# from scipy.special import comb
import scipy.interpolate as spi
import matplotlib.pyplot as plt

if False: #-- used to generate Gamma data
	gamma = float(input("gamma coefficient= "))

	for x in range(0, 255):
		y = int(pow(x/255.0, gamma)*255)
		print("{:3d}\t{:3d}".format(x, y))


if __name__ == "__main__":
   #-------------------------------------
	# Parse arguements
	#-------------------------------------
	parser = argparse.ArgumentParser(description="Bezier Curve fitting")	#-- ,add_help=False)
	parser.add_argument('gfile', help="input file containing the control points")
	# parser.add_argument('-k', '--order', nargs='?', const=1, type=int, default=0, help='JSON file for default RAW format.')
	parser.add_argument('-k', '--deg', type=int, default=3, help='the degree of the spline fit.')
	# parser.add_argument("-w", "--width", type=int, help='the width of the RAW image')
	# parser.add_argument("-h", "--height", type=int, help='the height of the RAW image')
	# parser.add_argument("--bayer", choices=['R', 'Gr', 'Gb', 'B'], help='bayer type of starting pixel\navailable options:R, Gr, Gb, B.')
	# parser.add_argument("--bits", type=int, help='number of bits per pixel')
	# parser.add_argument("--scale", type=int, help="percentage to downscale while generating output images, e.g., 30 stands for 30%%.")
	# parser.add_argument("--ROI", help='+x+y*w+h to specify ROI of RAW image.')
	args = parser.parse_args()

	#--------------------------------------------------------------------
	#-- Read Gamma points
	#--------------------------------------------------------------------
	X = []
	Y = []
	f_gma = args.gfile
	with open(f_gma, "r")  as f:
		# for line in f.readlines():
		# 	print(line.strip())
		line = f.readline()
		while line:
			x, y = line.strip().split()
			# print(x, y)
			X.append(int(x)*16)
			Y.append(int(y)*16)
			line = f.readline()
	f.close()

	#--------------------------------------------------------------------
	#-- conduct sci cubic spline fitting
	#--------------------------------------------------------------------
	#-- 找出 spline 的 t(vector knots 節點), c(spline coefficients 係數), k(degree of spline 階數)
	tck = spi.splrep(X, Y, k=args.deg)

	#-- 用 PPoly.from_spline 來查看 spline 每個分段函數的係數
	if True: #-- for further understanding
		pp = spi.PPoly.from_spline(tck)
		print(pp.c.T)

	#-- 求出整條 curve 的值
	new_x = [x for x in range(0, 256*16)]
	new_y = spi.splev(new_x, tck)

print("new_x: ", new_x)
print("new_y: ", new_y)

plt.plot()
plt.plot(X, Y, 'o', new_x, new_y)
plt.xlim(0, 256*16)
plt.show()
