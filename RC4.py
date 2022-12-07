'''
File Name: RC4.py

Program IDE: PyCharm

Create File Time:2022/12/7 12:12

Author: xiaolongtuan-yuan
/
'''

# -*- coding: utf-8 -*-
import base64


def get_message():
    print("输入你的信息： ")
    s = input()
    return s


def get_key():
    print("输入你的密钥： ")
    key = input()
    if key == '':
        key = "不要输入空的 key 值"
    return key


def init_box(key):
    # PRGA生成秘钥流
    s_box = list(range(256))  # 初始化S盒
    j = 0
    for i in range(256):
        j = (j + s_box[i] + ord(key[i % len(key)])) % 256  # i % len(key)用于当key长度小于256时使用最前面的T个字符补全
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box


def func(plain, box):
    # 将秘钥流与文字节异或运算
    res = []
    i = j = 0
    for s in plain:
        i = (i + 1) % 256
        j = (j + box[i]) % 256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j]) % 256
        k = box[t]
        res.append(chr(ord(s) ^ k))

    cipher = "".join(res)
    return cipher


def encrypt(plain, box):
    cipher = func(plain, box)

    # base64的目的也是为了变成可见字符
    print("base64后的编码")
    print(str(base64.b64encode(cipher.encode('utf-8')), 'utf-8'))


def decrypt(plain, box):
    plain = base64.b64decode(plain)
    plain = bytes.decode(plain)  # 因为返回的是解码过的  bytes，所以需要再用 decode 解码成字符串。

    cipher = func(plain, box)

    print("解密后的密文")
    print(cipher)


if __name__ == '__main__':
    while True:
        mode = input("1、加密 2、解密 3、退出: ")

        if mode == '1':  # 加密解密虽同源，但是由于不能直接用 =='1' or '2'，所以还是得分开写
            message = get_message()
            key = get_key()
            box = init_box(key)
            encrypt(message, box)
        elif mode == '2':  # 由于异或运算的对合性，RC4加密解密使用同一套算法。
            message = get_message()
            key = get_key()
            box = init_box(key)
            decrypt(message, box)
        else:
            print("操作结束！ ")
            break

'''
RC4算法的原理是“搅乱”，它包括初始化算法和伪随机子密码生成算法两大部分，在初始化的过程中， 
密钥的主要功能是将一个256字节的初始数簇进行随机搅乱，不同的数簇在经过伪随机子密码生成算
法的处理后可以得到不同的子密钥序列，将得到的子密钥序列和明文进行异或运算（XOR）后，得到密文。

由于RC4算法加密采用的是异或方式，所以，一旦子 密钥序列出现了重复，密文就有可能被破解，
但是目前还没有发现密钥长度达到128位的RC4有重复的可能性，所以，RC4也是目前最安全的加密算法之一。
'''