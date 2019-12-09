#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal

from sppm.settings import hlog, signals, SPPM_CONFIG


def cleanup():
    """
    退出程序时，删除PID文件以及lock文件
    :return:
    """
    try:
        if os.path.exists(SPPM_CONFIG.child_pid_file):
            os.remove(SPPM_CONFIG.child_pid_file)

        if os.path.exists(SPPM_CONFIG.lock_file):
            os.remove(SPPM_CONFIG.lock_file)

        if os.path.exists(SPPM_CONFIG.pid_file):
            os.remove(SPPM_CONFIG.pid_file)
    except IOError:
        pass


def signal_monitor(exit_callback=None, *args):
    hlog.debug('signal_monitor......')

    if signals[signal.SIGTERM]:
        hlog.debug('收到终止信号，准备退出......')

        if exit_callback:
            exit_callback(*args)

        return True
    return False


def to_uptime_format(seconds):
    """
    将秒转换为友好的天、时、分、秒
    :param seconds:
    :return:
    """
    one_minute_seconds = 60
    one_hour_seconds = 60 * 60
    one_day_seconds = 24 * 60 * 60

    days = seconds // one_day_seconds
    left_seconds = seconds % one_day_seconds

    hours = left_seconds // one_hour_seconds
    left_seconds = left_seconds % one_hour_seconds

    minutes = left_seconds // one_minute_seconds
    _seconds = left_seconds % one_minute_seconds

    result = ''

    if days:
        result += '%d day(s), ' % days

    if hours:
        result += '%d hour(s), ' % hours

    if minutes:
        result += '%d minute(s), ' % minutes

    result += '%d second(s)' % _seconds

    return result
