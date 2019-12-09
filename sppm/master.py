#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import signal
import sys
from pathlib import Path

import daemon

from sppm.child import start_child
from sppm.cmd_action import action_stop, action_reload, action_shutdown, action_restart, action_status, action_start
from sppm.log_level import LogLevel, LOG_LEVEL_NAMES
from sppm.process_status_lock import ProcessStatusLock
from sppm.settings import hlog, SPPM_CONFIG
from sppm.signal_handler import sigint_handler
from sppm.utils import cleanup

exit_status = 0


def get_version():
    version_file = Path(__file__).parent / 'version.txt'

    with open(str(version_file), 'r', encoding='utf-8') as f:
        __version__ = f.read().strip()
        return __version__


def parser_cmd_options():
    parser = argparse.ArgumentParser(prog=Path(sys.argv[0]),
                                     description='简化进程管理的命令行工具',
                                     usage='%(prog)s --no-daemon -d -v -l'
                                           '[--start|--stop|--reload|--shutdown|--restart|--status]')

    parser.add_argument('--no-daemon',
                        help='不使用进程管理模式',
                        required=False,
                        action='store_true')

    parser.add_argument('-l',
                        '--log-level',
                        help='日志级别，CRITICAL|ERROR|WARNING|INFO|DEBUG|TRACE，默认等级3（INFO）',
                        type=int,
                        choices=LogLevel.get_list(),
                        default=LogLevel.INFO.value,
                        required=False)

    # 定义互斥组，组中至少有一个参数是必须的:
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--start',
                              help='启动子进程',
                              action='store_true')

    action_group.add_argument('--stop',
                              help='等待子进程正常退出',
                              action='store_true')

    action_group.add_argument('--reload',
                              help='等待子进程正常退出，并启动新的子进程',
                              action='store_true')

    action_group.add_argument('--shutdown',
                              help='强制杀掉子进程',
                              action='store_true')

    action_group.add_argument('--restart',
                              help='强制杀掉子进程，并启动新的子进程',
                              action='store_true')

    action_group.add_argument('--status',
                              help='显示子进程状态',
                              action='store_true')

    parser.add_argument('-v',
                        '--version',
                        help='显示版本信息',
                        action='version',
                        version='%(prog)s v' + get_version())

    args = parser.parse_args()

    return args


def process_manager(cmd_args, child_callback, *child_args):
    global exit_status

    if os.path.exists(SPPM_CONFIG.pid_file):
        if os.path.exists(SPPM_CONFIG.child_pid_file):
            child_pid = ProcessStatusLock.get_pid_from_file(SPPM_CONFIG.child_pid_file)

            if cmd_args.start:
                hlog.error('sppm 已经在运行......')
                exit_status = 1
            elif cmd_args.stop:
                action_stop(child_pid)
            elif cmd_args.reload:
                action_reload(child_pid, start_child, cmd_args.no_daemon, child_callback, *child_args)
            elif cmd_args.shutdown:
                action_shutdown(child_pid)
            elif cmd_args.restart:
                action_restart(child_pid, start_child, cmd_args.no_daemon, child_callback, *child_args)
            elif cmd_args.status:
                action_status()
            else:
                pass
        else:
            hlog.error('子进程任务并未启动')
            exit_status = 1
    else:
        if cmd_args.start:
            action_start(cmd_args.no_daemon, start_child, child_callback, *child_args)
        else:
            hlog.error('sppm 并未启动，不能执行任何操作。')
            exit_status = 1


def load_log_config(log_level: int):
    log_file = Path(SPPM_CONFIG.log_file)

    logger = logging.getLogger()
    file_handler = logging.FileHandler(str(log_file))
    formatter = logging.Formatter('%(asctime)s %(process)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logging.getLogger().setLevel(LOG_LEVEL_NAMES[log_level])


def sppm_start(child_callback, *child_args):
    try:
        cmd_args = parser_cmd_options()

        if cmd_args.no_daemon or cmd_args.stop or cmd_args.shutdown or cmd_args.reload or cmd_args.restart:
            # 前台运行收到 CTRL+C 信号，直接回调，然后退出。
            signal.signal(signal.SIGINT, sigint_handler)

        load_log_config(cmd_args.log_level)

        # 一些动作不需要守护进程执行
        if cmd_args.no_daemon or cmd_args.stop or cmd_args.shutdown or cmd_args.status:
            process_manager(cmd_args, child_callback, *child_args)
        else:
            log_file_descriptors = []

            log_handler: logging.StreamHandler
            for log_handler in logging.getLogger().handlers:
                log_file_descriptors.append(log_handler.stream)

            with daemon.DaemonContext(files_preserve=log_file_descriptors, working_directory=os.getcwd()):
                process_manager(cmd_args, child_callback, *child_args)
    except Exception as e:
        # 使用异常防止PID被删除两次的问题
        cleanup()
        raise Exception(e)

    exit(exit_status)
