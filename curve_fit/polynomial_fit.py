#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Polynomial Fitting
'''

# Scientific libraries
import numpy as np
import matplotlib.pyplot as plt

points = np.array([(1, 1), (2, 4), (3, 1), (9, 3)])
print(points)

# get x and y vectors
x = points[:,0]
y = points[:,1]

# calculate polynomial
#
#-----------------------------------------------------------------------------
# np.polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False) 的使用
#-----------------------------------------------------------------------------
# 通常只使用前三個參數，x、y分別對應 input x、以及 y=f(x)，deg 自由度則是 f(x) 多項式的
# 最高冪次。
# polyfit() return 的是一組包含多項式係數的 ndarraay
#-----------------------------------------------------------------------------
# np.poly1d() 的使用:
#-----------------------------------------------------------------------------
# ploy1d() 的輸入是 polyfit() 得到的代表多項式係數的 ndarray，輸出則是整個多項式。
# Example :
# fx=np.poly1d([3,2,1])  <-- f(x)=3*x^2+2*x+1
# fx(0.5) 就可以得到 f(x=0.5) 的值
#-----------------------------------------------------------------------------
z = np.polyfit(x, y, 3)
f = np.poly1d(z)
print('Type of np.polyfit(): ', end='')
print(type(z))
print('z= ', end=''); print(z)
print('Type of np.poly1d(): ', end='')
print(type(f))
print('f= ', end=''); print(f)
print('f(0.5)= ', end=''); print(f(0.5))

new_x = np.linspace(x[0], x[-1], 40)
new_y = f(new_x)
print('new_x= ', end=''); print(new_x)
print('new_y= ', end=''); print(new_y)

plt.plot(new_x, new_y, 'r-')
plt.show()

