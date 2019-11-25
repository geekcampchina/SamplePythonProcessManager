#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
import settings
from common import hlog
from process_status_lock import ProcessStatusLock


def sigint_handler(sig, frame):
    settings.signals[signal.SIGINT] = True
    ProcessStatusLock.should_kill(settings.PPMS_LOCK_FILE)
    hlog.debug('Ctrl+C，准备优雅地退出......')


def sigterm_handler(sig, frame):
    settings.signals[signal.SIGTERM] = True
    hlog.debug('触发 SIGTERM 信号，准备优雅地退出......')


def sighup_handler(sig, frame):
    settings.signals[signal.SIGHUP] = True
    hlog.debug('触发 SIGHUP 信号，准备优雅地退出......')
