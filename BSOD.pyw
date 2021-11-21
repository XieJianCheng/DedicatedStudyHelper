import helper
import wx

app = wx.App()
frame = helper.blue_screen('0', '0', '0', '0', parent=None, id=-1, show_state=True)
frame.Show()
app.MainLoop()