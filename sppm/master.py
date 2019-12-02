#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import daemon
import logging
import os
import signal
import sys
from sppm.child import start_child
from multiprocessing import Process
from pathlib import Path

from sppm.log_level import LogLevel, LOG_LEVEL_NAMES
from sppm.process_status import ProcessStatus
from sppm.process_status_lock import ProcessStatusLock
from sppm.settings import hlog, SPPM_CONFIG
from sppm.signal_handler import sigint_handler, sigint_handler_exit
from sppm.utils import cleanup
from sppm.version import __version__

exit_status = 0


def action_start(is_no_daemon, child_callback, *child_args):
    with open(SPPM_CONFIG.pid_file, 'w') as f:
        f.write(str(os.getpid()))

    if is_no_daemon:
        hlog.info('**** 按Ctrl+C可以终止运行 ****')

    child_process = Process(target=start_child, args=(child_callback, *child_args))
    child_process.start()

    ProcessStatusLock.lock(child_process.pid, SPPM_CONFIG.lock_file)

    with open(SPPM_CONFIG.child_pid_file, 'w') as f:
        f.write(str(child_process.pid))

    child_process.join()


def action_stop(child_pid):
    os.kill(child_pid, signal.SIGTERM)
    ProcessStatusLock.wait_unlock(SPPM_CONFIG.lock_file)

    if SPPM_CONFIG.enable_timeout:
        action_shutdown(child_pid)


def action_reload(child_pid, is_no_daemon, child_callback, *child_args):
    action_stop(child_pid)
    action_start(is_no_daemon, child_callback, *child_args)


def action_shutdown(child_pid):
    os.kill(child_pid, signal.SIGTERM)
    hlog.info('当前处于强杀模式下，子进程 %d 将被强制杀死......' % child_pid)

    try:
        os.kill(child_pid, signal.SIGKILL)
    except Exception as e:
        del e
        hlog.info('子进程已经退出')

    # 强杀模式，子进程无法自己释放资源文件，需要父进程手动释放
    cleanup()


def action_restart(child_pid, is_no_daemon, child_callback, *child_args):
    action_shutdown(child_pid)
    action_start(is_no_daemon, child_callback, *child_args)


def action_status():
    ps = ProcessStatus(SPPM_CONFIG.lock_file)
    print(ps)


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
                        version='%(prog)s v' + __version__)

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
                action_reload(child_pid, cmd_args.no_daemon, child_callback, *child_args)
            elif cmd_args.shutdown:
                action_shutdown(child_pid)
            elif cmd_args.restart:
                action_restart(child_pid, cmd_args.no_daemon, child_callback, *child_args)
            elif cmd_args.status:
                action_status()
            else:
                pass
        else:
            hlog.error('子进程任务并未启动')
            exit_status = 1
    else:
        if cmd_args.start:
            action_start(cmd_args.no_daemon, child_callback, *child_args)
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

        # 注意防止Ctrl+C信号被绑定两次
        if cmd_args.no_daemon:
            signal.signal(signal.SIGINT, sigint_handler)
        elif cmd_args.stop or cmd_args.shutdown:
            signal.signal(signal.SIGINT, sigint_handler_exit)

        load_log_config(cmd_args.log_level)

        # 一些动作不需要守护进程执行
        if cmd_args.no_daemon or cmd_args.stop or cmd_args.shutdown or cmd_args.status:
            process_manager(cmd_args, child_callback, *child_args)
        else:
            log_file_descriptors = []

            for log_handler in logging.getLogger().handlers:
                log_file_descriptors.append(log_handler.stream)

            with daemon.DaemonContext(files_preserve=log_file_descriptors, working_directory=os.getcwd()):
                process_manager(cmd_args, child_callback, *child_args)
    except Exception as e:
        # 使用异常防止PID被删除两次的问题
        cleanup()
        raise Exception(e)

    exit(exit_status)
