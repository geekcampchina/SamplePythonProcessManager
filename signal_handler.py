#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
import settings
from utils import cleanup


def sigint_handler(sig, frame):
    settings.signals[signal.SIGINT] = True
    print('Ctrl+C，准备优雅地退出......')


def sigterm_handler(sig, frame):
    settings.signals[signal.SIGTERM] = True
    print('触发 SIGTERM 信号，准备优雅地退出......')


def sighup_handler(sig, frame):
    settings.signals[signal.SIGHUP] = True
    print('触发 SIGHUP 信号，准备优雅地退出......')
