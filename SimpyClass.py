# coding=utf-8
# /usr/bin/Python3.6

"""
Author: Xingwei Chen
Email:cxw19@mails.tsinghua.edu.cn
date:2021/12/11 15:31
"""
import logging
import math
import random
import time

import simpy
from functools import partial, wraps


def generator():
    idx = 0
    while True:
        yield math.sin(idx)
        idx += math.pi / 2


def run_generator(n=10):
    g = generator()
    for i in range(n):
        print(f'{next(g):.1f}')


def environment():  # read
    """
    no more events, until a certain time, until a certain event
    :return:
    """
    env = simpy.Environment()
    env.schedule(simpy.Event(env), 0)
    next_event_time = env.peek()
    env.step()


def event(env: simpy.Environment):  # read
    """
    An event
    - may happen (:attr:`triggered` is ``False``),
    - is going to happen (:attr:`triggered` is ``True``) or
    - has happened (:attr:`processed` is ``True``).
    """
    event_ = simpy.Event(env)
    env.timeout(delay=10, value=None)  # let time pass by


def process(env: simpy.Environment):
    """
    process created, it weill schedules
    :param env:
    :return:
    """
    generator_ = env.process(generator())
    generator_.callbacks.append([])


def interrupt(env: simpy.Environment):  # read
    generator_ = env.process(generator())
    generator_.interrupt()


def learn(env: simpy.Environment):
    while True:
        print(f"{env.now:.2f}, I start learning.")
        yield env.timeout(random.uniform(30, 60))
        print(f"{env.now:.2f}, 📱")
        yield env.timeout(random.uniform(30, 60))


def run_learn():
    env = simpy.Environment()
    env.process(learn(env))
    env.run(300)


def serve(env: simpy.Environment, client_id, server_: simpy.Resource):
    print(f"{env.now:>2.2f}, {client_id} arrived.")
    with server_.request() as server_req:
        yield server_req
        print(f'{env.now:2.2f}, {client_id} caught server.')
        yield env.timeout(random.uniform(10, 20))
        print(f'{env.now:2.2f}, {client_id} completed.')


def run_server():
    env = simpy.Environment()
    server_ = simpy.Resource(env, capacity=2)
    for i in range(4):
        env.process(serve(env, f'client-{i + 1}', server_))
    env.run()


def wait_multi_events():
    """
    典型场景: 仓库中的两个机器人要同时到达某个位置，或者人机协同时需要两者全部(&)完成
    """
    env = simpy.Environment()
    p, robot = env.timeout(10, value='People'), env.timeout(20, value='robot')
    result = yield p | robot
    assert result == {p: 'People'}

    p, robot = env.timeout(10, value='People'), env.timeout(20, value='robot')
    result = yield p & robot
    assert result == {p: 'People', robot: 'robot'}


def patch_resource(resource, pre=None, post=None):
    """
    Patch * resource * so that it calls the callable
    * pre * before each ... put/get/request/release operation
    and the callable * post * after each ... operation.
    The only argument to these functions is the resource ... instance.
    :param resource:
    :param pre:
    :param post:
    :return:
    """

    def get_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if pre:
                pre(resource)
            result = func(*args, **kwargs)
            if post:
                post(resource)
            return result

        return wrapper

    for name in ['put', 'get', 'request', 'release']:
        if hasattr(resource, name):
            setattr(resource, name, get_wrapper(getattr(resource, name)))


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        local_time = time.time()
        res = func(*args, **kwargs)
        logging.log(30, f"{func.__name__}, {time.time() - local_time:.5f}s")
        return res

    return wrapper


if __name__ == '__main__':
    # run_generator()
    # run_learn()
    run_server()
    import heapq
    heapq.heapify()
