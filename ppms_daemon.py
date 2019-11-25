#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import signal
import sys
import daemon
import settings
from ppms_child import start_child
from multiprocessing import Process

from process_status_lock import ProcessStatusLock
from settings import hlog
from signal_handler import sigint_handler
from utils import cleanup


def run(is_no_daemon, child_callback, *child_args):
    with open(settings.PPMS_PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    if is_no_daemon:
        hlog.info('**** 按Ctrl+C可以终止运行 ****')

    child_process = Process(target=start_child, args=(child_callback, *child_args))
    child_process.start()

    ProcessStatusLock.lock(child_process.pid, settings.PPMS_LOCK_FILE)

    with open(settings.PPMS_CHILD_PID_FILE, 'w') as f:
        f.write(str(child_process.pid))

    child_process.join()


def parser_cmd_options():
    parser = argparse.ArgumentParser(prog='ppms',
                                     description='进程管理工具',
                                     usage='%(prog)s --no-daemon -d -v [--stop|--start|--restart]')

    parser.add_argument('--no-daemon',
                        help='不使用进程管理模式',
                        required=False,
                        action='store_true')

    parser.add_argument('-d',
                        '--debug',
                        help='调试模式',
                        required=False,
                        action='store_true')

    # 定义互斥组，组中至少有一个参数是必须的:
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--start',
                              help='启动子进程',
                              action='store_true')

    action_group.add_argument('--stop',
                              help='优雅地停止子进程',
                              action='store_true')

    action_group.add_argument('--restart',
                              help='优雅地重启子进程',
                              action='store_true')

    parser.add_argument('-v',
                        '--version',
                        help='显示版本信息',
                        action='version',
                        version='%(prog)s v1.0.0')

    args = parser.parse_args()

    return args


def process_manager(cmd_args, child_callback, *child_args):
    if os.path.exists(settings.PPMS_PID_FILE):
        if not os.path.exists(settings.PPMS_CHILD_PID_FILE):
            print('子进程任务并未启动')
            exit(1)

        ppms_child_pid = ProcessStatusLock.get_pid_from_file(settings.PPMS_CHILD_PID_FILE)

        if cmd_args.start:
            hlog.error('ppms已经在运行......')
            exit(0)
        elif cmd_args.stop:
            os.kill(ppms_child_pid, signal.SIGTERM)
            # wait_unlock(args.task_type)
            ProcessStatusLock.should_kill(settings.PPMS_LOCK_FILE)
        elif cmd_args.restart:
            os.kill(ppms_child_pid, signal.SIGTERM)
            # wait_unlock(args.task_type)
            ProcessStatusLock.should_kill(settings.PPMS_LOCK_FILE)
            process_manager(cmd_args, child_callback, *child_args)
    else:
        if cmd_args.start or cmd_args.restart:
            run(cmd_args.no_daemon, child_callback, *child_args)
        else:
            hlog.error('ppms 并未启动，不能执行任何操作。')
            exit(1)


def main(child_callback, *child_args):
    try:
        cmd_args = parser_cmd_options()

        if cmd_args.no_daemon:
            signal.signal(signal.SIGINT, sigint_handler)

        if cmd_args.no_daemon:
            process_manager(cmd_args, child_callback, *child_args)
        else:
            log_file_descriptors = []

            for log_handler in hlog.get_logger().handlers:
                log_file_descriptors.append(log_handler.stream)

            if cmd_args.debug:
                with daemon.DaemonContext(files_preserve=log_file_descriptors,
                                          working_directory=os.getcwd(),
                                          stdout=sys.stdout,
                                          stderr=sys.stderr):
                    process_manager(cmd_args, child_callback, *child_args)
            else:
                with daemon.DaemonContext(files_preserve=log_file_descriptors,
                                          working_directory=os.getcwd()):
                    process_manager(cmd_args, child_callback, *child_args)
    except Exception as e:
        # 使用异常防止PID被删除两次的问题
        cleanup()
        raise Exception(e)
