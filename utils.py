#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import signal

from settings import PPMS_PID_FILE
from settings import PPMS_CHILD_PID_FILE
from settings import PPMS_LOCK_FILE
from settings import signals
from settings import hlog


def cleanup():
    """
    退出程序时，删除PID文件以及lock文件
    :return:
    """
    try:
        if os.path.exists(PPMS_CHILD_PID_FILE):
            os.remove(PPMS_CHILD_PID_FILE)

        if os.path.exists(PPMS_LOCK_FILE):
            os.remove(PPMS_LOCK_FILE)

        if os.path.exists(PPMS_PID_FILE):
            os.remove(PPMS_PID_FILE)
    except IOError:
        pass


def signal_monitor(exit_callback, *args):
    hlog.debug('signal_monitor......')

    if signals[signal.SIGINT] or signals[signal.SIGTERM]:
        hlog.debug('收到终止信号，准备退出......')

        if exit_callback:
            exit_callback(*args)
