
# coding: utf-8

# In[19]:


#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np

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
    


# In[27]:


'''
    ndarray 基本屬性: ndim, shape, size, dtype, itemsize, data
'''

print_banner('Example : create an 1-D array, a=np.arange(15)')
a = np.arange(15)    # create an ndarray instant with 15 elements
#a.reshape(3,5)
print('ndarray attributes : a = np.arange(15) ----')
printf('ndarray.ndim : '); print(a.ndim)
printf('ndarray.shape: '); print(a.shape)    # tuple of ndarray dimensions
printf('ndarray.size: '); print(a.size)      # number of elements of ndarray
printf('ndarray.dtype: '); print(a.dtype)    # data type of element
printf('ndarray.itemsize: '); print(a.itemsize) # the size of element
printf('ndarray.data : '); print(a.data)
printf('ndarray : '); print(a)

print_banner('clone a new ndarray which is reshaped from a : b = reshape(3.5)')
b = a.reshape(3,5)
printf('ndarray.ndim : '); print(b.ndim)
printf('ndarray.shape: '); print(b.shape)    # tuple of ndarray dimensions
printf('ndarray.size: '); print(b.size)      # number of elements of ndarray
printf('ndarray.dtype: '); print(b.dtype)    # data type of element
printf('ndarray.itemsize: '); print(b.itemsize) # the size of element
printf('ndarray.data : '); print(b.data)
printf('ndarray : '); print(b)


# In[26]:


'''
    Initiate an ndarray with a list [1,3,5,7,9] --> 1-D array
'''
print_banner('Initiate an ndarray with a list [1,3,5,7,9]')
x = np.array([1,3,5,7,9])
print('ndarray attributes : a = np.array([1,3,5,7,9]) ----')
printf('ndarray.ndim : '); print(x.ndim)
printf('ndarray.shape: '); print(x.shape)    # tuple of ndarray dimensions
printf('ndarray.size: '); print(x.size)      # number of elements of ndarray
printf('ndarray.dtype: '); print(x.dtype)    # data type of element
printf('ndarray.itemsize: '); print(x.itemsize) # the size of element
printf('ndarray.data : '); print(x.data)
printf('ndarray : '); print(x)


# In[32]:


'''
    Initiate an ndarray with a tuple --> tuple 直接指定 array 的 shape
'''
print_banner('Initiate an ndarray with a tuple (2,3,4)')
x = np.zeros( (2,3,4) )
print('ndarray attributes : x = np.zero((2,3,4)) ----')
printf('ndarray.ndim : '); print(x.ndim)
printf('ndarray.shape: '); print(x.shape)    # tuple of ndarray dimensions
printf('ndarray.size: '); print(x.size)      # number of elements of ndarray
printf('ndarray.dtype: '); print(x.dtype)    # data type of element
printf('ndarray.itemsize: '); print(x.itemsize) # the size of element
printf('ndarray.data : '); print(x.data)
printf('ndarray : '); print(x)


print_banner('clone a new array y from : x.reshape(4,6)')
y = x.reshape(4,6)
printf('ndarray.ndim : '); print(y.ndim)
printf('ndarray.shape: '); print(y.shape)    # tuple of ndarray dimensions
printf('ndarray : '); print(y)

