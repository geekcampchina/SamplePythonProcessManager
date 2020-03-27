#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from time import sleep

logger = logging.getLogger()


def foo():
    """
    子进程任务foo，该任务中没有阻塞执行的情况，不需要利用文件锁通信
    """
    exit_args = "arg_foo"
    n = 0

    while True:
        logger.info('Run %d time(s) task->%s.' % (n, "foo"))
        n += 1

        # 如果运行回调函数并返回True，则退出循环
        if sppm.signal_monitor(exit_callback, *exit_args):
            logger.info('任务回调函数返回True，退出......')
            break
        # 模拟任务执行需要十秒
        sleep(10)


# noinspection PyUnusedLocal
def exit_callback(*args):
    """
    退出进程时的回调，用于提供给sppm.signal_monitor，不提供则默认不作处理直接关闭子进程
    """
    print("执行exit_callback函数")


if __name__ == "__main__":
    try:
        import sppm
    except ModuleNotFoundError:
        import sys
        from pathlib import Path

        # 解决直接从源代码（未安装sppm包）运行时，"import sppm" 无法导入问题
        sppm_root_src = str(Path(__file__).absolute().parent.parent)
        sys.path.insert(0, sppm_root_src)

        import sppm

    sppm.sppm_start(foo)
