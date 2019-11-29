#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
from datetime import datetime
import os
from time import sleep
from sppm.settings import hlog, SPPM_CONFIG
from sppm.utils import cleanup


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
    def wait_unlock(lock_file):
        """
        等待子进程释放文件锁
        :return:
        """
        while True:
            hlog.debug('等待释放文件锁：%s' % lock_file)

            if not os.path.exists(lock_file):
                hlog.debug('文件锁：%s 已经释放' % lock_file)
                break

            sleep(1)

    @staticmethod
    def lock(process_pid, lock_file, is_working=False):
        """
        子进程运行时，创建文件锁
        :param process_pid:
        :param lock_file:
        :param is_working: 是否活跃
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
        :param lock_file:
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
        :return:
        """
        now_timestamp = datetime.now().timestamp()
        block_timestamp = ProcessStatusLock.get_block_timestamp(lock_file)
        # print('now_timestamp=%f' % now_timestamp)
        # print('block_timestamp=%f' % block_timestamp)
        # print('ProcessStatusLock.MAX_IDLE_SECONDS=%f' % ProcessStatusLock.MAX_IDLE_SECONDS)

        if now_timestamp - block_timestamp >= ProcessStatusLock.MAX_IDLE_SECONDS:
            return True

        return False

    @staticmethod
    def is_working(lock_file):
        """
        进程活跃
        :param lock_file:
        :return: 1表示活跃，0表示空闲
        """
        result = False
        working_mark_line_no = 3
        line_no = 1

        with open(lock_file, 'r') as f:
            if line_no == working_mark_line_no:
                result = int(f.readline())

            line_no += 1

        return result

    @staticmethod
    def should_kill(lock_file):
        """
        是否可以杀死进程。
        标记进程状态为：等待退出，然后自杀
        :return:
        """
        process_id = ProcessStatusLock.get_pid_from_file(lock_file)

        while True:
            hlog.debug('读取文件锁时间戳，检测子进程是否空闲......：%s' % lock_file)

            if not ProcessStatusLock.is_working(lock_file) and ProcessStatusLock.is_idle(lock_file):
                hlog.debug('根据时间戳检测到子进程已经空闲，发送终止信号......')

                # 发送终止信号，就算使用SIGKILL强制杀掉进程
                # 代码用户也可以自行判断信号，跳过数据处理
                os.kill(process_id, signal.SIGTERM)

                os.kill(process_id, signal.SIGKILL)
                cleanup()

                break

            sleep(1)


def lock(is_work=False):
    ProcessStatusLock.lock(os.getpid(), SPPM_CONFIG.lock_file, is_work)
