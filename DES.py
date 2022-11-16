'''
File Name: DES.py

Program IDE: PyCharm

Create File Time:2022/11/15 21:08

Author: xiaolongtuan-yuan
/
'''
import base64

import config
import re

subKey = []


# 初始置换
def ip_change(bin_str):
    res = ""
    for i in config.IP_table:
        res += bin_str[i - 1]  # 数组下标i
    return (res[:32], res[32:])


# 逆置换
def ip_re_change(L16, R16):
    s = L16 + R16
    res = ""
    for i in config.IP_re_table:
        res += s[i - 1]
    return res


def XOR(s1, s2):
    if len(s1) != len(s2):
        print("程序异常！1")
        return
    res = ""
    for i in range(len(s1)):
        res += str(int(s1[i], 2) ^ int(s2[i], 2))
    return res


def E_extend(s):
    res = ""
    for i in config.e_table:
        res += s[i - 1]
    return res


def S_compress(s):
    res = ""
    for j in range(8):
        i = j * 6
        row = int(s[i] + s[i + 5], 2)
        col = int(s[i + 1:i + 5], 2)
        num = bin(config.S_BOX[j][row][col])[2:]
        for k in range(4 - len(num)):
            num = '0' + num
        res += num
    return res


def p_change(bin_str):
    res = ""
    for i in config.p_table:
        res += bin_str[i - 1]  # 数组下标i-1
    return res


def f_function(s, k):
    s1 = E_extend(s)
    s2 = XOR(s1, k)
    s3 = S_compress(s2)
    s4 = p_change(s3)
    return s4


def iteration(L0, R0):
    for i in range(15):
        R = R0
        R0 = XOR(L0, f_function(R0, subKey[i]))
        L0 = R
    L16 = XOR(L0, f_function(R0, subKey[15]))
    R16 = R0
    return (L16, R16)


def cp1_change(k):
    res = ""
    for i in config.pc1_table:
        res += k[i - 1]
    return (res[:28], res[28:])


def cp2_change(c, d):
    k = c + d
    res = ""
    for i in config.pc2_table:
        res += k[i - 1]
    return res


def left_turn(k, i):
    res = k[i:]
    res += k[0:i]
    return res


def generate_subKey(key):
    c0, d0 = cp1_change(key)
    for i in config.KEY_MOVE:
        c0 = left_turn(c0, i)
        d0 = left_turn(d0, i)
        subKey.append(cp2_change(c0, d0))
    return


def DES(STR):
    L0, R0 = ip_change(STR)
    L16, R16 = iteration(L0, R0)
    res = ip_re_change(L16, R16)
    return res


def str2bin(message):
    res = ""
    for i in message:
        tmp = bin(ord(i))[2:]
        for j in range(0, 8 - len(tmp)):
            tmp = '0' + tmp  # 把输出的b给去掉
        res += tmp
    return res


# 二进制转化为字符串
def bin2str(bin_str):
    res = ""
    tmp = re.findall(r'.{8}', bin_str)
    for i in tmp:
        res += chr(int(i, 2))
    # return str(base64.b64encode(res.encode()), 'utf-8')
    return res

# 补充为64位整除
def deal_mess(bin_mess):
    """
    :param bin_mess: 二进制的信息流
    :return: 补充的64位信息流
    """
    ans = len(bin_mess)
    if ans % 64 != 0:
        for i in range(64 - (ans % 64)):  # 不够64位补充0
            bin_mess += '0'
    return bin_mess


# 查看秘钥是否为64位
def input_key_judge(bin_key):
    """
    全部秘钥以补0的方式实现长度不满足64位的
    :param bin_key:
    """
    ans = len(bin_key)
    if len(bin_key) < 64:
        if ans % 64 != 0:
            for i in range(64 - (ans % 64)):  # 不够64位补充0
                bin_key += '0'
    # else:
    #     bin_key = bin_key[0:64]    #秘钥超过64位的情况默认就是应该跟密文一样长 直接将密钥变为跟明文一样的长度，虽然安全性会有所下降
    return bin_key


def all_message_encrypt(message, key):
    bin_mess = deal_mess(str2bin(message))
    res = ""
    bin_key = input_key_judge(str2bin(key))
    generate_subKey(bin_key)
    tmp = re.findall(r'.{64}', bin_mess)
    for i in tmp:
        res += DES(i)
    res = bin2str(res)
    print("结果"+ res)
    return res

def all_message_decrypt(message, key):
    bin_mess = deal_mess(str2bin(message))
    res = ""
    bin_key = input_key_judge(str2bin(key))
    generate_subKey(bin_key)

    subKey.reverse()
    tmp = re.findall(r'.{64}', bin_mess)
    for i in tmp:
        res += DES(i)
    res = bin2str(res)
    print("结果： " + res)
    return res


def mes_encrypt():
    print("请输入明文：")
    mes = input()
    # mes = str(base64.b64decode(mes).decode(), 'utf-8')
    print("请输入秘钥：")
    key = input()
    s = all_message_encrypt(mes, key)

def mes_decrypt():
    print("请输入密文：")
    mes = input()
    # mes = str(base64.b64decode(mes).decode(), 'utf-8')
    print("请输入密钥：")
    key = input()
    s = all_message_decrypt(mes, key)



if __name__ == "__main__":
    while True:
        subKey = []
        method = input("1、加密 2、解密 3、退出:  ")
        if method == "1":
            mes_encrypt()
        elif method == "2":
            mes_decrypt()
        else:
            break


