#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
from sppm import settings
from sppm.settings import hlog


def sigint_handler(sig, frame):
    settings.signals[signal.SIGINT] = True
    hlog.debug('收到 Ctrl+C 信号，准备退出......')


def sigint_handler_exit(sig, frame):
    hlog.debug('收到 Ctrl+C 信号，退出......')
    exit(0)


def sigterm_handler(sig, frame):
    settings.signals[signal.SIGTERM] = True
    hlog.debug('收到 SIGTERM 信号，准备退出......')
