import os, sys

cyModulesPath = "D:\\cyMyProjects\\gitPython\\cyModules"

if os.name == "nt":
	print("Add ", cyModulesPath, " to module load path.")
	sys.path.append(cyModulesPath)
	
