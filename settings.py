#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
from pathlib import PurePath
from happy_python import HappyLog

PPMS_PID_FILE = 'ppms.pid'
CONFIG_DIR = PurePath(__file__).parent / 'conf'
LOG_CONF_FILE = str(CONFIG_DIR / 'log.ini')

hlog = HappyLog.get_instance(LOG_CONF_FILE)

signals = {
    signal.SIGINT: False,
    signal.SIGHUP: False,
    signal.SIGTERM: False
}
