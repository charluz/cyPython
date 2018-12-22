# HOWTO: Use my Python Modules #

## Windows ##

I put my modules in `D:\cyMyProjects\gitPython\cyModules`. We can add a snippet as shown below at the begining of the script to define the load path of Python.


```
import os, platform

"""
For Windows OS:
	os.name == 'nt'
	platform.system() == "Windows"
"""

cyModulesPath = "D:\\cyMyProjects\\gitPython\\cyModules"

if os.name == "nt":
	sys.path.append(cyModulesPath)
```
