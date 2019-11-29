#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
from pathlib import PurePath
from happy_python import HappyLog

PPMS_PID_FILE = 'ppms.pid'
PPMS_LOCK_FILE = 'ppms.lock'
PPMS_CHILD_PID_FILE = 'ppms_child.pid'

CONFIG_DIR = PurePath(__file__).parents[1] / 'conf'
LOG_CONF_FILE = str(CONFIG_DIR / 'log.ini')

hlog = HappyLog.get_instance(LOG_CONF_FILE)

signals = {
    signal.SIGINT: False,
    signal.SIGHUP: False,
    signal.SIGTERM: False
}

TASK_NAME = ''
