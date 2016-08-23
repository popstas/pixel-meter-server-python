#!/usr/bin/python

import wx
import time
from lib import *
from lib.PixelServer import PixelServer
from lib.PixelServerHandler import PixelServerHandler
from lib.PixelTrayIcon import PixelTrayIcon
from pubsub import pub

class TaskBarFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, style=wx.FRAME_NO_TASKBAR)
        #panel = wx.Panel(self)
        self.tbicon = PixelTrayIcon(self, 'images/icon.png', 'Pixel server')
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.server = PixelServer(PixelServerHandler, comportname=config['comportname'], tcpport=8035)
        time.sleep(2)
        self.server.startServer()
        pub.sendMessage('pixel', val='199', msg='server started', bright='10', source='self')
        time.sleep(2)
        pub.sendMessage('pixel', val='-1')

    def onClose(self, evt):
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        self.server.HTTPServer.socket.close()  # TODO: server exit with exception
        self.Destroy()

def main():
    app = wx.App(False)
    TaskBarFrame()

    #server.info()

    app.MainLoop()


if __name__ == '__main__':
    main()

