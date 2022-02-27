# coding: utf-8

# 这是复刻蓝屏的等比例缩小版
# 只支持复刻win10蓝屏
# 可以在图片资源存在的情况下自由内嵌

# 兼容1680*1050和1920*1080下125%、150%、175%缩放
# 兼容1680*1050分辨率以下各种缩放
# 1680*1050及以上分辨率的100%缩放在完整版兼容更好
# 800*600完全不兼容

import wx
import ctypes


class blue_screen_win10(wx.Frame):
    winapi = ctypes.windll.user32
    screen_x = winapi.GetSystemMetrics(0)
    screen_y = winapi.GetSystemMetrics(1)

    size = (screen_x+18, screen_y+43)

    def __init__(self, parent=None, id=-1):
        # 初始化
        wx.Frame.__init__(self, parent, id, 'BSOD', pos=(-8, -35))
        wx.Frame.SetMinSize(self, size=self.size)
        wx.Frame.SetMaxSize(self, size=self.size)
        wx.Frame.SetSize(self, size=self.size)
        pnl = wx.Panel(self)

        # 文字控件
        word_face = wx.StaticText(pnl, label=':(', pos=(100, 50))
        word_contents_1 = wx.StaticText(pnl, label='你的设备遇到问题，需要关机。\n我们只收集某些错误信息，然后为你关闭电脑。', pos=(100, 200))
        word_contents_2 = wx.StaticText(pnl, label='90%完成', pos=(100, 325))
        img = wx.Image('QR_small.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()                  # 假二维码
        wx.StaticBitmap(pnl, -1, img, (100, 400), (img.GetWidth(), img.GetHeight()))    # 假二维码
        word_more_1 = wx.StaticText(pnl, label='有关此问题的详细信息和可能的解决方法，请访问\nhttps://www.microsoft.com/', pos=(305, 405))
        word_more_2 = wx.StaticText(pnl, label=f'如果致电支持人员，请向他们提供以下信息：\n终止代码：Your PC is not happy\n失败的操作：explorer.exe', pos=(305, 485))

        # 字体
        font_face = wx.Font(pointSize=81, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='Microsoft YaHei')
        font_contents = wx.Font(pointSize=25, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                                faceName='Microsoft YaHei')
        font_more = wx.Font(pointSize=16, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='Microsoft YaHei')
        word_face.SetFont(font_face)
        word_contents_1.SetFont(font_contents)
        word_contents_2.SetFont(font_contents)
        word_more_1.SetFont(font_more)
        word_more_2.SetFont(font_more)

        # 颜色
        color_background = (0, 124, 224)
        color_contents = (255, 255, 255)
        pnl.SetBackgroundColour(color_background)
        word_face.SetForegroundColour(color_contents)
        word_contents_1.SetForegroundColour(color_contents)
        word_contents_2.SetForegroundColour(color_contents)
        word_more_1.SetForegroundColour(color_contents)
        word_more_2.SetForegroundColour(color_contents)


def run_blue():
    # 假蓝屏窗口
    app_blue = wx.App()

    frame_blue = blue_screen_win10(parent=None, id=-1)

    frame_blue.Show()
    # 运行到这里就会进入窗口循环
    app_blue.MainLoop()


run_blue()

# 这其实主要是为了教室电脑而打造的hhh
