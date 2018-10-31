import matplotlib.pyplot as plt
import numpy as np

'''
Reference : https://medium.com/@yehjames/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC2-5%E8%AC%9B-%E8%B3%87%E6%96%99%E8%A6%96%E8%A6%BA%E5%8C%96-matplotlib-seaborn-plotly-75cd353d6d3f
Matplot 的畫線格式 :
    (1) Line
        '-' (solid line),  '--' (dashed line), '-.' (dashed dot line), ':' (dotted line) 
    (2) Marker
        ',' (pixel marker), '.' (point marker), 
        r 代表紅色、兩個-代表虛線，b代表藍色、s代表方塊，g代表綠色，^代表三角形, v代表倒三角形, 
        '>' (triangle right marker), '<' (triangle left marker)
'''

plt.ylabel('Y-axis')
plt.xlabel('X-axis')
# t = np.linspace(0., 5.)
# print("LINSPACE -- t : " + str(t))
# plt.plot(t, 'r+')   
# plt.show()

# t = np.arange(0., 5., 0.2)
# # print("ARANGE -- t : " + str(t))
# plt.plot(t, t, 'r,--', t, t**2, 'bs-.', t, t**3, 'g^:')
# plt.show()

## 長條圖 (Bar Chart)
x = [4, 4, 7, 7, 8, 9, 10, 10, 10, 11, 11, 12, 12, 12, 12, 13, 13, 13]
y = [2, 10, 4, 22, 16, 10, 18, 26, 34, 17, 28, 14, 20, 24, 28, 26, 34, 34]
# plt.bar(x, y)
plt.scatter(x, y)
plt.show()

