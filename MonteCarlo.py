# coding=utf-8
# /usr/bin/Python3.6

"""
Author: Xingwei Chen
Email:cxw19@mails.tsinghua.edu.cn
date:2021/12/10 23:54
"""
import random

import numpy as np


def pi(times=100000):
    """
    P = (pi*r^2)/S, S is the area of square, r is radius of circle
    We set the r=0.5, pi=4SP
    :param times:
    :return:
    """
    cnt = 0
    x = np.random.random(times) - 0.5
    y = np.random.random(times) - 0.5
    P = (x ** 2 + y ** 2 <= 1 / 4).mean()
    return 4 * P


def calculus_sin_x(n=100000):
    """
    ∫sin(x)dx = - cos(x)
    ∫sin(x)dx(0,pi) = cos(0)-cos(pi)=2
    :return:
    """
    x = np.linspace(0, np.pi, num=n)
    y = np.sin(x)
    return y.sum() * np.pi / n


if __name__ == '__main__':
    for i in range(1, 10):
        print(f"PI ≈ {pi(10 ** i):.10f}  [{10 ** i:>9,d}]")
    for i in range(1, 7):
        print(f"initiate sin x on (0, pi) ≈ {calculus_sin_x(10 ** i):.5f}  [{10 ** i:>9,d}]")
