#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import signal

from sppm.settings import hlog
from sppm.signal_handler import sigterm_handler
from sppm.utils import cleanup


# noinspection PyUnusedLocal
def sigint_skip_handler(sig, frame):
    pass


def start_child(task_callback, *args):
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    signal.signal(signal.SIGTERM, sigterm_handler)

    # 子进程不需要响应Ctrl+C事件
    signal.signal(signal.SIGINT, sigint_skip_handler)

    try:
        task_callback(*args)
    except Exception as e:
        hlog.error(e)
    finally:
        cleanup()

    hlog.exit_func(func_name)
