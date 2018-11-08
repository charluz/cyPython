# -*- coding: utf-8 -*-
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

fig = plt.figure(figsize=(16,12))
ax = fig.gca(projection="3d")

img = cv.imread("D65_light_bypassGamma_check_shrding1.png")     # 修改图片位置
img = cv.blur(img,(5,5))
img = cv.blur(img,(5,5))
img = cv.blur(img,(5,5))


#img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#imgd = np.array(img)      # image类 转 numpy

#B = img[:,:,0]
#G = img[:,:,1]
#R = img[:,:,2]


max_B_value = 0;
max_G_value = 0;
max_R_value = 0;
for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if max_B_value <img[i, j][0]:
                max_B_value = img[i, j][0]
            
            if max_G_value <img[i, j][1]:
                max_G_value = img[i, j][1]
            if max_R_value <img[i, j][2]:
                max_R_value = img[i, j][2]
print("max value",max_B_value,max_G_value,max_R_value)

for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j][0] = img[i, j][0]*100/max_G_value
            img[i, j][1] = img[i, j][1]*100/max_G_value
            img[i, j][2] = img[i, j][2]*100/max_G_value

img = cv.blur(img,(5,5))
img = cv.blur(img,(5,5))
img = cv.blur(img,(5,5))
img = cv.GaussianBlur(img,(7,7),0)
img = cv.GaussianBlur(img,(7,7),0)
img = cv.GaussianBlur(img,(7,7),0)

B = img[:,:,0]
G = img[:,:,1]
R = img[:,:,2]

imgd = np.array(B) 

#img2 = cv.imread("test_b.jpg")     # 修改图片位置
#img2 = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
#imgd2 = np.array(img2)      # image类 转 numpy

imgd2 = np.array(R)
imgd3 = np.array(G)

# 准备数据
sp = img.shape
h = int(sp[0])#height(rows) of image
w = int(sp[1])#width(colums) of image

x = np.arange(0,w,1)
y = np.arange(0,h,1)
x,y = np.meshgrid(x,y)
z = imgd
#surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm)  # cmap指color map
#surf = ax.plot_surface(x, y, z, color='b')  # cmap指color map
surf = ax.plot_surface(x, y, z, cmap=cm.Blues)  # cmap指color map

z = imgd2
#surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm)  # cmap指color map
#surf = ax.plot_surface(x, y, z, color='tomato')  # cmap指color map
#surf = ax.plot_surface(x, y, z, color='r')  # cmap指color map
surf = ax.plot_surface(x, y, z, cmap=cm.Reds)  # cmap指color map

z = imgd3
#surf = ax.plot_surface(x, y, z, color='yellowgreen')  # cmap指color map
surf = ax.plot_surface(x, y, z, cmap=cm.Greens)  # cmap指color map

# 自定义z轴
ax.set_zlim(0,100)
ax.zaxis.set_major_locator(LinearLocator(20))  # z轴网格线的疏密，刻度的疏密，20表示刻度的个数
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))  # 将z的value字符串转为float，保留2位小数

# 设置坐标轴的label和标题
ax.set_xlabel('x', size=15)
ax.set_ylabel('y', size=15)
ax.set_zlabel('z', size=15)
ax.set_title("Surface plot", weight='bold', size=20)

# 添加右侧的色卡条
#fig.colorbar(surf, shrink=0.6, aspect=8)  # shrink表示整体收缩比例，aspect仅对bar的宽度有影响，aspect值越大，bar越窄
plt.show()
#--------------------- 
#作者：yefcion 
#来源：CSDN 
#原文：https://blog.csdn.net/yefcion/article/details/80883605 
#版权声明：本文为博主原创文章，转载请附上博文链接！#