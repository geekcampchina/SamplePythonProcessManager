#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
from pathlib import PurePath

from happy_python import HappyLog

from sppm.sppm_config import SppmConfig

hlog = HappyLog.get_instance()

signals = {
    signal.SIGINT: False,
    signal.SIGHUP: False,
    signal.SIGTERM: False
}

SPPM_CONFIG = SppmConfig.get_instance()
