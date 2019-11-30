#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sppm
from time import sleep


def foo():
    """
    需要启动子进程的函数
    子进程任务foo，该任务中有阻塞执行的情况，需要利用文件锁通信，否则触发终止信号后需要等阻塞完之后才能退出
    """
    exit_args = "foo"
    n = 0
    while True:
        # 如果运行回调函数并返回True，则退出循环
        if sppm.signal_monitor(exit_callback, *exit_args):
            print('任务回调函数返回True，退出......')
            break

        # 需要阻塞等待前上锁
        sppm.working_lock()

        print('Run %d time(s) task->%s.' % (n, "foo"))
        n += 1

        # 模拟任务执行需要十秒
        sleep(10)


def exit_callback(*args):
    """
    推出进程时的回调，用于提供给sppm.signal_monitor，不提供则默认不作处理直接关闭子进程
    """
    print("执行exit_callback函数")


if __name__ == "__main__":
    sppm.sppm_start(foo)
