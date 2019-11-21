#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import signal
import settings
from time import sleep


def task_loop(name, callback):
    from child_resource import hlog

    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    n = 0

    while True:
        hlog.info('Run %d time(s) task->%s.' % (n, name))
        n += 1

        # 如果运行回调函数并返回True，则退出循环
        if callback():
            hlog.info('任务回调函数返回True，退出......')
            break

        sleep(2)

    hlog.exit_func(func_name)


def foo(*args):
    from child_resource import hlog

    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    def foo_callback():
        return settings.signals[signal.SIGINT] or settings.signals[signal.SIGTERM]

    hlog.var('args', str(args))
    task_loop('foo', foo_callback)

    hlog.exit_func(func_name)


def bar(*args):
    from child_resource import hlog

    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    def bar_callback():
        return settings.signals[signal.SIGINT] or settings.signals[signal.SIGTERM]

    hlog.var('args', str(args))
    task_loop('bar', bar_callback)

    hlog.exit_func(func_name)
