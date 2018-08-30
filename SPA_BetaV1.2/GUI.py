import wx
import sys
import os
import datetime

import settings
import Image
import Elaboration


class mainWindow(wx.Frame):

    def __init__(self, parent, title):

        self.panel = None

        # infos
        self.screenWidth = None
        self.screenHeight = None
        self.filesDir = ''
        self.filesSelected = None

        self.debugCheck = None
        self.widthPanel = None
        self.heightPanel = None

        # buttons
        self.openFilesButton = None
        self.launchButton = None
        self.viewButton = None

        # parameters items
        self.lowThreshCheck = None
        self.lowThresh = None
        self.highThreshCheck = None
        self.highThresh = None
        self.threshButton = None

        self.blurCheck = None
        self.blur = None

        self.dilateCheck = None
        self.dilate = None

        self.areaCheck = None
        self.area = None

        # log
        self.log = None

        # GUI size
        screenSize = wx.DisplaySize()
        self.screenWidth = int(screenSize[0] * 0.95)
        self.screenHeight = int(screenSize[1] * 0.95)

        # init
        wx.Frame.__init__(self, parent, title=title, size=(wx.Size(self.screenWidth, self.screenHeight)))

        self.SetIcon(wx.Icon(settings.icon, wx.BITMAP_TYPE_PNG))

        self.createTopBar()
        self.GUI()  # create GUI
        self.Centre()
        self.Show()

    def createTopBar(self):
        self.CreateStatusBar()  # Create status bar in the bottom of window

        # setting up menu
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()
        helpMenu = wx.Menu()

        # items of fileMenu
        menuOpenImg = fileMenu.Append(wx.ID_OPEN, "Open image\s", " Open images")
        fileMenu.AppendSeparator()  # separator
        menuExit = fileMenu.Append(wx.ID_EXIT, "Exit", " Terminate the program")

        # items of helpMenu
        guideAbout = helpMenu.Append(wx.ID_ANY, "Guide", " How to use SPA ")
        helpMenu.AppendSeparator()  # separator
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "About", " Information about SPA")

        # Create menuBar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "File")  # Adding fileMenu to menuBar
        menuBar.Append(viewMenu, "View")  # Adding viewMenu to menuBar
        menuBar.Append(helpMenu, "Help")  # Adding helpMenu to MenuBar

        # Menu events
        self.Bind(wx.EVT_MENU, self.OnOpenImg, menuOpenImg)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnGuide, guideAbout)

        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content

    def GUI(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#FFFFFF')

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)

        gs = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)

        vbox.Add(gs, flag=wx.EXPAND)
        gs.AddMany([(vbox1, 0, wx.EXPAND), (vbox2, 0, wx.EXPAND)])

        vbox1.Add(hbox1, 0, wx.EXPAND)
        vbox1.Add(hbox2, 0, wx.EXPAND)
        vbox1.Add(hbox3, 0, wx.EXPAND)
        vbox1.Add(hbox4, 0, wx.EXPAND)
        vbox2.Add(hbox5, 0, wx.EXPAND)
        vbox2.Add(hbox6, 0, wx.EXPAND)
        vbox2.Add(hbox7, 0, wx.EXPAND)

        # FILE #######################################
        fileSelected = wx.StaticBox(self.panel, label='Files Selected',
                                    size=(wx.Size(self.screenWidth, self.screenHeight / 2.2)))
        fileSelected.SetBackgroundColour('#FFFFFF')
        fileSelectedSizer = wx.StaticBoxSizer(fileSelected, wx.VERTICAL)
        fileSelectedSizer.SetMinSize(self.screenWidth, self.screenHeight / 2.2)
        hbox1.Add(fileSelectedSizer, flag=wx.ALL | wx.EXPAND, border=4)

        self.files = wx.StaticText(fileSelected, label=self.checkFiles())

        fileSelectedSizer.Add(self.files, flag=wx.LEFT | wx.BOTTOM | wx.EXPAND, border=4)

        self.openFilesButton = wx.Button(self.panel, label='Open File/s')
        hbox2.Add(self.openFilesButton, flag=wx.ALL | wx.EXPAND, border=4)

        # PARAMS ####################################
        params = wx.StaticBox(self.panel, label='Parameters', size=(wx.Size(self.screenWidth, self.screenHeight / 2)))
        params.SetBackgroundColour('#FFFFFF')
        paramsSizer = wx.StaticBoxSizer(params, wx.VERTICAL)
        hbox3.Add(paramsSizer, flag=wx.ALL | wx.EXPAND, border=4)

        self.debugCheck = wx.CheckBox(params, label='Debug Mode')
        self.debugCheck.SetBackgroundColour('#FFFFFF')
        self.debugCheck.SetForegroundColour('black')
        debugBox = wx.BoxSizer(wx.HORIZONTAL)
        debugBox.Add(self.debugCheck, flag=wx.ALL | wx.EXPAND, border=4)

        self.panelCheck = wx.CheckBox(params, label='Panel Size')
        self.panelCheck.SetBackgroundColour('#FFFFFF')
        self.panelCheck.SetForegroundColour('black')
        self.widthPanel = wx.TextCtrl(params)
        self.heightPanel = wx.TextCtrl(params)
        panelSizeBox = wx.BoxSizer(wx.HORIZONTAL)
        panelSizeBox.Add(self.panelCheck, flag=wx.LEFT | wx.EXPAND, border=4)
        panelSizeBox.Add(self.widthPanel, flag=wx.LEFT | wx.EXPAND, border=9)
        panelSizeBox.Add(self.heightPanel, flag=wx.LEFT | wx.EXPAND, border=12)

        self.lowThreshCheck = wx.CheckBox(params, label='Low Thresh')
        self.lowThreshCheck.SetBackgroundColour('#FFFFFF')
        self.lowThreshCheck.SetForegroundColour('black')
        self.lowThresh = wx.TextCtrl(params)
        self.highThreshCheck = wx.CheckBox(params, label='High Thresh')
        self.highThreshCheck.SetBackgroundColour('#FFFFFF')
        self.highThreshCheck.SetForegroundColour('black')
        self.highThresh = wx.TextCtrl(params)
        self.threshButton = wx.ToggleButton(params, label='Auto Thresh')
        threshBox = wx.BoxSizer(wx.HORIZONTAL)
        threshBox.Add(self.lowThreshCheck, flag=wx.LEFT | wx.EXPAND, border=4)
        threshBox.Add(self.lowThresh, flag=wx.LEFT | wx.EXPAND, border=1)
        threshBox.Add(self.highThreshCheck, flag=wx.LEFT | wx.EXPAND, border=12)
        threshBox.Add(self.highThresh, flag=wx.LEFT | wx.EXPAND, border=4)
        threshBox.Add(self.threshButton, flag=wx.LEFT | wx.EXPAND, border=12)

        self.blurCheck = wx.CheckBox(params, label='Blur Value')
        self.blurCheck.SetBackgroundColour('#FFFFFF')
        self.blurCheck.SetForegroundColour('black')
        self.blur = wx.TextCtrl(params)
        blurBox = wx.BoxSizer(wx.HORIZONTAL)
        blurBox.Add(self.blurCheck, flag=wx.LEFT | wx.EXPAND, border=4)
        blurBox.Add(self.blur, flag=wx.LEFT | wx.EXPAND, border=9)

        self.dilateCheck = wx.CheckBox(params, label='Dilate Iters')
        self.dilateCheck.SetBackgroundColour('#FFFFFF')
        self.dilateCheck.SetForegroundColour('black')
        self.dilate = wx.TextCtrl(params)
        dilateBox = wx.BoxSizer(wx.HORIZONTAL)
        dilateBox.Add(self.dilateCheck, flag=wx.LEFT | wx.EXPAND, border=4)
        dilateBox.Add(self.dilate, flag=wx.LEFT | wx.EXPAND, border=8)

        self.areaCheck = wx.CheckBox(params, label='Area Lim (px)')
        self.areaCheck.SetBackgroundColour('#FFFFFF')
        self.areaCheck.SetForegroundColour('black')
        self.area = wx.TextCtrl(params)
        areaBox = wx.BoxSizer(wx.HORIZONTAL)
        areaBox.Add(self.areaCheck, flag=wx.LEFT | wx.EXPAND, border=4)
        areaBox.Add(self.area, flag=wx.LEFT | wx.EXPAND, border=8)

        paramsSizer.Add(debugBox, flag=wx.ALL | wx.EXPAND, border=4)
        paramsSizer.Add(panelSizeBox, flag=wx.ALL | wx.EXPAND, border=4)
        paramsSizer.Add(threshBox, flag=wx.ALL | wx.EXPAND, border=4)
        paramsSizer.Add(blurBox, flag=wx.ALL | wx.EXPAND, border=4)
        paramsSizer.Add(dilateBox, flag=wx.ALL | wx.EXPAND, border=4)
        paramsSizer.Add(areaBox, flag=wx.ALL | wx.EXPAND, border=4)

        self.launchButton = wx.Button(self.panel, label='Launch Elaboration')
        hbox4.Add(self.launchButton, flag=wx.ALL | wx.EXPAND, border=4)

        self.reset()

        # LOG #################################################
        self.log = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE,
                               size=(wx.Size(self.screenWidth, self.screenHeight / 2.5)))
        self.log.SetBackgroundColour('black')
        self.log.SetForegroundColour('green')
        hbox5.Add(self.log, flag=wx.LEFT | wx.EXPAND, border=4)
        # redirect cmd print to log panel
        sys.stdout = RedirectText(self.log)

        # VIEW #################################################
        self.viewButton = wx.Button(self.panel, label='View Panels')
        hbox6.Add(self.viewButton, flag=wx.ALL | wx.EXPAND, border=4)

        viewPanels = wx.StaticBox(self.panel, label='View Panels', size=(wx.Size(self.screenWidth, self.screenHeight / 2.5)))
        viewPanels.SetBackgroundColour('#FFFFFF')
        viewPanelsSizer = wx.StaticBoxSizer(viewPanels, wx.VERTICAL)
        viewPanelsSizer.SetMinSize(self.screenWidth, self.screenHeight / 2.5)
        hbox7.Add(viewPanelsSizer, flag=wx.ALL | wx.EXPAND, border=4)
        viewPanelsSizer.Add( wx.StaticText(viewPanels, label=' Not implemented in this version'), flag=wx.LEFT | wx.BOTTOM | wx.EXPAND, border=4)

        self.panel.SetSizerAndFit(vbox)

        # EVENTS ################################################
        self.Bind(wx.EVT_BUTTON, self.OnOpenImg, self.openFilesButton)
        self.Bind(wx.EVT_BUTTON, self.Elaborate, self.launchButton)
        self.widthPanel.Bind(wx.EVT_CHAR, self.onChar)
        self.heightPanel.Bind(wx.EVT_CHAR, self.onChar)
        self.lowThresh.Bind(wx.EVT_CHAR, self.onChar)
        self.highThresh.Bind(wx.EVT_CHAR, self.onChar)
        self.blur.Bind(wx.EVT_CHAR, self.onChar)
        self.dilate.Bind(wx.EVT_CHAR, self.onChar)
        self.area.Bind(wx.EVT_CHAR, self.onChar)

    def onChar(self, event):
        key = event.GetKeyCode()
        acceptable_characters = "1234567890."

        if chr(key) in acceptable_characters or key == wx.WXK_BACK:
            event.Skip()
            return

        else:
            return False

    def OnOpenImg(self, e):
        # Open file
        dlg = wx.FileDialog(self, "Choose an image or more", self.filesDir, "", "*.*", wx.FD_MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:

            self.filesSelected = dlg.GetFilenames()
            self.filesDir = dlg.GetDirectory()

            label = ''

            for file in self.filesSelected:
                f = open(os.path.join(self.filesDir, file), 'r')
                label = label + self.filesDir + '/' + file + '\n'

            self.files.SetLabel(label)
            f.close()
            dlg.Destroy()

            string = "Would you want to use recommended values?"
            string = string + "\n\nATTENTION:\nPressing YES values will be set.\n(Flag check boxes you want to use!)"
            recommendedDialog = wx.MessageDialog(None, string, "Recommended values", wx.YES_NO)

            if recommendedDialog.ShowModal() == wx.ID_YES:

                fileType = self.extractFile(self.filesSelected[0])

                # recommended values set
                if fileType == '.tif' or fileType == '.tiff' or fileType == '.TIF' or fileType == '.TIFF':
                    self.widthPanel.SetValue('')
                    self.heightPanel.SetValue('')
                    self.lowThresh.SetValue(str(settings.TIFF_LOW))
                    self.highThresh.SetValue(str(settings.TIFF_HIGH))
                    self.blur.SetValue(str(settings.TIFF_BLUR))
                    self.dilate.SetValue(str(settings.TIFF_DILATE))
                    self.area.SetValue(str(settings.TIFF_AREA))
                elif fileType == '.jpg' or fileType == '.jpeg' or fileType == '.JPG' or fileType == '.JPEG':
                    self.widthPanel.SetValue('')
                    self.heightPanel.SetValue('')
                    self.lowThresh.SetValue(str(settings.JPG_LOW))
                    self.highThresh.SetValue(str(settings.JPG_HIGH))
                    self.blur.SetValue(str(settings.JPG_BLUR))
                    self.dilate.SetValue(str(settings.JPG_DILATE))
                    self.area.SetValue(str(settings.JPG_AREA))
                    pass
                else:
                    self.reset()

    def checkFiles(self):
        if self.filesSelected is None:
            label = 'No Files'
        else:
            for file in self.filesSelected:
                label = label + self.filesDir + '/' + file + '\n'

        return label

    def Elaborate(self, e):
        if self.filesSelected == '' or self.filesSelected is None:
            dlg = wx.MessageDialog(self, "ERROR - No file selected!", "ERROR", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            string = "Are you sure to elaborate following images?"
            for file in self.filesSelected:
                string = string + '\n' + file
            elBox = wx.MessageDialog(None, string, "Elaboration", wx.YES_NO)

            if elBox.ShowModal() == wx.ID_YES:

                # name folder
                if len(self.filesSelected) > 1:
                    settings.SPA.setSaveDir(
                        settings.SPA.getSaveDir() + '/Plant_' + str(datetime.datetime.now().strftime("%d-%m-%Y_%H.%M")))

                i = 0

                self.readParams()

                self.waitCursorMode()

                for file in self.filesSelected:
                    newImg = Image.Image(id=i, filepath=self.filesDir + '/' + file)

                    el = Elaboration.Elaboration(id=i, sourceImg=newImg)
                    el.launchProcedure()  # call procedure of elaboration

                    if i == 0:
                        totalTime = el.getExeTime()
                    else:
                        totalTime = totalTime + el.getExeTime()

                    i = i + 1

                self.resetCursorMode()

                if el.getStatus() is 4:

                    if i > 1:
                        message = 'PROCEDURE COMPLETED!\n\n' + str(i) + ' images processed successfully!\n\n'
                        message = message + 'PROCESSING TIME: ' + str(totalTime) + '\n\n'
                        message = message + 'OUTPUT FOLDER:\n' + str(settings.SPA.getSaveDir())

                    else:
                        message = 'PROCEDURE COMPLETED!\n\n' + str(
                            newImg.getFilename()) + ' PROCESSED SUCCESSFULLY!\n\n'
                        message = message + 'PANELS DETECTED: ' + str(newImg.getPanels()) + '\n'
                        message = message + 'PROCESSING TIME: ' + str(totalTime).split(":")[2] + ' seconds!\n\n'
                        message = message + 'OUTPUT FOLDER:\n' + str(settings.SPA.getSaveDir())

                    message = message + '\n\n- PARAMETERS -\n'
                    message = message + 'Debug Mode: ' + str(settings.SPA.checkDebugMode())

                    if settings.SPA.checkDim()[0] is not None and settings.SPA.checkDim()[1] is not None:
                        message = message + '\nPanels Size: ' + str(settings.SPA.checkDim()[0]) + ' x ' + str(
                            settings.SPA.checkDim()[1])
                        message = message + '\nRate: ' + str(
                            int(settings.SPA.checkDim()[0]) / int(settings.SPA.checkDim()[1]))
                    else:
                        message = message + '\nPanels Size: Unknown'
                        message = message + '\nRate: ' + str(settings.RATE_DEFAULT) + ' (default)'

                    params = settings.SPA.getParams()

                    if settings.SPA.getParams()[settings.AUTOTHRESH_PARAM]:
                        message = message + '\nAuto Thresh: ' + str(settings.autoThreshValue)
                    else:
                        message = message + '\nLow Thresh: ' + params[settings.LOWTHRESH_PARAM]
                        message = message + '\nHigh Thresh: ' + params[settings.HIGHTHRESH_PARAM]
                    message = message + '\nBlur: ' + params[settings.BLUR_PARAM]
                    message = message + '\nDilate: ' + params[settings.DILATE_PARAM]
                    message = message + '\nArea Min: ' + params[settings.MINAREA_PARAM]

                    dlg = wx.MessageDialog(self, message, "SUCCESS", wx.OK)
                    print('\n----------------------------------')
                    print('OUTPUT MESSAGE:\n')
                    print(message)

                else:
                    dlg = wx.MessageDialog(self, 'ELABORATION IS FAILED!', "ERROR", wx.OK)

                settings.SPA.resetSaveDir()
                dlg.ShowModal()
                dlg.Destroy()

            elBox.Destroy()

    def OnAbout(self, e):
        # dialog box with OK button
        message = 'Solar Panel Analyzer (SPA)\n'
        message = message + 'was developed by Jacopo De Luca\n\n'
        message = message + 'This is the result of a practical project of Software Engineering course\n'
        message = message + 'DIBRIS - Università degli Studi di Genova (Italy)\n\n'
        message = message + 'SPA was made for WeSii s.r.l and\n'
        message = message + 'ALL RIGHTS ARE RESERVED (2018)\n\n'
        message = message + 'jacopodeluca.private@gmail.com'

        dlg = wx.MessageDialog(self, message, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnGuide(self, e):
        # dialog box with OK button
        message = 'How to use Solar Panel Analyzer (SPA)\n\n'
        message = message + 'SPA works with JPG anf TIF files.\n'
        message = message + 'More precisely, SPA works with dataset owned by WeSii s.r.l, which consists in RGB images collection captured during the flight of the drone.\n'
        message = message + 'In desinging and developing phases there were three kinds of images, which are considered by SPA.\n'
        message = message + 'SPA needs some parameters to accomplish fast and precisely the elaboration. This values are result of tests and they could be different for different pictures from those analyzed.\n'
        message = message + '\nReccomended values are the following.\n\n'
        message = message + '1) JPG:\n'
        message = message + ' Low Threshold - 100\n'
        message = message + ' High Threshold - 200\n'
        message = message + ' Blur - 8\n'
        message = message + ' Dilate iters - 2\n'
        message = message + ' Min area - 10000\n\n'
        message = message + '2) JPG (second collection):\n'
        message = message + ' Low Threshold - 150\n'
        message = message + ' High Threshold - 400\n'
        message = message + ' Blur - 8\n'
        message = message + ' Dilate iters - 1\n'
        message = message + ' Min area - 500000\n\n'
        message = message + '3) TIF:\n'
        message = message + ' Low Threshold - 100\n'
        message = message + ' High Threshold - 200\n'
        message = message + ' Blur - 8\n'
        message = message + ' Dilate iters - 1\n'
        message = message + ' Min area - 12500000\n\n'
        message = message + 'It is recommended to take note of the above values.\n'
        message = message + 'However, a method for parameter configuration has been devised, but has not yet been developed.\n\n'
        message = message + '"Debug Mode" of SPA saves all of procedure steps , in this way the user can check the right functioning.\n'
        message = message + 'It is also recommended to insert the dimensions of panels which user want to find. SPA computes the ratio to improve their detection.\n\n'
        message = message + 'SPA also collects data about source image and detected panels, in this way it can generate two different files:\n'
        message = message + '- report.CSV, which includes info about panels\n'
        message = message + '- metadata.XML, which includes metadata of source image.\n'
        message = message + 'GPS coordinates are taken from metadata (feature not implemented for TIF images).\n\n'
        message = message + 'Finally SPA generates "particular_data.XML" which contains all the info about elaboration.\n'
        message = message + 'The goal should be a XML file creation with data referred to general plant, omitting double info about the same panel.\n'
        message = message + 'Developing this functioning requires more time and knowledge, an "ad-hoc" recognition algorithm should be devised, and for these reasons it was not developed.\n'
        dlg = wx.MessageDialog(self, message, "Guide - How to use", wx.OK)
        dlg.Fit()
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        decisionalBox = wx.MessageDialog(None, 'Are you sure to quit?', 'Quit', wx.YES_NO)

        if decisionalBox.ShowModal() == wx.ID_YES:
            self.Close(True)

        decisionalBox.Destroy()

    def readParams(self):

        params = list()

        if self.debugCheck.IsChecked():
            params.insert(settings.DEBUG_PARAM, True)
        else:
            params.insert(settings.DEBUG_PARAM, None)

        if self.panelCheck.IsChecked() and self.widthPanel.GetValue() != '' and self.heightPanel.GetValue() != '':
            dim = [self.widthPanel.GetValue(), self.heightPanel.GetValue()]
            params.insert(settings.DIM_PARAM, dim)
        else:
            params.insert(settings.DIM_PARAM, [None, None])

        if self.threshButton.GetValue():
            params.insert(settings.AUTOTHRESH_PARAM, True)
            self.lowThreshCheck.SetValue(False)
            self.highThreshCheck.SetValue(False)
            self.lowThresh.SetValue('')
            self.highThresh.SetValue('')
            params.insert(settings.LOWTHRESH_PARAM, 0)
            params.insert(settings.HIGHTHRESH_PARAM, 255)
        else:
            params.insert(settings.AUTOTHRESH_PARAM, False)
            if self.lowThreshCheck.IsChecked() and self.lowThresh.GetValue() != '':
                params.insert(settings.LOWTHRESH_PARAM, self.lowThresh.GetValue())
            else:
                params.insert(settings.LOWTHRESH_PARAM, settings.LOWTHRESH_DEFAULT)
            if self.highThreshCheck.IsChecked() and self.highThresh.GetValue() != '':
                params.insert(settings.HIGHTHRESH_PARAM, self.highThresh.GetValue())
            else:
                params.insert(settings.HIGHTHRESH_PARAM, settings.HIGHTHRESH_DEFAULT)

        if self.blurCheck.IsChecked() and self.blur.GetValue() != '':
            params.insert(settings.BLUR_PARAM, self.blur.GetValue())
        else:
            params.insert(settings.BLUR_PARAM, settings.BLUR_DEFAULT)

        if self.dilateCheck.IsChecked() and self.dilate.GetValue() != '':
            params.insert(settings.DILATE_PARAM, self.dilate.GetValue())
        else:
            params.insert(settings.DILATE_PARAM, settings.DILATE_DEFAULT)

        if self.areaCheck.IsChecked() and self.area.GetValue() != '':
            params.insert(settings.MINAREA_PARAM, self.area.GetValue())
        else:
            params.insert(settings.MINAREA_PARAM, settings.MINAREA_DEFAULT)

        settings.SPA.setParams(params)

    def extractFile(self, filename):
        filename, file_extension = os.path.splitext(filename)
        return file_extension

    def reset(self):
        self.files.SetLabel("No Files")
        self.filesSelected = None
        self.filesDir = ''

        self.debugCheck.SetValue(False)
        self.panelCheck.SetValue(False)
        self.threshButton.SetValue(False)
        self.lowThreshCheck.SetValue(False)
        self.highThreshCheck.SetValue(False)
        self.blurCheck.SetValue(False)
        self.dilateCheck.SetValue(False)
        self.areaCheck.SetValue(False)

        self.widthPanel.SetValue('')
        self.heightPanel.SetValue('')
        self.lowThresh.SetValue(settings.LOWTHRESH_DEFAULT)
        self.highThresh.SetValue(settings.HIGHTHRESH_DEFAULT)
        self.blur.SetValue(settings.BLUR_DEFAULT)
        self.dilate.SetValue(settings.DILATE_DEFAULT)
        self.area.SetValue(settings.MINAREA_DEFAULT)

    def waitCursorMode(self):
        myCursor = wx.StockCursor(wx.CURSOR_WAIT)
        self.panel.SetCursor(myCursor)

    def resetCursorMode(self):
        myCursor = wx.StockCursor(wx.CURSOR_DEFAULT)
        self.panel.SetCursor(myCursor)

# class to redirect cmd messages
class RedirectText:
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)
