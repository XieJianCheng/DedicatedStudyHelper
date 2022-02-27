# coding:utf-8

import os
import wx
import ctypes
import re
import random

# 是否关机
shutdown_state = True

# 获取屏幕尺寸，为了适配1920*1080分辨率以上的屏幕
winapi = ctypes.windll.user32
screen_x = winapi.GetSystemMetrics(0)
screen_y = winapi.GetSystemMetrics(1)


def read_ini():
    # 读取配置
    with open('../BSOD.ini', 'r+', encoding='utf-8') as fo:
        got_all = fo.readlines()
        got_color = got_all[0]
        got_face = got_all[1]
        got_bsod = got_all[2]
        got_size = got_all[3]

    # 处理
    processed_got_color = got_color
    processed_got_face = got_face.strip()[1:-1]
    processed_got_bsod = got_bsod.strip()
    processed_got_size = got_size.strip()

    # 得到最后的参数
    final_color = []  # 颜色
    re_color = r'[0-9]'
    tmp_color = ''
    for i in processed_got_color:
        if i == ',' or i == '\n':
            final_color.append(int(tmp_color))
            tmp_color = ''  # 清空
        found = re.findall(re_color, i)
        if len(found) == 1:
            tmp_color += i
        found = []  # 清空
    print(f'final_color:{final_color}')  # debugging
    tuple(final_color)
    final_face = processed_got_face  # 脸
    final_bsod = processed_got_bsod  # 要调用蓝屏

    # 返回结果
    return final_color, final_face, final_bsod


def read_word():
    # 读取
    with open('../data/BSOD.txt', 'r+', encoding='utf-8') as fo:
        got_list = fo.readlines()
        got_str = """"""
        for i in got_list:
            got_str += i
        got_str = got_str.strip()

    # 返回结果
    return got_str


run_read_ini = read_ini()  # 读取配置
run_read_word = read_word()  # 读取文字


class blue_screen_win10(wx.Frame):
    size = (screen_x + 18, screen_y + 43)       # 窗口大小

    # 加载百分比
    load_num = 0
    stop_state = False

    def __init__(self, parent=None, id=-1):
        # 初始化
        wx.Frame.__init__(self, parent, id, 'BSOD', pos=(-8, -35))
        wx.Frame.SetMinSize(self, size=self.size)
        wx.Frame.SetMaxSize(self, size=self.size)
        wx.Frame.SetSize(self, size=self.size)
        pnl = wx.Panel(self)

        # 文字控件
        word_face = wx.StaticText(pnl, label=run_read_ini[1])   # :(
        word_contents_1 = wx.StaticText(pnl, label='你的设备遇到问题，需要关机。\n我们只收集某些错误信息，然后为你关闭电脑。')
        self.word_contents_2 = wx.StaticText(pnl, label=f'{str(self.load_num)}%完成')
        img = wx.Image('../image/QR.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()  # 假二维码
        show_img = wx.StaticBitmap(pnl, -1, img, (img.GetWidth(), img.GetHeight()))  # 假二维码
        # 获取显示在蓝屏的路径
        file_dir = __file__[0:-len(re.findall(r'\w+.[py|w]+$', __file__)[0]) - 1]
        word_more_1 = wx.StaticText(pnl, label=f'有关此问题的详细信息和可能的解决方法，请访问\n{file_dir}')
        word_more_2 = wx.StaticText(pnl, label=f'如果致电支持人员，请向他们提供以下信息：\n终止代码：{run_read_word}\n失败的操作：wininit.exe')

        # 布局
        sizer_v_info = wx.BoxSizer(wx.VERTICAL)
        sizer_v_info.Add(word_more_1, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.BOTTOM, border=32)
        sizer_v_info.Add(word_more_2, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.TOP, border=32)
        sizer_h_info = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_info.Add(show_img, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.RIGHT, border=60)
        sizer_h_info.Add(sizer_v_info, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP)
        sizer_v_all = wx.BoxSizer(wx.VERTICAL)
        sizer_v_all.Add(word_face, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.BOTTOM, border=5)
        sizer_v_all.Add(word_contents_1, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.BOTTOM, border=40)
        sizer_v_all.Add(self.word_contents_2, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.BOTTOM, border=33)
        sizer_v_all.Add(sizer_h_info, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP)
        sizer_h_all = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_all.Add(sizer_v_all, proportion=0, flag=wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.LEFT | wx.TOP, border=100)
        pnl.SetSizer(sizer_h_all)

        # 字体
        font_face = wx.Font(pointSize=122, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='Microsoft YaHei')
        font_contents = wx.Font(pointSize=40, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                                faceName='Microsoft YaHei')
        font_more = wx.Font(pointSize=23, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='Microsoft YaHei')
        word_face.SetFont(font_face)
        word_contents_1.SetFont(font_contents)
        self.word_contents_2.SetFont(font_contents)
        word_more_1.SetFont(font_more)
        word_more_2.SetFont(font_more)

        # 颜色
        color_background = run_read_ini[0]
        color_contents = (255, 255, 255)
        pnl.SetBackgroundColour(color_background)
        word_face.SetForegroundColour(color_contents)
        word_contents_1.SetForegroundColour(color_contents)
        self.word_contents_2.SetForegroundColour(color_contents)
        word_more_1.SetForegroundColour(color_contents)
        word_more_2.SetForegroundColour(color_contents)

        # 图标
        try:
            open('image/icon_BSOD.ico', 'rb')
        except FileNotFoundError:
            print("没有找到图标文件")
        else:
            self.icon = wx.Icon(name="image/icon_BSOD.ico", type=wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.icon)

        self.ctrl_loading()

    def ctrl_loading(self):
        if shutdown_state is True and self.load_num >= 100:     # 关机条件：1、shutdown_state是True 2、百分比到了100
            self.shutdown()
        else:
            rand_load = random.randint(84, 98)
            if self.load_num >= rand_load and shutdown_state is False:      # 停止加载条件
                self.stop_state = True
            else:       # 否则继续加大数字
                rand_time = random.randint(5, 200)
                wx.FutureCall(rand_time, self.ctrl_load)        # 这里和下面……

    def ctrl_load(self):
        self.load_num += 1
        self.word_contents_2.SetLabel(f'{self.load_num}%完成')

        if self.stop_state is False:
            self.ctrl_loading()                                 # ……这里和上面组成迭代

    @staticmethod
    def shutdown():
        os.system('shutdown -s -t 0')



if __name__ == '__main__':
    app = wx.App()
    frame = blue_screen_win10(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
