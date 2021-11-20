# coding:utf-8

# 这个模块是从我之前写的项目里来的，现在做下优化
# 模块全拼EncryptionAndDecryption，在原来的项目叫CAD_CEI(CompilationAndDecoding)

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
