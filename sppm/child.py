#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import signal
from sppm.signal_handler import sigterm_handler
from sppm.utils import cleanup
from sppm.settings import hlog


def start_child(task_callback, *args):
    func_name = inspect.stack()[0][3]
    hlog.enter_func(func_name)

    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        task_callback(*args)
    except Exception as e:
        hlog.error(e)
    finally:
        cleanup()

    hlog.exit_func(func_name)
