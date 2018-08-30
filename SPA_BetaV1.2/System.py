import os
import settings

if not settings.byCmd:
    import GUI


class System:

    def __init__(self):
        if not settings.byCmd:
            self.__gui = GUI.mainWindow(None, title='Solar Panel Analyzer (SPA) - Beta Version 1.2')

        self.__input = list()  # list of Images
        self.__saveDir = settings.SPAOutputPath

        self.__params = list() # list of parameters
        self.__params.insert(settings.DEBUG_PARAM, False)
        self.__params.insert(settings.DIM_PARAM, [None,None])
        self.__params.insert(settings.AUTOTHRESH_PARAM, None)
        self.__params.insert(settings.LOWTHRESH_PARAM, None)
        self.__params.insert(settings.HIGHTHRESH_PARAM, None)
        self.__params.insert(settings.BLUR_PARAM, None)
        self.__params.insert(settings.DILATE_PARAM, None)
        self.__params.insert(settings.MINAREA_PARAM, None)

        self.__panelsList = list()  # list of detected panels (DG)

        # create folder if it does not exist
        if not os.path.exists(self.__saveDir):
           os.makedirs(self.__saveDir)

        print('System initializated')
        print('SPA output dir: ' + str(self.__saveDir))

    # get
    def getInput(self):
        return self.__input

    def getSaveDir(self):
        return self.__saveDir

    def getParams(self):
        return self.__params

    def getPanelsList(self):
        return self.__panelList

    def getGUI(self):
        return self.__gui

    # set
    def setInput(self, inp):
        self.__input = inp
        return

    def setSaveDir(self, inp):
        self.__saveDir = inp
        return

    def resetSaveDir(self):
        self.__saveDir = settings.SPAOutputPath
        return

    def setParams(self, inp):
        self.__params = inp
        return

    def setDebugMode(self):
        self.__params[settings.DEBUG_PARAM] = True
        return

    def setPanelsList(self, inp):
        self.__panelsList = inp
        return

    # check params
    def checkDebugMode(self):
        return self.__params[settings.DEBUG_PARAM]

    def checkDim(self):
        return self.__params[settings.DIM_PARAM]


    # others - GUI methods
    # def insertImage(self):
    #     return
    #
    # def readParams(self):
    #     return
    #
    # def launchElaboration(self):
    #     return
    #
    # def viewPanel(self):
    #     return
    #
    # def updatePanels(self):
    #     return


    # NOT IMPLEMENTED
    #
    # def saveDG(self):
    #     return
