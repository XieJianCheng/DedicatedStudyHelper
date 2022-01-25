# coding: utf-8

"""
期中考前最后的一个项目，为了专注学习

开始时间 2021.11.8 20:25
"""

import re
import os
import time
import wx
from module import EAD
import ctypes

# 版本号
version = 'v1.6.10'

# 获取屏幕尺寸，为了适配1920*1080分辨率以上的屏幕
winapi = ctypes.windll.user32
screen_x = winapi.GetSystemMetrics(0)
screen_y = winapi.GetSystemMetrics(1)

########################################################################################################################


class commands:
    @staticmethod
    def GetReadSave_time(run_mode):
        # %m月 %d日 %H时 %M分
        now_month = time.strftime('%m')
        now_day = time.strftime('%d')
        now_hour = time.strftime('%H')
        now_minute = time.strftime('%M')

        if os.path.exists('data/record.txt') is False:
            fo_f = open('data/record.txt', 'w+', encoding='utf-8')
            _str_now_mouth = now_month
            _str_now_day = now_day
            _str_now_hour = now_hour
            _str_now_minute = now_minute

            write_string = EAD.compiling(f'{_str_now_mouth}{_str_now_day}{_str_now_hour}{_str_now_minute}',
                                         EAD.password_character_set(True))

            fo_f.write(write_string)
            fo_f.close()

        if run_mode == 'get':
            return now_month, now_day, now_hour, now_minute

        elif run_mode == 'read':
            with open('data/record.txt', 'r+', encoding='utf-8') as fo2:
                got = EAD.decoding(fo2.readlines()[0], EAD.password_character_set(False))
                print(got)
            return got[0: 2], got[2: 4], got[4: 6], got[6:]

        elif run_mode == 'save':
            str_now_mouth = now_month
            str_now_day = now_day
            str_now_hour = now_hour
            str_now_minute = now_minute

            write_string = EAD.compiling(f'{str_now_mouth}{str_now_day}{str_now_hour}{str_now_minute}',
                                         EAD.password_character_set(True))

            with open('data/record.txt', 'w+', encoding='utf-8') as fo:
                fo.write(write_string)

    @staticmethod
    def set_duration_time(control_month: str, control_day: str, control_hour: str, control_minute: str):
        if len(control_month) == 1:
            control_month = f'0{control_month}'
        if len(control_day) == 1:
            control_day = f'0{control_day}'
        if len(control_hour) == 1:
            control_hour = f'0{control_hour}'
        if len(control_minute) == 1:
            control_minute = f'0{control_minute}'

        with open('data/duration.txt', 'w+', encoding='utf-8') as fo1:
            fo1.write(EAD.compiling(f'{control_month}{control_day}{control_hour}{control_minute}',
                                    EAD.password_character_set(True)))

    @staticmethod
    def read_duration():
        if os.path.exists('data/duration.txt') is False:
            fo_f = open('data/duration.txt', 'w+', encoding='utf-8')
            fo_f.write(EAD.compiling('00000000', EAD.password_character_set(True)))
            fo_f.close()
        with open('data/duration.txt', 'r+', encoding='utf-8') as fo1:
            got = EAD.decoding(fo1.readlines()[0], EAD.password_character_set(False))
            print(got)

        duration_month = int(got[0:2])
        duration_day = int(got[2:4])
        duration_hour = int(got[4:6])
        duration_minute = int(got[6:])

        # 现在时间-记录时间
        disparity_month = int(commands.GetReadSave_time('get')[0]) - int(commands.GetReadSave_time('read')[0])
        disparity_day = int(commands.GetReadSave_time('get')[1]) - int(commands.GetReadSave_time('read')[1])
        disparity_hour = int(commands.GetReadSave_time('get')[2]) - int(commands.GetReadSave_time('read')[2])
        disparity_minute = int(commands.GetReadSave_time('get')[3]) - int(commands.GetReadSave_time('read')[3])

        # 计算总时差
        ########
        all_minute_disparity = 0
        all_hour_disparity = 0
        all_day_disparity = 0
        all_month_disparity = 0
        ####
        all_month_disparity += 0 + disparity_month
        all_day_disparity += all_month_disparity * 30 + disparity_day
        all_hour_disparity += all_day_disparity * 24 + disparity_hour
        all_minute_disparity += all_hour_disparity * 60 + disparity_minute
        ########
        all_minute_duration = 0
        all_hour_duration = 0
        all_day_duration = 0
        all_month_duration = 0
        ####
        all_month_duration += 0 + duration_month
        all_day_duration += all_month_duration * 30 + duration_day
        all_hour_duration += all_day_duration * 24 + duration_hour
        all_minute_duration += all_hour_duration * 60 + duration_minute

        print(f'all: {all_minute_disparity} {all_minute_duration}')

        if all_minute_disparity >= all_minute_duration:
            return True  # 到时间
        else:
            return False  # 没到时间

    @staticmethod
    def shutdown():
        print('in commands.shutdown()')
        os.system('shutdown -s -t 3 -c 还没到时间不能开机，好好去复习')


cmds = commands()


########################################################################################################################


def read_ini():
    # 读取配置
    with open('BSOD.ini', 'r+', encoding='utf-8') as fo:
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
    with open('data/BSOD.txt', 'r+', encoding='utf-8') as fo:
        got_list = fo.readlines()
        got_str = """"""
        for i in got_list:
            got_str += i
        got_str = got_str.strip()

    # 返回结果
    return got_str


run_read_ini = read_ini()  # 读取配置
run_read_word = read_word()  # 读取文字


class blue_screen_win98(wx.Frame):
    size = (screen_x + 18, screen_y + 43)

    def __init__(self, run_state='show', mo='0', da='0', ho='0', mi='0', parent=None, id=-1):
        # 初始化
        wx.Frame.__init__(self, parent, id, 'BSOD', pos=(-10, -35))
        wx.Frame.SetMinSize(self, size=self.size)
        wx.Frame.SetMaxSize(self, size=self.size)
        wx.Frame.SetSize(self, size=self.size)
        pnl = wx.Panel(self)

        # 文字
        word_main = """A fatal exception 0E has occurred at 0028:C0034B23.    The current
application will be terminated.

*    Press any key to terminate the current application.
*    Press CTRL+ALT+DEL again to restart your computer.  You will
      lose any unsaved information in all applications."""

        # 控件
        show_title = wx.StaticText(pnl, label='Windows')
        show_word = wx.StaticText(pnl, label=word_main)
        show_next = wx.StaticText(pnl, label='Press any key to continue _')

        # 颜色
        color_bg = (28, 0, 176)
        color_title_bg = (168, 168, 168)
        color_title_word = (30, 2, 176)
        color_word_main = (249, 248, 253)
        color_next = (249, 248, 253)
        pnl.SetBackgroundColour(color_bg)
        show_title.SetBackgroundColour(color_title_bg)
        show_title.SetForegroundColour(color_title_word)
        show_word.SetForegroundColour(color_word_main)
        show_next.SetForegroundColour(color_next)

        # 字体
        font_all = wx.Font(pointSize=12, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                           faceName='NSimSun')
        show_title.SetFont(font_all)
        show_title.SetFont(font_all)
        show_word.SetFont(font_all)
        show_next.SetFont(font_all)

        # 布局
        sizer_h_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_1.Add(show_title, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_2.Add(show_word, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_3.Add(show_next, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(sizer_h_1, proportion=1, flag=wx.ALIGN_CENTER)
        sizer_v.Add(sizer_h_2, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_v.Add(sizer_h_3, proportion=1, flag=wx.ALIGN_CENTER)
        pnl.SetSizer(sizer_v)

        # 图标
        try:
            open('image/icon_BSOD.ico', 'rb')
        except FileNotFoundError:
            print("没有找到图标文件")
        else:
            self.icon = wx.Icon(name="image/icon_BSOD.ico", type=wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.icon)

        if run_state == 'show':
            pass
        elif run_state == 'shutdown':
            cmds.shutdown()
        elif run_state == 'record':
            main(mo, da, ho, mi)


class blue_screen_winxp(wx.Frame):
    size = (screen_x + 18, screen_y + 43)

    def __init__(self, run_state='show', mo='0', da='0', ho='0', mi='0', parent=None, id=-1):
        # 初始化
        wx.Frame.__init__(self, parent, id, 'BSOD', pos=(-10, -35))
        wx.Frame.SetMinSize(self, size=self.size)
        wx.Frame.SetMaxSize(self, size=self.size)
        wx.Frame.SetSize(self, size=self.size)
        pnl = wx.Panel(self)

        # 文字
        word_all = """One of your disks needs to be checked for consistency. You
may cancel the disk check, but it is strongly recommended
that you continue.
windows will now check the disk.

CHKDSK is verifying files (stage 1 of 3) ...
File verificatioin completed.
CHKDSK is verifying indexes (stage 1 of 3) ...
..
Checking file system of C:
The type of the file system is NTFS.

CHKDSK is verifying files (stage 1 of 3) ...
File verificatioin completed.
CHKDSK is verifying indexes (stage 1 of 3) ...
..
Checking file system of D:
The type of the file system is NTFS.

CHKDSK is verifying files (stage 1 of 3) ...
File verificatioin completed.
CHKDSK is verifying indexes (stage 1 of 3) ...
..
Checking file system of E:
The type of the file system is NTFS.

CHKDSK is verifying files (stage 1 of 3) ...
File verificatioin completed.
CHKDSK is verifying indexes (stage 1 of 3) ...
..
Checking file system of F:
The type of the file system is NTFS.

One of your disks needs to be checked for consistency. You
may cancel the disk check, but it is strongly recommended
that you continue.
windows will now check the disk.

CHKDSK is verifying files (stage 1 of 3) ...
File verification completed.
CHKDSK is verifying indexes (stage 2 of 3) ...
An unspecified error occurred."""
        # 控件
        show_word = wx.StaticText(pnl, label=word_all, pos=(100, 100))
        img = wx.Image('image/xplogo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()  # 假二维码
        wx.StaticBitmap(pnl, -1, img, (1730, 30), (img.GetWidth(), img.GetHeight()))  # 假二维码

        # 颜色
        color_word = (240, 240, 240)
        color_bg = (90, 126, 220)
        show_word.SetForegroundColour(color_word)
        pnl.SetBackgroundColour(color_bg)

        # 字体
        font_word = wx.Font(pointSize=12, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='NSimSun')
        show_word.SetFont(font_word)

        # 图标
        try:
            open('image/icon_BSOD.ico', 'rb')
        except FileNotFoundError:
            print("没有找到图标文件")
        else:
            self.icon = wx.Icon(name="image/icon_BSOD.ico", type=wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.icon)

        if run_state == 'show':
            pass
        elif run_state == 'shutdown':
            cmds.shutdown()
        elif run_state == 'record':
            main(mo, da, ho, mi)


class blue_screen_win7(wx.Frame):
    size = (screen_x + 18, screen_y + 43)

    def __init__(self, run_state='show', mo='0', da='0', ho='0', mi='0', parent=None, id=-1):
        # 初始化
        wx.Frame.__init__(self, parent, id, 'BSOD', pos=(-10, -35))
        wx.Frame.SetMinSize(self, size=self.size)
        wx.Frame.SetMaxSize(self, size=self.size)
        wx.Frame.SetSize(self, size=self.size)
        pnl = wx.Panel(self)

        # 蓝屏文字
        word_all = """A problem has been detected and windows has been shut down to prevent damage to you computer.

INTERRUPT_EXCEPTION_NOT_HANDLED

If this is the first time you've seen this stop error screen,
restart your computer. If this screen appears again, follow
these steps:

Check to make sure any new hardware or software is properly installed.
If this is a new installation, ask your hardware or software manufacturer
for any windows updates you might need.

If problems continue, disable or remove any newly installed hardware
or software. Disable BIOS memory options such as aching or shadowing.
If you need to use safe Mode to remove or disable components, restart
your computer, press F8 to select Advanced Startup Options, and then
select Safe Mode.

Techical information:

*** STOP: 0x0000003d (0xFFFFF800054DCF90, 0x0000000000000000,0x0000000000000000,0
xFFFFF80003ED1490)


Collecting data for crash dump ...
Initializing disk for crash dump ...."""

        # 文字控件
        show_word = wx.StaticText(pnl, label=word_all, pos=(100, 100))

        # 颜色
        color_bg = (0, 0, 130)
        color_word = (242, 245, 255)
        pnl.SetBackgroundColour(color_bg)
        show_word.SetForegroundColour(color_word)

        # 字体
        font_word = wx.Font(pointSize=12, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='NSimSun')
        show_word.SetFont(font_word)

        # win7蓝屏这么丝滑的吗

        # 图标
        try:
            open('image/icon_BSOD.ico', 'rb')
        except FileNotFoundError:
            print("没有找到图标文件")
        else:
            self.icon = wx.Icon(name="image/icon_BSOD.ico", type=wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.icon)

        if run_state == 'show':
            pass
        elif run_state == 'shutdown':
            cmds.shutdown()
        elif run_state == 'record':
            main(mo, da, ho, mi)


class blue_screen_win10(wx.Frame):
    size = (screen_x + 18, screen_y + 43)

    def __init__(self, run_state='show', mo='0', da='0', ho='0', mi='0', parent=None, id=-1):
        # 初始化
        wx.Frame.__init__(self, parent, id, 'BSOD', pos=(-8, -35))
        wx.Frame.SetMinSize(self, size=self.size)
        wx.Frame.SetMaxSize(self, size=self.size)
        wx.Frame.SetSize(self, size=self.size)
        pnl = wx.Panel(self)

        # 文字控件
        word_face = wx.StaticText(pnl, label=run_read_ini[1], pos=(200, 100))
        word_contents_1 = wx.StaticText(pnl, label='你的设备遇到问题，需要关机。\n我们只收集某些错误信息，然后为你关闭电脑。', pos=(200, 320))
        word_contents_2 = wx.StaticText(pnl, label='90%完成', pos=(200, 510))
        img = wx.Image('image/QR.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()  # 假二维码
        wx.StaticBitmap(pnl, -1, img, (200, 605), (img.GetWidth(), img.GetHeight()))  # 假二维码
        # 获取显示在蓝屏的路径
        file_dir = __file__[0:-len(re.findall(r'\w+.[py|w]+$', __file__)[0]) - 1]
        word_more_1 = wx.StaticText(pnl, label=f'有关此问题的详细信息和可能的解决方法，请访问\n{file_dir}', pos=(520, 610))
        word_more_2 = wx.StaticText(pnl, label=f'如果致电支持人员，请向他们提供以下信息：\n终止代码：{run_read_word}\n失败的操作：play.exe',
                                    pos=(520, 750))

        # 字体
        font_face = wx.Font(pointSize=122, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='Microsoft YaHei')
        font_contents = wx.Font(pointSize=40, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                                faceName='Microsoft YaHei')
        font_more = wx.Font(pointSize=23, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='Microsoft YaHei')
        word_face.SetFont(font_face)
        word_contents_1.SetFont(font_contents)
        word_contents_2.SetFont(font_contents)
        word_more_1.SetFont(font_more)
        word_more_2.SetFont(font_more)

        # 颜色
        color_background = run_read_ini[0]
        color_contents = (255, 255, 255)
        pnl.SetBackgroundColour(color_background)
        word_face.SetForegroundColour(color_contents)
        word_contents_1.SetForegroundColour(color_contents)
        word_contents_2.SetForegroundColour(color_contents)
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

        if run_state == 'show':
            pass
        elif run_state == 'shutdown':
            cmds.shutdown()
        elif run_state == 'record':
            main(mo, da, ho, mi)


def run_blue(run_state, month='0', day='0', hour='0', minute='0'):
    # 假蓝屏窗口
    app_blue = wx.App()

    # 要调用哪个蓝屏
    if run_read_ini[2] == 'win98':
        frame_blue = blue_screen_win98(run_state, month, day, hour, minute, parent=None, id=-1)
    elif run_read_ini[2] == 'winxp':
        frame_blue = blue_screen_winxp(run_state, month, day, hour, minute, parent=None, id=-1)
    elif run_read_ini[2] == 'win7':
        frame_blue = blue_screen_win7(run_state, month, day, hour, minute, parent=None, id=-1)
    else:
        frame_blue = blue_screen_win10(run_state, month, day, hour, minute, parent=None, id=-1)

    frame_blue.Show()
    # 运行到这里就会进入窗口循环
    app_blue.MainLoop()


########################################################################################################################


def run_check():
    full_state = cmds.read_duration()
    if full_state is True:
        return full_state
    else:
        run_blue('shutdown')


def main(month='0', day='0', hour='0', minute='0'):
    # 运行
    cmds.GetReadSave_time('save')
    cmds.set_duration_time(month, day, hour, minute)
    run_check()


########################################################################################################################


class window(wx.Frame):
    size = (400, 400)
    title = f'专注学习助手{version}'

    def __init__(self, parent=None, id=-1):
        wx.Frame.__init__(self, None, id, self.title, size=self.size, pos=(560, 160))
        wx.Frame.SetMinSize(self, size=(350, 350))
        pnl = wx.Panel(self)

        # 控件
        title = wx.StaticText(pnl, label=self.title)
        bt_1h = wx.Button(pnl, label='关机1小时', size=(90, 50))
        bt_2h = wx.Button(pnl, label='关机2小时', size=(90, 50))
        bt_3h = wx.Button(pnl, label='关机3小时', size=(90, 50))
        bt_5m = wx.Button(pnl, label='关机5分钟', size=(90, 50))
        bt_10m = wx.Button(pnl, label='关机10分钟', size=(90, 50))
        bt_30m = wx.Button(pnl, label='关机半小时', size=(90, 50))
        ############
        tip_custom = wx.StaticText(pnl, label='自定义：')
        self.input_day = wx.TextCtrl(pnl, size=(40, 22), style=wx.TE_PROCESS_ENTER)
        tip_day = wx.StaticText(pnl, label='天')
        self.input_hour = wx.TextCtrl(pnl, size=(40, 22), style=wx.TE_PROCESS_ENTER)
        tip_hour = wx.StaticText(pnl, label='小时')
        self.input_minute = wx.TextCtrl(pnl, size=(40, 22), style=wx.TE_PROCESS_ENTER)
        tip_minute = wx.StaticText(pnl, label='分钟')
        bt_run_custom = wx.Button(pnl, label='确定', size=(50, 30))
        #############
        bt_shutdown = wx.Button(pnl, label='关机', size=(135, 40))
        bt_quit = wx.Button(pnl, label='退出', size=(135, 40))
        ######
        bt_ini = wx.Button(pnl, label='蓝屏配置', size=(88, 40))
        bt_about = wx.Button(pnl, label='软件说明', size=(88, 40))
        bt_log = wx.Button(pnl, label='更新日志', size=(88, 40))

        # 颜色
        contents_color = (224, 248, 249)
        contents_color_2 = (170, 204, 255)
        bt_1h.SetBackgroundColour(contents_color)
        bt_2h.SetBackgroundColour(contents_color)
        bt_3h.SetBackgroundColour(contents_color)
        bt_5m.SetBackgroundColour(contents_color)
        bt_10m.SetBackgroundColour(contents_color)
        bt_30m.SetBackgroundColour(contents_color)
        self.input_day.SetBackgroundColour(contents_color_2)
        self.input_hour.SetBackgroundColour(contents_color_2)
        self.input_minute.SetBackgroundColour(contents_color_2)

        # 事件
        bt_1h.Bind(wx.EVT_BUTTON, self.run_bt_1h)
        bt_2h.Bind(wx.EVT_BUTTON, self.run_bt_2h)
        bt_3h.Bind(wx.EVT_BUTTON, self.run_bt_3h)
        bt_5m.Bind(wx.EVT_BUTTON, self.run_bt_5m)
        bt_10m.Bind(wx.EVT_BUTTON, self.run_bt_10m)
        bt_30m.Bind(wx.EVT_BUTTON, self.run_bt_30m)
        self.input_day.Bind(wx.EVT_TEXT_ENTER, self.run_custom)
        self.input_hour.Bind(wx.EVT_TEXT_ENTER, self.run_custom)
        self.input_minute.Bind(wx.EVT_TEXT_ENTER, self.run_custom)
        bt_run_custom.Bind(wx.EVT_BUTTON, self.run_custom)
        bt_shutdown.Bind(wx.EVT_BUTTON, self.run_shutdown)
        bt_quit.Bind(wx.EVT_BUTTON, self.run_quit)
        bt_about.Bind(wx.EVT_BUTTON, self.run_about)
        bt_log.Bind(wx.EVT_BUTTON, self.run_log)
        bt_ini.Bind(wx.EVT_BUTTON, self.run_ini)

        sizer_h_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_1.Add(title, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_2.Add(bt_1h, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_2.Add(bt_2h, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_2.Add(bt_3h, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_3.Add(bt_5m, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_3.Add(bt_10m, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_3.Add(bt_30m, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_6.Add(tip_custom, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_6.Add(self.input_day, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_6.Add(tip_day, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_6.Add(self.input_hour, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_6.Add(tip_hour, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_6.Add(self.input_minute, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_6.Add(tip_minute, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_6.Add(bt_run_custom, proportion=0, flag=wx.ALIGN_CENTER)
        sizer_h_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_5.Add(bt_shutdown, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_5.Add(bt_quit, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_7.Add(bt_ini, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_7.Add(bt_about, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)
        sizer_h_7.Add(bt_log, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=3)

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(sizer_h_1, proportion=1, flag=wx.ALIGN_CENTER)
        sizer_v.Add(sizer_h_2, proportion=1, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        sizer_v.Add(sizer_h_3, proportion=1, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        sizer_v.Add(sizer_h_6, proportion=1, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        sizer_v.Add(sizer_h_5, proportion=1, flag=wx.ALIGN_CENTER)
        sizer_v.Add(sizer_h_7, proportion=1, flag=wx.ALIGN_CENTER)
        pnl.SetSizer(sizer_v)

        # 字体
        # 字体均来自：字加 https://zijia.foundertype.com/
        font_title = wx.Font(pointSize=22, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                             faceName='FZZJ-YGYTKJW')
        font_contents = wx.Font(pointSize=11, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                                faceName='FZZJ-YSBKJW')
        font_change = wx.Font(pointSize=9, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                              faceName='方正颜真卿楷书 简繁')
        font_quit = wx.Font(pointSize=18, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                            faceName='FZLiHeiS ExtraBold')
        font_about = wx.Font(pointSize=14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.LIGHT, underline=False,
                             faceName='方正启功行楷 简')
        title.SetFont(font_title)
        bt_1h.SetFont(font_contents)
        bt_2h.SetFont(font_contents)
        bt_3h.SetFont(font_contents)
        bt_5m.SetFont(font_contents)
        bt_10m.SetFont(font_contents)
        bt_30m.SetFont(font_contents)
        # ####################
        tip_custom.SetFont(font_change)
        self.input_day.SetFont(font_change)
        tip_day.SetFont(font_change)
        self.input_hour.SetFont(font_change)
        tip_hour.SetFont(font_change)
        self.input_minute.SetFont(font_change)
        tip_minute.SetFont(font_change)
        bt_run_custom.SetFont(font_change)
        # ####################
        bt_shutdown.SetFont(font_quit)
        bt_quit.SetFont(font_quit)
        bt_ini.SetFont(font_about)
        bt_about.SetFont(font_about)
        bt_log.SetFont(font_about)

        # 图标
        try:
            open('image/icon_helper.ico', 'rb')
        except FileNotFoundError:
            print("没有找到图标文件")
        else:
            self.icon = wx.Icon(name="image/icon_helper.ico", type=wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.icon)

    @staticmethod
    def run_bt_1h(event):
        run_blue('record', hour='1')

    @staticmethod
    def run_bt_2h(event):
        run_blue('record', hour='2')

    @staticmethod
    def run_bt_3h(event):
        run_blue('record', hour='3')

    @staticmethod
    def run_bt_5m(event):
        run_blue('record', minute='5')

    @staticmethod
    def run_bt_10m(event):
        run_blue('record', minute='10')

    @staticmethod
    def run_bt_30m(event):
        run_blue('record', minute='30')

    @staticmethod
    def run_shutdown(event):
        run_blue('shutdown')

    @staticmethod
    def run_quit(event):
        import sys
        sys.exit()

    @staticmethod
    def run_write(event):
        if os.path.exists('about.txt') is False:
            fo = open('about.txt', 'w+', encoding='utf-8')
            fo.close()
        file_dir = f'{os.getcwd()}\\about.txt'
        os.startfile(file_dir)
        print(f'文件位置：{file_dir}')

    @staticmethod
    def run_about(event):
        passage_str = """软件说明

原理：
记录设定时的时间和关机时长，开机自启，
用运行时的时间与上一次记录的时间作差，
用这个差与关机时长作比较，
时间差更大的话就说明到时间了，
否则关机，
关机命令是windows平台的 shutdown -s -t 0


写这个项目后一些想说的话:
快要期中考，怕自己复习不认真，
就临时写了这个项目（虽然没什么用hhh）
注释的话……后面慢慢补吧hhh，
毕竟，这也是临时写的项目，
很多地方都不规范，虽然能运行，但是可读性全无
多线程和窗口循环最为致命！！！    # v1.6更新
Python的逻辑真的不适合写大项目   # v1.6更新
项目结构太杂乱了               #v1.6.4更新

字体均来自：字加 https://zijia.foundertype.com/



2021.11.28 18:19
由于各种原因，
我感觉这个项目已经没有写下去的意义了，
现在就停了吧。
最后一个版本是v1.6.7
以后也不会再有功能更新了吧
再见

Github地址：https://www.github.com/XieJianCheng/DedicatedStudyHelper/
"""
        wx.MessageBox(passage_str, '关于这个软件', wx.YES_DEFAULT)

    @staticmethod
    def run_log(event):
        passage_str = f"""更新日志

当前版本：{version}

v1.2.1：
1. 换了一种时间计算方式，避免时间是负数的情况
2. 加了打开文件、关机、退出按钮
3. 修bug

v1.3.0：
把打开文件换成更直观的文本交互，纯粹是嫌麻烦

v1.4.0：
调用了之前写的字符串加密项目，
使软件无解

v1.5.0：
把时间记录也加密了，
同时把反触发也加进关机条件里，
只要报错了就关机，
做到了真正的无解（至少我自己想不出解法）

v1.6.0:
关机之前会显示蓝屏，玩一玩hhh

v1.6.1:
时间没到也可以显示蓝屏

v1.6.3:
可以自定义蓝屏颜色和标题文字

v1.6.5:
新增win7蓝屏，但就是感觉没内味

v1.6.6:
又加了xp和win98的蓝屏

v1.6.7:
可以直接修改蓝屏配置，
这应该是最后一个版本了吧，以后也不太可能会有功能更新了，版本号也不会高过v1.6了

v1.6.10:
在写关机的时候，顺便优化了win10蓝屏，显示的路径改为真实路径，
另外说一句，这个项目从进入v1.6.x和其他原因干扰开始，一直在变味"""

        wx.MessageBox(passage_str, '软件更新日志')

    def run_custom(self, event):
        got_day = self.input_day.GetValue()
        got_hour = self.input_hour.GetValue()
        got_minute = self.input_minute.GetValue()

        send_month = ''
        send_day = ''
        send_hour = ''
        send_minute = ''

        send_month = '0'
        if got_day == '':
            send_day = '0'
        else:
            send_day = got_day
        if got_hour == '':
            send_hour = '0'
        else:
            send_hour = got_hour
        if got_minute == '':
            send_minute = '0'
        else:
            send_minute = got_minute

        run_blue('record', send_month, send_day, send_hour, send_minute)

    @staticmethod
    def run_ini(event):
        os.startfile('BSOD.ini')


if __name__ == '__main__':
    try:
        if run_check() is True:
            app_main = wx.App()
            frame_main = window(parent=None, id=-1)
            frame_main.Show()
            app_main.MainLoop()
    except TypeError:
        run_blue('shutdown')

# 下一个项目绝对不会不写注释了 hhh

# v1.0.0结束时间 2021.11.9 20:23
# v1.2.0结束时间 2021.11.10 13:40
# v1.3.0结束时间 2021.11.17 13:05
# v1.4.0结束时间 2021.11.19 22:54
# v1.6.3结束时间 2021.11.24 19:51
# v1.6.7结束时间 2021.11.28 18:19


# 空两行是我对这条注释的尊重，再空两行是我对项目的不舍
# 最终结束时间 2021.11.28 18:26
