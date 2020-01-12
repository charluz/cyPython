# -*- encoding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

if False: #-- used to generate Gamma data 
	gamma = float(input("gamma coefficient= "))

	for x in range(0, 255):
		y = int(pow(x/255.0, gamma)*255)
		print("{:3d}\t{:3d}".format(x, y))

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
	
print("list X: ", X)
print("list Y: ", Y)
f.close()

#-- conduct numpy polyfit
order = 6
z = np.polyfit(X, Y, order)
print(z)
fpoly = np.poly1d(z)

new_x = np.linspace(0, 255)
new_y = fpoly(new_x)

plt.plot()
plt.plot(X, Y, 'o', new_x, new_y)
plt.xlim(0, 256)
plt.show()