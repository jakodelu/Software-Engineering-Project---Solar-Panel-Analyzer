import wx

import settings
import System

if __name__ == '__main__':
    app = wx.App(redirect=False)
    settings.SPA = System.System()
    app.MainLoop()
