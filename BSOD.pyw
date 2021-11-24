from helper import blue_screen
import wx

app = wx.App()
frame = blue_screen('show', '0', '0', '0', '0', parent=None, id=-1)
frame.Show()
app.MainLoop()
