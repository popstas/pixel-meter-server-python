import wx
from pubsub import pub


class PixelTrayIcon(wx.TaskBarIcon):
    TBMENU_RESTORE = wx.NewId()
    TBMENU_LOG = wx.NewId()
    TBMENU_CLOSE = wx.NewId()

    def __init__(self, frame, icon, tooltip):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame

        self.tooltip = tooltip
        self.set_icon(icon)

        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

        pub.subscribe(self.pixelListener, 'pixel')

    def pixelListener(self, val, msg='', bright='', source=''):
        print(val, msg, bright, source)
        if val != '-1':
            self.ShowBalloon(source, msg)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        # menu.Append(self.TBMENU_RESTORE, "Open Program")
        # menu.Append(self.TBMENU_LOG, "Show log")
        # menu.AppendSeparator()
        menu.Append(self.TBMENU_CLOSE, "Exit")
        return menu

    def set_icon(self, path):
        # icon = wx.TaskBarIcon()
        #icon.SetIcon(icon, self.tooltip)
        icons = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icons, self.tooltip)

    def OnTaskBarActivate(self, evt):
        """"""
        pass

    # ----------------------------------------------------------------------
    def OnTaskBarClose(self, evt):
        """
        Destroy the taskbar icon and frame from the taskbar icon itself
        """
        self.frame.Close()

    #----------------------------------------------------------------------
    def OnTaskBarLeftClick(self, evt):
        """
        Create the right-click menu
        """
        menu = self.CreatePopupMenu()
        self.PopupMenu(menu)
        menu.Destroy()
