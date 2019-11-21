#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
from signal_handler import sighup_handler
from signal_handler import sigterm_handler
from utils import cleanup


def start_child(task_callback, *args):
    signal.signal(signal.SIGHUP, sighup_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

    task_callback(args)
    cleanup()
