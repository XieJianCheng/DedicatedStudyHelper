# coding:utf-8

# 本工具用于对明码进行加密，以及对密码的解密

# 这是我第一个运用OOP(面向对象编程)的自主开发项目

# 开始时间2021.8.20 22：43
"""
print("\n本工具用于对明码进行加密，以及对密码的解密\n")

want_str = input("请输入要加密或者解密？\n")
conversion_str = input("请输入要转化的字符串：\n")


class Password:
    def __init__(self, need_str, string):
        self.need_str = need_str
        self.string = string

    def get_need(self):
        global need_bool
        if Password.__init__.need_str == "加密":
            need_bool = True
        elif Password.__init__.need_str == "解密":
            need_bool = False
        else:
            print("输入错误\n自动退出程序")
            quit()
        return need_bool

    @property
    def get_string(self):
        return self.string

    @staticmethod
    def compiling():
        word = Password.get_string
        password = []
        for i in word:
            password.append(ord(i))
        for j in str(password):
            password.append(ord(j))
        for k in str(password):
            password.append(ord(k))
        return password


if __name__ == "__main__":
    run_Password = Password(want_str, conversion_str)
    Password.get_need(None)
"""
# 致命错误：
# 忽略了OOP的本质，
# 根本没有运用到面向对象编程的思想，
# 而是直接把方法当成了函数


# 第二次开始时间2021.8.22 14:29
# 第二次编写目的：
# 练习函数运用
# 练习算法能力


import re


def password_character_set(change_type):
    """
    用于生成密码字符集
    """
    key_list = ['[', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ']', ',', ' ']
    value_list = ['#$', '%u', 'w{', '@e', '_v', 'z$', '(f', '&k', '{t', ',l', ']q', '$#', 'c?', 'n?']
    if change_type:
        passwords = dict(zip(key_list, value_list))
    else:
        passwords = dict(zip(value_list, key_list))
    return passwords


def get_need():
    """
    用于获取运行的方式，也就是加密或者解密
    """
    global need_bool
    while True:
        need_str = input("你想要加密(1)还是解密(2)？\n或者退出(3)？\n")
        if need_str == "加密" or need_str == '1':
            need_bool = True
            break
        elif need_str == "解密" or need_str == '2':
            need_bool = False
            break
        elif need_str == "退出" or need_str == '3':
            print("即将退出程序……")
            quit()
        else:
            print("\n输入错误！\n请继续输入\n\n")
            continue
    return need_bool


def get_string():
    primary_string = str(input("请输入原始字符串：\n"))
    return primary_string


def compiling(string, password_set):
    """
    用于对字符串进行加密
    """
    primary_word = string
    new_word = []
    for i in primary_word:
        new_word.append((ord(i) + 34) * 2)
    primary_password = str(new_word)
    password = ''
    for j in primary_password:
        password = password + password_set.get(j)
    return password


def decoding(password, password_set):
    """
    用于对字符串进行解密
    """

    primary_password_1 = password

    re_str_1 = r'[^"]'
    primary_password_2 = re.findall(re_str_1, primary_password_1)

    test_string = ''
    times = 0
    new_password = []
    for n in primary_password_2:
        times += 1
        test_string = test_string + n
        if times % 2 == 0:
            new_password.append(test_string[-2:])

    primary_word = ''
    for m in new_password:
        primary_word = primary_word + password_set.get(m)

    re_str_2 = r'\d+'
    match = re.findall(re_str_2, str(primary_word))
    new_string = ''
    for i in match:
        j = int(i)
        o = int((j / 2) - 34)
        k = chr(o)
        new_string = new_string + k
    return new_string


def main():
    run__get_need = get_need()
    run__get_string = get_string()
    if run__get_need:
        run = compiling(run__get_string, password_character_set(True))
    else:
        run = decoding(run__get_string, password_character_set(False))
    print("最后的结果为：")
    print(run)
    print('\n')


if __name__ == '__main__':
    print("\n本工具用于对字符串的加密和解密\n")
    while True:
        main()

# 第一次阶段性编写完成 2021.8.22 23：20
# 第二次阶段性编写完成 2021.8.24 22：10
# 2021.8.24 22:29 圆满完成

# 下一个目标：
# 将此工具GUI化
