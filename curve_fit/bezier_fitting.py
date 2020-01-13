# -*- encoding: utf-8 -*-

import argparse
import numpy as np
from scipy.special import comb
import matplotlib.pyplot as plt

if False: #-- used to generate Gamma data
	gamma = float(input("gamma coefficient= "))

	for x in range(0, 255):
		y = int(pow(x/255.0, gamma)*255)
		print("{:3d}\t{:3d}".format(x, y))


def bernstein_poly(i, n, t):
	"""
	The Bernstein polynomial of n, i as a function of t
	"""
	return comb(n, i) * ( t**(n-i) ) * (1 - t)**i



def bezier_curve(points, nTimes=1000):
	"""
	Given a set of control points, return the
	bezier curve defined by the control points.

		points should be a list of lists, or list of tuples
		such as [ [1,1],
				 [2,3],
				 [4,5], ..[Xn, Yn] ]
		nTimes is the number of time steps, defaults to 1000

		See http://processingjs.nihongoresources.com/bezierinfo/
	"""

	nPoints = len(points)
	xPoints = np.array([p[0] for p in points])
	yPoints = np.array([p[1] for p in points])

	# print('length of points : ', end=''); print(nPoints)
	# print('xPoints : ', end=''); print(xPoints)
	# print('yPoints : ', end=''); print(yPoints)

	t = np.linspace(0.0, 1.0, nTimes)

	polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)])

	# print('type of polynomial_array :', end=''); print(type(polynomial_array))
	# print('length of polynomial_array :', end=''); print(len(polynomial_array))
	xvals = np.dot(xPoints, polynomial_array)
	yvals = np.dot(yPoints, polynomial_array)

	#print('xvals (np.dot()): ', end=''); print(xvals)

	return xvals, yvals

if __name__ == "__main__":
   #-------------------------------------
	# Parse arguements
	#-------------------------------------
	parser = argparse.ArgumentParser(description="Bezier Curve fitting")	#-- ,add_help=False)
	parser.add_argument('gfile', help="input file containing the control points")
	# parser.add_argument('--gui', nargs='?', const=1, type=int, default=0, help='JSON file for default RAW format.')
	# parser.add_argument('--conf', help='JSON file for default RAW format.')
	# parser.add_argument("-w", "--width", type=int, help='the width of the RAW image')
	# parser.add_argument("-h", "--height", type=int, help='the height of the RAW image')
	# parser.add_argument("--bayer", choices=['R', 'Gr', 'Gb', 'B'], help='bayer type of starting pixel\navailable options:R, Gr, Gb, B.')
	# parser.add_argument("--bits", type=int, help='number of bits per pixel')
	# parser.add_argument("--scale", type=int, help="percentage to downscale while generating output images, e.g., 30 stands for 30%%.")
	# parser.add_argument("--ROI", help='+x+y*w+h to specify ROI of RAW image.')
	args = parser.parse_args()
		#-- Read Gamma points
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
			X.append(int(x))
			Y.append(int(y))
			line = f.readline()
	f.close()

	#-- conduct sci bezier curve fitting
	points = []
	for i in range(0, len(X)):
		points.append([X[i], Y[i]])
	new_x, new_y = bezier_curve(points, nTimes=50)

print("new_x: ", new_x)
print("new_y: ", new_y)

plt.plot()
plt.plot(X, Y, 'o', new_x, new_y)
plt.xlim(0, 256)
plt.show()
