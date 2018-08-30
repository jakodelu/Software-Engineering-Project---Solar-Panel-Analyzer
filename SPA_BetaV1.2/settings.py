import getpass
import platform
import os

# CMD MODE ################################################
global arg
arg = None

global byCmd
byCmd = False

global OUTPUT
global SOURCE
global LOW
global HIGH
global BLUR
global NITERS
global AREA
global DEBUG_POS

OUTPUT = 1
SOURCE = 2
LOW = 3
HIGH = 4
BLUR = 5
NITERS = 6
AREA = 7
DEBUG_POS = 8

########################################################

global SPA

global SPAOutputPath

global icon
icon = 'icon/SPA_icon.png'

if byCmd == True:
    SPAOutputPath = arg[1] + '/SPA_output'
else:
    if platform.system() == 'Windows':
            SPAOutputPath = 'C:/Users/' + getpass.getuser() + '/Desktop/SPA_output'
    else:
        if str(os.getenv('LANG')) == 'it_IT.UTF-8':
            SPAOutputPath = '/home/' + getpass.getuser() + '/Scrivania/SPA_output'
        else:
            SPAOutputPath = '/home/' + getpass.getuser() + '/Desktop/SPA_output'

#parameters position in list of params
global DEBUG_PARAM
global DIM_PARAM
global LOWTHRESH_PARAM
global HIGHTHRESH_PARAM
global AUTOTHRESH_PARAM
global BLUR_PARAM
global DILATE_PARAM
global MINAREA_PARAM


DEBUG_PARAM = 0
DIM_PARAM = 1
AUTOTHRESH_PARAM = 2
LOWTHRESH_PARAM = 3
HIGHTHRESH_PARAM = 4
BLUR_PARAM = 5
DILATE_PARAM = 6
MINAREA_PARAM = 7

#default values
global LOWTHRESH_DEFAULT
global HIGHTHRESH_DEFAULT
global BLUR_DEFAULT
global DILATE_DEFAULT
global MINAREA_DEFAULT
global RATE_DEFAULT

LOWTHRESH_DEFAULT = '100'
HIGHTHRESH_DEFAULT = '200'
BLUR_DEFAULT = '8'
DILATE_DEFAULT = '2'
MINAREA_DEFAULT = '10000'
RATE_DEFAULT = 1.8

#reccomended values
global TIFF_LOW
global TIFF_HIGH
global TIFF_BLUR
global TIFF_DILATE
global TIFF_AREA

TIFF_LOW = 100
TIFF_HIGH = 200
TIFF_BLUR = 8
TIFF_DILATE = 1
TIFF_AREA = 12500000

global JPG_LOW
global JPG_HIGH
global JPG_BLUR
global JPG_DILATE
global JPG_AREA

JPG_LOW = 100
JPG_HIGH = 200
JPG_BLUR = 8
JPG_DILATE = 2
JPG_AREA = 10000

global autoThreshValue
autoThreshValue = None
