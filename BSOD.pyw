import helper
import wx

app = wx.App()
frame = helper.run_blue('show')
try:
    frame.Show()
except:
    pass
app.MainLoop()
