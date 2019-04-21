import os, sys, platform

winModulesPath = "D:\\cyMyProjects\\gitPython\\cyModules"
linuxModulesPath = "/home/charles/workbench/gitPython/cyModules"

if os.name == "nt":
    print("appending {} to system path ...".format(winModulesPath))
    sys.path.append(winModulesPath)

if platform.system() == 'Linux':
    print("appending {} to system path ...".format(linuxModulesPath))
    sys.path.append(linuxModulesPath)
