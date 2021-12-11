# coding=utf-8
# /usr/bin/Python3.6

"""
Author: Xingwei Chen
Email:cxw19@mails.tsinghua.edu.cn
date:2021/12/11 15:21
"""
import logging
import random

import simpy
import numpy as np

from AVSRS.AGVs import AGVFleet, Lift, AGV
from AVSRS.Config import *


class AVSRSEnv(simpy.Environment):
    """

    """

    def __init__(self):
        super().__init__()
        self.AGVs = AGVFleet(self, num_of_agv=NUM_OF_TIERS)
        self.lift = Lift(self)
        self.inbound_idx = self.outbound_idx = 0
        self.initialize()

    def initialize(self):
        self.process(self.source_inbound())
        self.process(self.source_outbound())

    def source_inbound(self):
        while True:
            self.inbound_idx += 1
            time_interval_of_inbound_order_arrive = random.expovariate(ARRIVAL_RATE)
            yield self.timeout(time_interval_of_inbound_order_arrive)
            self.process(self.store(self.inbound_idx, self.rand_place()))

    def source_outbound(self):
        while True:
            self.outbound_idx += 1
            time_interval_of_outbound_order_arrive = random.expovariate(ARRIVAL_RATE)
            yield self.timeout(time_interval_of_outbound_order_arrive)
            tier, aisle, bay = random.randint(1, NUM_OF_TIERS), random.randint(1, NUM_OF_AISLES), random.randint(1, NUM_OF_BAYS)
            self.process(self.retrieve(self.outbound_idx, self.rand_place()))

    def retrieve(self, order_idx, target):
        logging.log(10, f"{self.now:.2f}, outbound order[{order_idx}] arrived, {target}")
        tier, aisle, bay = target
        agv = yield self.AGVs.get(lambda agv_: agv_.place[0] == tier)
        time_to_aisle = agv.travel_cross_aisle(aisle)
        time_to_bay = agv.travel_along_aisle(bay)
        yield self.timeout(2 * (time_to_aisle + time_to_bay))
        self.AGVs.put(agv)
        if tier != 0:
            with self.lift.request() as lift_req:
                yield lift_req
                time_to_tier0 = self.lift.travel_to_tier_x(0)
                yield self.timeout(time_to_tier0)
        # request workstation

    def store(self, order_idx, target):
        order_name = f'inbound order[{order_idx}]'
        logging.log(10, f"{self.now:.2f}, {order_name} arrived, {target}")
        tier, aisle, bay = target
        if tier != 0:
            with self.lift.request() as lift_req:
                yield lift_req
                logging.log(10, f"{self.now:.2f}, {order_name} caught the lift")
                time_to_tier = self.lift.travel_to_tier_x(tier)
                yield self.timeout(time_to_tier)
                logging.log(10, f"{self.now:.2f}, lift with{order_name} arrived target tier")

        agv = yield self.AGVs.get(filter=lambda agv: agv.place[0] == tier)
        logging.log(10, f"{self.now:.2f}, {order_name} caught the agv")
        time_to_aisle = agv.travel_cross_aisle(aisle)
        time_to_bay = agv.travel_along_aisle(bay)
        yield self.timeout(2 * (time_to_aisle + time_to_bay))
        logging.log(10, f"{self.now:.2f}, agv completed the {order_name} task")
        self.AGVs.put(agv)

    @staticmethod
    def rand_place():
        tier, aisle, bay = random.randint(1, NUM_OF_TIERS), random.randint(1, NUM_OF_AISLES), random.randint(1, NUM_OF_BAYS)
        return tier, aisle, bay


if __name__ == '__main__':
    logging.basicConfig(level=log_level, format='')
    avsrs = AVSRSEnv()
    avsrs.run(until=SIMULATION_ELAPSE)
