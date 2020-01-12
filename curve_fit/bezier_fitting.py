# -*- encoding: utf-8 -*-

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

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    # print('type of polynomial_array :', end=''); print(type(polynomial_array))
    # print('length of polynomial_array :', end=''); print(len(polynomial_array))
    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    #print('xvals (np.dot()): ', end=''); print(xvals)

    return xvals, yvals

if __name__ == "__main__":
	#-- Read Gamma points
	X = []
	Y = []
	f_gma = "gamma_pt.txt"
	with open(f_gma, "r")  as f:
		# for line in f.readlines():
		# 	print(line.strip())
		line = f.readline()
		while line:
			x, y = line.strip().split()
			print(x, y)
			X.append(int(x))
			Y.append(int(y))
			line = f.readline()
	f.close()

	#-- conduct sci bezier curve fitting
	points = []
	for i in range(0, len(X)):
		points.append([X[i], Y[i]])
	new_x, new_y = bezier_curve(points, nTimes=5000 )

plt.plot()
plt.plot(X, Y, 'o', new_x, new_y)
plt.xlim(0, 256)
plt.show()