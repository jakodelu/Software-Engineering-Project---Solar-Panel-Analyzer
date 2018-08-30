import sys

import System
import Image
import Elaboration
import settings

# MAIN ##################################################################
settings.byCmd = True
if len(sys.argv) < 9:
    print("\nERROR! Missing parameters")
    print("Needed: output - input - low threshold - high threshold - blur value - iters of dilate - min area limitation - debug mode")
    print("Parameters must be inserted sorting as above")
    sys.exit()

settings.arg = sys.argv

settings.SPA = System.System()
newImg = Image.Image(id=1, filepath=sys.argv[2])
el = Elaboration.Elaboration(id=1, sourceImg=newImg)
el.launchProcedure()

if el.getStatus() is 4:
    print('Path of result is: ' + settings.SPAOutputPath)
    print()

    print('<< ELABORATION COMPLETED!')
    print()

    print('PANELS DETECTED: ' + str(newImg.getPanels()))
    print()

    print('PROCESSING TIME: ' + str(el.getExeTime()).split(":")[2] + ' seconds')
    print()

    print('PARAMETERS:')
    message = ''
    idx = 0
    for i in settings.arg:
        if idx == settings.OUTPUT:
            message = message + 'Output folder: ' + i + '/SPA_output'
        elif idx == settings.SOURCE:
            message = message + 'Source image: '
        elif idx == settings.LOW:
            message = message + 'lowthresh: '
        elif idx == settings.HIGH:
            message = message + 'highthresh: '
        elif idx == settings.BLUR:
            message = message + 'blur: '
        elif idx == settings.NITERS:
            message = message + 'nIters: '
        elif idx == settings.AREA:
            message = message + 'area lim: '
        elif idx == settings.DEBUG_POS:
            message = message + 'debugMode: '
        else:
            pass

        if idx == settings.OUTPUT:
            message = message + i + '/SPA_output'
            message = message + '\n'
        elif settings.OUTPUT < idx < settings.DEBUG_POS:
            message = message + i
            message = message + '\n'
        elif idx == settings.DEBUG_POS:
            message = message + str(settings.SPA.checkDebugMode())
            message = message + '\n'
        else:
            pass

        idx = idx + 1

    print(message)

else:
    print('<< ERROR!!!!!!\n<< ELABORATION FAILED!')
    print()