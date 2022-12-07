'''
File Name: myRSA.py

Program IDE: PyCharm

Create File Time:2022/12/7 14:22

Author: xiaolongtuan-yuan
/
'''
# -*- coding: utf-8 -*-

import random


def get_message():
    s = input("输入你的信息： ")
    return s
def get_sec():
    n = input("请输入安全质数：")
    return n

def get_key():
    D = input("请输入D: ")
    N = input("请输入N: ")
    if D == '' or N == '':
        key = "不要输入空的值"
    return (D, N)
def get_key2():
    E = input("请输入E: ")
    N = input("请输入N: ")
    if E == '' or N == '':
        key = "不要输入空的值"
    return (E, N)


# 辗转相除法求最大公因数
def gcd(a, b):
    if a < b: a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a


# 生成n, e, d
def generate_key(key_len):  # key_len要比消息长度大
    p = random_prime(key_len // 2)
    q = random_prime(key_len // 2)
    n = p * q
    ph_n = (p - 1) * (q - 1)
    print("ph_n:" + str(ph_n))
    e = 65537  # e取固定值
    d = generate_d(ph_n, e)
    return (n, e, d)


# 开始选择p q
def random_prime(half_len):
    while True:
        n = random.randint(0, 1 << half_len)  # 求2^half_len之间的大数
        if n % 2 != 0:
            found = True
            # 随机性测试
            for i in range(0, 5):  # 5的时候错误率已经小于千分之一
                if prime_test(n) == False:
                    found = False
                    break
            if found == True:
                return n


# Miller-Rabin
def prime_test(n):
    q = n - 1
    k = 0
    # 寻找k,q 是否满足2^k*q =n - 1
    while q % 2 == 0:
        k += 1
        q = q // 2
    a = random.randint(2, n - 2)
    # 如果 a^q mod n= 1, n 可能是一个素数
    if fast_mod(a, q, n) == 1:
        return True
    # 如果存在j满足 a ^ ((2 ^ j) * q) mod n == n-1, n 可能是一个素数
    for j in range(0, k):
        if fast_mod(a, (2 ** j) * q, n) == n - 1:
            return True
    # n 不是素数
    return False


def ext_gcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, q = ext_gcd(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, q


# 产生秘钥d
def generate_d(ph_n, e):
    (x, y, r) = ext_gcd(ph_n, e)
    if y < 0:
        return y + ph_n  # 同y % ph_n
    return y


def fast_mod(mes, E, N):
    ret = 1
    tmp = mes
    while E:
        if E & 0x1:
            ret = ret * tmp % N
        tmp = tmp * tmp % N
        E >>= 1
    return ret


if __name__ == '__main__':
    while True:
        mode = input("0、钥匙对生成 1、加密 2、解密 3、退出: ")
        if mode == '0':
            security = int(get_sec())
            (n, e, d) = generate_key(security)
            print("秘钥对为 N：{} E:{} D:{}".format(n, e, d))
        elif mode == '1':  # 加密解密虽同源，但是由于不能直接用 =='1' or '2'，所以还是得分开写
            password = int(get_message())
            E, N = get_key2()
            E, N = int(E), int(N)
            res = fast_mod(password, E, N)
            print("密文：", res)
        elif mode == '2':  # 由于异或运算的对合性，RC4加密解密使用同一套算法。
            password = int(get_message())
            D, N = get_key()
            D, N = int(D), int(N)
            res = fast_mod(password, D, N)
            print("解密结果：", res)
        else:
            print("操作结束！ ")
            break
