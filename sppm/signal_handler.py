#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal

from sppm import settings
from sppm.process_status_lock import ProcessStatusLock
from sppm.settings import hlog
from sppm.utils import gen_task_filename


def sigint_handler(sig, frame):
    settings.signals[signal.SIGINT] = True
    ProcessStatusLock.should_kill(gen_task_filename(settings.PPMS_LOCK_FILE))
    hlog.debug('Ctrl+C，准备优雅地退出......')


def sigterm_handler(sig, frame):
    settings.signals[signal.SIGTERM] = True
    hlog.debug('触发 SIGTERM 信号，准备优雅地退出......')


def sighup_handler(sig, frame):
    settings.signals[signal.SIGHUP] = True
    hlog.debug('触发 SIGHUP 信号，准备优雅地退出......')
