#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import signal

from signal_handler import sighup_handler
from signal_handler import sigterm_handler
from utils import cleanup
# 此处导入包仅仅解决语法问题，由于跨守护进程文件句柄已经被关闭
# 实际生效的hlog在 process_manager 函数中被导入
from settings import hlog


def start_child(task_callback, *args):
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    signal.signal(signal.SIGHUP, sighup_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        task_callback(args)
    except Exception as e:
        hlog.error(e)
    finally:
        cleanup()

    hlog.exit_func(func_name)
