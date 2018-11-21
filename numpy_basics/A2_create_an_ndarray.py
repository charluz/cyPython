
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
''' There are mnay ways to create an ndarray of numpy. 
    This tutorial is to illustrate the common methods. 
'''

def printf(s):
    '''print a string without the default newline at the end of output'''
    print(s, end='')
    return

    
def print_banner(s):
    '''print a banner with given string'''
    print('=================================================================')
    print(s)
    print('=================================================================')
    return
    




'''可以使用 array() 从常规的Python列表(list)和元组(tuple)创造数组。
所创建的数组类型由原序列中的元素类型推导'''

print_banner('Example : a = array( [2,3,4] ) <-- with a python 1-D list')
a = np.array( [2,3,4] )
printf('ndim  : '); print(a.ndim)
printf('shape : '); print(a.shape)
printf('a : '); print(a)

print_banner('Example : b = array( [[1, 1],[2,2]] ) <-- with a python 2-D list')
b = np.array( [[1, 1],[2,2]] )
printf('ndim  : '); print(b.ndim)
printf('shape : '); print(b.shape)
printf('b : '); print(b)

print_banner('錯誤的方法： a = array(1,2,3,4) ---> (X) ')
try:
    a = array(1,2,3,4)
except:
    print('Illegal way to create an array with a = array(1,3,5,7) !!')



print_banner("Example: c = array( [ (1.5, 3), (2.5, 7) ] ) \n" + "tuple 可以當作 list 的 element 初始 ndarray")
c = np.array( [ (1.5, 3, 2), (2.5, 7, 9.1) ] )
printf('ndim  : '); print(c.ndim)
printf('shape : '); print(c.shape)
printf('b : '); print(c)

