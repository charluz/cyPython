import sys, os
print("script: sys.argv[0] is", repr(sys.argv[0]))
print("script: __file__ is", repr(__file__))
print("script: cwd is", repr(os.getcwd()))


dirname, filename = os.path.split(os.path.abspath(__file__))
print("running from", dirname)
print("file is", filename)

