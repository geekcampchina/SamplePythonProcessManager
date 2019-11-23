#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import settings
import table_driven
from settings import hlog
from time import sleep


def get_pid_from_file(pid_file):
    """
    从文件读取PID
    :return:
    """
    with open(pid_file, 'r') as f:
        return int(f.readline())


def make_child_pid_filename(task_type):
    """
    生成子进程PID文件名
    :param task_type: 任务类型
    :return:
    """
    return 'ppms_{0}.pid'.format(table_driven.TASK_TYPE_NAMES[task_type])


def make_child_locak_filename(task_type):
    """
    生成子进程lock文件名
    :param task_type: 任务类型
    :return:
    """
    return 'ppms_{0}.lock'.format(table_driven.TASK_TYPE_NAMES[task_type])


def lock_child(task_type, child_pid):
    """
    子进程运行时，创建文件锁
    :param task_type: 任务类型
    :param child_pid: 子进程PID
    :return:
    """
    child_lock_file = make_child_locak_filename(task_type)

    with open(child_lock_file, 'w') as f:
        f.write(child_pid)


def wait_unlock(task_type):
    """
    等待子进程释放文件锁
    :param task_type: 任务类型
    :return:
    """
    child_lock_file = make_child_locak_filename(task_type)

    while True:
        hlog.debug('等待释放文件锁：%s' % child_lock_file)

        if not os.path.exists(child_lock_file):
            hlog.debug('文件锁：%s 已经释放' % child_lock_file)
            break

        sleep(1)


def cleanup():
    """
    退出程序时，删除PID文件以及lock文件
    :return:
    """
    try:
        for task_type in table_driven.TASK_TYPE_NAMES.keys():
            child_pid_file = make_child_pid_filename(task_type)
            child_lock_file = make_child_locak_filename(task_type)

            if os.path.exists(child_pid_file):
                os.remove(child_pid_file)

            if os.path.exists(child_lock_file):
                os.remove(child_lock_file)

        if os.path.exists(settings.PPMS_PID_FILE):
            os.remove(settings.PPMS_PID_FILE)
    except IOError:
        pass
