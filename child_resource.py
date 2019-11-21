#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import PurePath
from happy_python import HappyLog

CONFIG_DIR = PurePath(__file__).parent / 'conf'
LOG_CONF_FILE = str(CONFIG_DIR / 'log.ini')


hlog = HappyLog.get_instance(LOG_CONF_FILE)
