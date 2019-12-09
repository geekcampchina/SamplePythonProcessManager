#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class LogLevel(Enum):
    CRITICAL = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5

    @staticmethod
    def get_list():
        return [*range(LogLevel.CRITICAL.value, LogLevel.CRITICAL.TRACE.value + 1)]


LOG_LEVEL_NAMES = {
    LogLevel.CRITICAL.value: 'CRITICAL',
    LogLevel.ERROR.value: 'ERROR',
    LogLevel.WARNING.value: 'WARNING',
    LogLevel.INFO.value: 'INFO',
    LogLevel.DEBUG.value: 'DEBUG',
    LogLevel.TRACE.value: 'TRACE',
}
