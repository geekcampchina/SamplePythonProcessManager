#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import signal

from sppm import settings
from sppm.cmd_action import action_shutdown
from sppm.process_status_lock import ProcessStatusLock
from sppm.settings import hlog, SPPM_CONFIG


# noinspection PyUnusedLocal
def sigint_handler(sig, frame):
    hlog.debug('收到 Ctrl+C 信号，退出......')

    child_pid = ProcessStatusLock.get_pid_from_file(SPPM_CONFIG.child_pid_file)
    action_shutdown(child_pid)
    exit(0)


# noinspection PyUnusedLocal
def sigterm_handler(sig, frame):
    settings.signals[signal.SIGTERM] = True
    hlog.debug('收到 SIGTERM 信号，准备退出......')
