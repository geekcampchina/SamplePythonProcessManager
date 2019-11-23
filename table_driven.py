#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
表驱动相关的设置
"""

from ppms_task import foo
from ppms_task import bar

TASK_TYPE_NAMES = {
    0: 'foo',
    1: 'bar',
}

TASK_NAME_CALLBACKS = {
    'foo': foo,
    'bar': bar,
}
