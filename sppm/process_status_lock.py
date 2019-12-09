#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from time import sleep

from sppm.settings import hlog, SPPM_CONFIG


class ProcessStatusLock:
    MAX_IDLE_SECONDS = 2

    @staticmethod
    def get_pid_from_file(pid_file):
        """
        从文件读取PID
        :return:
        """
        with open(pid_file, 'r') as f:
            return int(f.readline())

    @staticmethod
    def wait_unlock_by_child(lock_file):
        n = 0

        while True:
            hlog.debug('从资源文件获取子进程状态，检测子进程是否空闲或退出......：%s' % lock_file)

            if SPPM_CONFIG.enable_timeout and n >= SPPM_CONFIG.timeout:
                hlog.debug('等待子进程退出超时')
                break

            if not ProcessStatusLock.is_working(lock_file) and ProcessStatusLock.is_idle(lock_file):
                hlog.debug('子进程空闲或已经退出')
                break

            n += 1
            sleep(1)

    @staticmethod
    def wait_unlock_by_file(lock_file):
        n = 0

        while True:
            hlog.debug('等待释放文件锁：%s' % lock_file)

            if SPPM_CONFIG.enable_timeout and n >= SPPM_CONFIG.timeout:
                hlog.debug('等待释放文件锁超时')
                break

            if not os.path.exists(lock_file):
                hlog.debug('文件锁：%s 已经释放' % lock_file)
                break

            n += 1
            sleep(1)

    @staticmethod
    def wait_unlock(lock_file):
        """
        等待子进程释放文件锁
        :return:
        """
        # noinspection PyBroadException
        try:
            ProcessStatusLock.wait_unlock_by_child(lock_file)
            ProcessStatusLock.wait_unlock_by_file(lock_file)
        except Exception:
            hlog.info('子进程已经退出')

    @staticmethod
    def lock(process_pid, lock_file, is_working=False):
        """
        子进程运行时，创建文件锁
        :param process_pid: 进程编号
        :param lock_file: 资源文件路径
        :param is_working: 工作状态
        :return:
        """
        block_timestamp = datetime.now().timestamp()

        with open(lock_file, 'w') as f:
            f.write(str(process_pid) + '\n')
            f.write(str(block_timestamp) + '\n')
            f.write(str(int(is_working)) + '\n')

    @staticmethod
    def get_block_timestamp(lock_file):
        """
        从文件锁获取时间戳
        :param lock_file: 资源文件路径
        :return:
        """
        block_timestamp = 0.0
        block_timestamp_line_no = 2
        line_no = 1

        with open(lock_file, 'r') as f:
            if line_no == block_timestamp_line_no:
                block_timestamp = float(f.readline())

            line_no += 1

        return block_timestamp

    @staticmethod
    def is_idle(lock_file):
        """
        进程是否空闲
        :param lock_file: 资源文件路径
        :return:
        """
        now_timestamp = datetime.now().timestamp()
        block_timestamp = ProcessStatusLock.get_block_timestamp(lock_file)
        result = now_timestamp - block_timestamp >= ProcessStatusLock.MAX_IDLE_SECONDS

        return result

    @staticmethod
    def is_working(lock_file):
        """
        进程活跃
        :param lock_file: 资源文件路径
        :return:
        """
        result = False
        total_line_num = 3

        with open(lock_file, 'r') as f:
            lines = f.readlines()

            if len(lines) != total_line_num:
                raise ValueError('无效的资源文件：%s' % lock_file)

            result = int(lines[2])

        return result


def working_lock(is_active: bool):
    ProcessStatusLock.lock(os.getpid(), SPPM_CONFIG.lock_file, is_active)
