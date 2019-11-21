#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
from ppms_task import foo
from ppms_task import bar

PPMS_PID_FILE = 'ppms.pid'

TASK_TYPE_NAMES = {
    0: 'foo',
    1: 'bar',
}

TASK_NAME_CALLBACKS = {
    'foo': foo,
    'bar': bar,
}

signals = {
    signal.SIGINT: False,
    signal.SIGHUP: False,
    signal.SIGTERM: False
}
