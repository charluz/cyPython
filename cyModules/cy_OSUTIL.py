#!/usr/bin/env python
#-- encoding: utf-8 --

import os, sys, platform

PLATFORM_WINDOWS = 'Windows'
PLATFOMR_LINUX = 'Linux'
CLNAME = 'cyOSUTIL'

#--------------------------------------
# Class: cyOSUTIL
#--------------------------------------
class cyOSUTIL():
    """
    My utility functions to process OS specific operations, such as
    parse path of an input file.

    Functions:
    -------------
    """

    def __init__(self, debug=False):
        """
        """
        self.debug = debug
        if platform.system() == PLATFOMR_LINUX:
            self.platform = PLATFOMR_LINUX
        else:
            self.platform = PLATFORM_WINDOWS

        if self.debug:
            print("{}: Running on {}.".format(CLNAME, self.platform))

        return


    def debug(self, en=False):
        '''
        '''
        if en:
            self.debug = True
        else:
            self.debug = False

        return


    def parse_path(self, infile):
        '''
        '''
        # Get directory name
        fl_dir = os.path.dirname(infile)
        if not fl_dir:
            fl_dir = '.'

        # get the filename
        file_name = os.path.basename(infile)
        fl_base, fl_ext = os.path.splitext(file_name)

        return fl_dir, fl_base, fl_ext


    def create_dir(self, dir_name):
        if not os.path.exists(dir_name):
            try:
                os.mkdir(dir_name)
            except:
                if self.debug:
                    print("{}:ERROR: Can't create directory, {}.".format(CLNAME, repr(dir_name)))
                return ""
            if self.debug: print("{}: Directory {} created.".format(CLNAME, dir_name))
        else:
            if self.debug: print("{}: Directory {} existed.".format(CLNAME, dir_name))

        return dir_name


    def create_sub_dir(self, sub_name, parent='.'):
        dir_name = "{}/{}".format(parent, sub_name)
        self.create_dir(dir_name)
        return dir_name


    def change_dir(self, dir_name):
        os.chdir(dir_name)

