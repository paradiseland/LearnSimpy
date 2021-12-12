# coding=utf-8
# /usr/bin/Python3.6

"""
Author: Xingwei Chen
Email:cxw19@mails.tsinghua.edu.cn
date:2021/12/10 23:47
"""
import random
import logging
from typing import List

import simpy
from simpy import Environment

LOG_LEVEL = 5
SIM_TIME = 3600
ARRIVAL_RATE = 100 / 3600
SERVICE_RATE = 80 / 3600
random.seed(42)  # ensure the same result


class MM1(Environment):

    def __init__(self):
        super().__init__()
        self.server = simpy.Resource(self, capacity=1)
        self.index, self.served = 1, 0
        self.process(self.clients())
        self.process(self.observe())
        self.queue_record = [0, 0]  # record[0]: serve times, record[1]: sum of all queues
        self.waiting_time: List[float] = []  # 1/(mu-lambda)
        self.serve_time: List[float] = []
        self.total_time: List[float] = []

    def clients(self):
        while True:
            time_interval = random.expovariate(ARRIVAL_RATE)
            yield self.timeout(time_interval)
            logging.log(10, f"{self.now:.2f}, client-{self.index} arrived")
            self.process(self.serve(self.index))
            self.index += 1

    def observe(self):
        while True:
            self.queue_record[0] += 1
            self.queue_record[1] += len(self.server.put_queue)
            yield self.timeout(10)

    def serve(self, client_id):
        arrive_time = self.now
        with self.server.request() as server_req:
            yield server_req
            waiting_time = self.now - arrive_time
            self.waiting_time.append(waiting_time)
            logging.log(10, f"{self.now:.2f}, client-{client_id} starts served.")
            serve_time = random.expovariate(SERVICE_RATE)
            self.serve_time.append(serve_time)
            yield self.timeout(serve_time)
        self.total_time.append(self.now - arrive_time)
        logging.log(10, f"{self.now:.2f}, client-{client_id} has left, serve_time:{serve_time:.2f}, waiting time:{waiting_time:.2f}.")
        self.served = client_id

    def output(self):
        logging.log(50, f"{'-' * 30}\nTotal Simulation time: {SIM_TIME} s\n"
                        f"Arrive: {self.index}\n"
                        f"Served: {self.served}\n"
                        f"Mean Queue Length:{self.queue_record[1] / self.queue_record[0]:.2f}\n"
                        f"Mean Waiting Time:{sum(self.waiting_time) / len(self.waiting_time):.2f} s\n"
                        f"Mean Service Time:{sum(self.serve_time) / len(self.serve_time):.2f} s\n"
                        f"Mean Total Time:{sum(self.total_time) / len(self.total_time):.2f} s")
        logging.log(50,
                    f"Verify Little's law: L({self.queue_record[1] / self.queue_record[0]:.2f})=λW({ARRIVAL_RATE:.2f} *{sum(self.waiting_time) / len(self.waiting_time):.2f})[{ARRIVAL_RATE * sum(self.waiting_time) / len(self.waiting_time):.2f}]")


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL, format='')
    mm1 = MM1()
    mm1.run(until=SIM_TIME)
    mm1.output()
