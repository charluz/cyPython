#!/usr/bin/env python
# encoding: utf-8

from sklearn import datasets
import matplotlib.pyplot as plt

digits = datasets.load_digits()

# 設定圖形的大小（寬, 高）inches
fig = plt.figure(figsize=(4,3))

# 調整子圖形 
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)

# 把前 8 個手寫數字顯示在子圖形
for i in range(8):
	if 0:
	    # 在 2 x 4 網格中第 i + 1 個位置繪製子圖形，並且關掉座標軸刻度
    	ax = fig.add_subplot(2, 4, i + 1, xticks = [], yticks = [])
	else: # 也可以寫成這樣
		# 在 i + 1 的位置初始化子圖形
		plt.subplot(2, 4, i+1)
		# 關掉子圖形座標軸刻度
		plt.axis('off')

    # 顯示圖形，色彩選擇灰階
    ax.imshow(digits.images[i], cmap = plt.cm.binary)
    # 在左下角標示目標值 (row, col) in pixels
    ax.text(0, 7, str(digits.target[i]))

# 顯示圖形
plt.show()


