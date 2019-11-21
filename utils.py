#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import settings


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
    return 'ppms_{0}.pid'.format(settings.TASK_TYPE_NAMES[task_type])


def cleanup():
    """
    退出程序时，删除PID文件
    :return:
    """
    try:
        for task_name in settings.TASK_TYPE_NAMES.keys():
            child_pid_file = make_child_pid_filename(task_name)

            if os.path.exists(child_pid_file):
                os.remove(child_pid_file)

        if os.path.exists(settings.PPMS_PID_FILE):
            os.remove(settings.PPMS_PID_FILE)
    except IOError as e:
        pass
