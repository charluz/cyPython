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

'''
    For the given path, get the List of all files in the directory tree
'''
def list_dir_files(dirName, extPatt=""):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + list_dir_files(fullPath, extPatt)
        else:
            if extPatt == "":
                allFiles.append(fullPath)
            else:
                _, _, fl_ext = parse_path(fullPath)
                if fl_ext == extPatt:
                    allFiles.append(fullPath)
    return allFiles


def list_all_dirs(rootDir):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(rootDir)
    allDirs = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(rootDir, entry)

        if os.path.isdir(fullPath):
            allDirs.append(fullPath)
            allDirs += list_all_dirs(fullPath)

    return allDirs

