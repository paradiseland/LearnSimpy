# coding=utf-8
# /usr/bin/Python3.6

"""
Author: Xingwei Chen
Email:cxw19@mails.tsinghua.edu.cn
date:2021/12/11 15:43
"""
import simpy

from AVSRS.Config import v_lift, v_agv, WIDTH_OF_AISLE, WIDTH_OF_BAY


class AGV:
    def __init__(self, idx, tier, **kwargs):
        self.index = idx
        self.name = f"AGV-{idx}"
        self.place = (0, 0, 0)
        self.tier = tier

    def travel_cross_aisle(self, aisle):
        return abs(self.place[1] - aisle) * WIDTH_OF_AISLE / v_agv

    def travel_along_aisle(self, bay):
        return abs(self.place[2] - bay) * WIDTH_OF_BAY / v_agv


class AGVFleet(simpy.FilterStore):
    """

    """

    def __init__(self, env: simpy.Environment, num_of_agv):
        super().__init__(env)
        self.items = [AGV(idx=i + 1, tier=i) for i in range(num_of_agv)]


class Lift(simpy.Resource):
    def __init__(self, env: simpy.Environment, **kwargs):
        super().__init__(env)
        self.tier: int = 0

    def travel_to_tier_x(self, x):
        return abs(x - self.tier) / v_lift
