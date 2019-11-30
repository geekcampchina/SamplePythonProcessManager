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

    if signals[signal.SIGINT] or signals[signal.SIGTERM]:
        hlog.debug('收到终止信号，准备退出......')

        if exit_callback:
            exit_callback(*args)

        return True
    return False
