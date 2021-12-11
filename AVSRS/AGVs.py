# coding=utf-8
# /usr/bin/Python3.6

"""
Author: Xingwei Chen
Email:cxw19@mails.tsinghua.edu.cn
date:2021/12/11 15:43
"""
import simpy

class AGV():
    def __init__(self, idx, **kwargs):
        self.index =  idx
        self.name = f"AGV-{idx}"
        self.place = ()

class AGVFleet(simpy.FilterStore):
    """

    """
    def __init__(self, env: simpy.Environment):
        super().__init__(env)
        self.items =
