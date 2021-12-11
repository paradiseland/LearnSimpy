# coding=utf-8
# /usr/bin/Python3.6

"""
Author: Xingwei Chen
Email:cxw19@mails.tsinghua.edu.cn
date:2021/12/11 15:21
"""
import logging
import simpy
import numpy as np


class AVSRSEnv(simpy.Environment):
    """

    """

    def __init__(self):
        super().__init__()
