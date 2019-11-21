#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal

import settings


def task_loop(name, callback):
    from time import sleep
    n = 0

    while True:
        print('Run %d time(s) task->%s.' % (n, name))
        n += 1

        # 如果运行回调函数并返回True，则退出循环
        if callback():
            print('任务回调函数返回True，退出......')
            exit(0)

        sleep(2)


def foo(*args):
    def foo_callback():
        return settings.signals[signal.SIGINT] or settings.signals[signal.SIGTERM]

    print('args=%s' % str(args))
    task_loop('foo', foo_callback)


def bar(*args):
    def bar_callback():
        return settings.signals[signal.SIGINT] or settings.signals[signal.SIGTERM]

    print('args=%s' % str(args))
    task_loop('bar', bar_callback)
