#!/usr/bin/env python
# encoding: utf-8

import argparse


###########################################################
# RAW Format JSON Parser
###########################################################
def conf_json_load():
    import json
    global gRawFormat

    #jsonDict = {}
    conf_json = "./raw_conf.json"
    try:
        with open(conf_json, "r") as f:
            jsonDict = json.load(f)
    except:
        print("Error: failed to load configuration file ... ", conf_json)
        jsonDict = None

    #print(jsonDict)
    if jsonDict:
        gRawFormat["showBayerColor"] = jsonDict["showBayerColor"]
        gRawFormat["showRawGray"] = jsonDict["showRawGray"]
        gRawFormat["width"] = jsonDict["width"]
        gRawFormat["height"] = jsonDict["height"]
        gRawFormat["bits"] = jsonDict["bits"]
        gRawFormat["bayer"] = jsonDict["bayer"]

    return jsonDict


###########################################################
# MainEntry
###########################################################

gRawFormat = {
    "showBayerColor"    : False,
    "showRawGray"       : True,
    "showRawRGB"        : False,
    "width"         : 1600,
    "height"        : 1200,
    "bits"          : 10,
    "bayer"         : 3,    #-- "bayer cdoe: R=0, Gr=1, Gb=2, B=3"
}



def print_arguments():
    print("--- Program Arguments -----------------------------------------------")
    argstr = "rawImage"
    print(argstr, ": ", gRawImgFile)
    argstr = "width"
    print(argstr, ": ", gRawFormat[argstr])
    argstr = "height"
    print(argstr, ": ", gRawFormat[argstr])
    argstr = "bayer"
    print(argstr, ": ", gRawFormat[argstr])
    argstr = "bits"
    print(argstr, ": ", gRawFormat[argstr])
    print("---------------------------------------------------------------------")
    print()


if __name__ == "__main__":
    #-------------------------------------
    # Parse arguements
    #-------------------------------------
    argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('rawImage', help="input RAW image file name")
    parser.add_argument('--conf', help='JSON file for default RAW format.')
    parser.add_argument("--width", type=int, help='the width of the RAW image')
    parser.add_argument("--height", type=int, help='the height of the RAW image')
    parser.add_argument("-b", "--bayer", choices=['R', 'Gr', 'Gb', 'B'], help='bayer type of starting pixel\navailable options:R, Gr, Gb, B.')
    parser.add_argument("-n", "--bits", type=int, help='number of bits per pixel')
    parser.add_argument("--scale", type=int, help="percentage to downscale while generating output images, e.g., 30 stands for 30%%.")
    parser.add_argument("--ROI", help='+x+y*w+h to specify ROI of RAW image.')
    args = parser.parse_args()

    gRawImgFile = args.rawImage
    # print(args.conf)
    if args.conf:
        conf_json_load()
    else:
        if args.width and args.height:
            gRawFormat["width"]     = args.width
            gRawFormat["height"]    = args.height
        elif args.bits:
            gRawFormat["bits"]      = args.bits
        elif args.bayer:
            gRawFormat["bayer"]     = args.bayer
        else:
            pass

    #-------------------------------------
    # Initialize globals
    #-------------------------------------
    gRawWidth, gRawHeight = gRawFormat["width"], gRawFormat["height"]
    gRawBits = gRawFormat["bits"]
    gRawBayerTye = gRawFormat["bayer"]

    gIsShowBayerImage = gRawFormat["showBayerColor"]
    gIsShowRawImage = gRawFormat["showRawGray"]
    gIsShowRawRGB = gRawFormat["showRawRGB"]

    if False:   #-- Debug only !!
        print_arguments()



# def hello(args):
#     print('Hello, {0}!'.format(args.name))


# def goodbye(args):
#     print('Goodbye, {0}!'.format(args.name))


# parser = argparse.ArgumentParser()
# subparsers = parser.add_subparsers()

# hello_parser = subparsers.add_parser('hello')
# hello_parser.add_argument('name')  # add the name argument
# hello_parser.set_defaults(func=hello)  # set the default function to hello

# goodbye_parser = subparsers.add_parser('goodbye')
# goodbye_parser.add_argument('name')
# goodbye_parser.set_defaults(func=goodbye)

# if __name__ == '__main__':
#     args = parser.parse_args()
#     args.func(args)  # call the default functio
