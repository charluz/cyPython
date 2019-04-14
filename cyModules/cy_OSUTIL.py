#!/usr/bin/env python
#-- encoding: utf-8 --

import os, sys, platform

PLATFORM_WINDOWS = 'Windows'
PLATFOMR_LINUX = 'Linux'
CLNAME = 'cyOS'

cyOSDebugCtrl = False

def debug_set(en):
    global cyOSDebugCtrl
    if en:
        cyOSDebugCtrl = True
    else:
        cyOSDebugCtrl = False

    return

def dbgPrint(*args):
    if cyOSDebugCtrl:
        print(' '.join(map(str,args)))


def parse_path(infile):
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


def create_dir(dir_name):
    dbgPrint("create_dir(): dir_name= ", dir_name)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name, exist_ok=True)
        except:
            dbgPrint("{}:ERROR: Can't create directory, {}.".format(CLNAME, repr(dir_name)))
            return ""
        dbgPrint("{}: Directory {} created.".format(CLNAME, dir_name))
    else:
        dbgPrint("{}: Directory {} existed.".format(CLNAME, dir_name))

    return dir_name


def create_sub_dir(sub_name, parent='.'):
    dir_name = "{}/{}".format(parent, sub_name)
    create_dir(dir_name)
    return dir_name


def change_dir(dir_name):
    os.chdir(dir_name)

