#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal

from sppm import settings
from sppm.process_status_lock import ProcessStatusLock
from sppm.settings import hlog, SPPM_CONFIG


def sigint_handler(sig, frame):
    settings.signals[signal.SIGINT] = True
    ProcessStatusLock.should_kill(SPPM_CONFIG.lock_file)
    hlog.debug('Ctrl+C，准备优雅地退出......')


def sigterm_handler(sig, frame):
    settings.signals[signal.SIGTERM] = True
    hlog.debug('触发 SIGTERM 信号，准备优雅地退出......')


def sighup_handler(sig, frame):
    settings.signals[signal.SIGHUP] = True
    hlog.debug('触发 SIGHUP 信号，准备优雅地退出......')
