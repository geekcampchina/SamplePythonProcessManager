#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
import settings
# for 子进程：此处导入包仅仅解决语法问题，由于跨守护进程文件句柄已经被关闭
# for 子进程：实际生效的hlog在 process_manager 函数中被导入
from settings import hlog


def sigint_handler(sig, frame):
    settings.signals[signal.SIGINT] = True
    hlog.debug('Ctrl+C，准备优雅地退出......')


def sigterm_handler(sig, frame):
    settings.signals[signal.SIGTERM] = True
    hlog.debug('触发 SIGTERM 信号，准备优雅地退出......')


def sighup_handler(sig, frame):
    settings.signals[signal.SIGHUP] = True
    hlog.debug('触发 SIGHUP 信号，准备优雅地退出......')
