#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import signal
import sys
from time import sleep

import daemon
from ppms_child import start_child
from multiprocessing import Process
import settings
from signal_handler import sigint_handler
from utils import cleanup, make_child_pid_filename, get_pid_from_file, lock_child, wait_unlock


def run(args):
    with open(settings.PPMS_PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    if args.no_daemon:
        print('**** 按Ctrl+C可以终止运行 ****')

    task_name = settings.TASK_TYPE_NAMES[args.task_type]
    task_callback = settings.TASK_NAME_CALLBACKS[task_name]

    child_process = Process(target=start_child, args=(task_callback, '测试参数'))
    child_process.start()

    lock_child(args.task_type, str(child_process.pid))

    with open(make_child_pid_filename(args.task_type), 'w') as f:
        f.write(str(child_process.pid))

    child_process.join()


def parser_cmd_options():
    parser = argparse.ArgumentParser(prog='daemon',
                                     description='Python Process Manager Sample',
                                     usage='%(prog)s --no-daemon -d [-f|-b] -B <baz> -V',
                                     epilog="Python编写的进程管理程序示例")

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
    type_group = parser.add_mutually_exclusive_group(required=True)
    type_group.add_argument('-f',
                            '--foo',
                            help='运行子进程任务：foo',
                            action='store_true')
    type_group.add_argument('-b',
                            '--bar',
                            help='运行子进程任务：bar',
                            action='store_true')

    # 定义互斥组，组中至少有一个参数是必须的:
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--start',
                              help='启动子进程任务',
                              action='store_true')

    action_group.add_argument('--stop',
                              help='优雅地停止子进程任务',
                              action='store_true')

    action_group.add_argument('--restart',
                              help='优雅地重启子进程任务',
                              action='store_true')

    parser.add_argument('-V',
                        '--version',
                        help='显示版本信息',
                        action='version',
                        version='%(prog)s v1.0.0')

    args = parser.parse_args()
    args.task_type = 0 if args.foo else 1

    return args


def process_manager(args):
    if os.path.exists(settings.PPMS_PID_FILE):
        child_pid_file = make_child_pid_filename(args.task_type)

        if not os.path.exists(child_pid_file):
            print('[ERROR] -f 或 -b 指定的子进程任务并未启动')
            exit(1)

        ppms_child_pid = get_pid_from_file(child_pid_file)

        if args.start:
            print('ppms已经在运行......')
            exit(0)
        elif args.stop:
            os.kill(ppms_child_pid, signal.SIGTERM)
            wait_unlock(args.task_type)
        elif args.restart:
            os.kill(ppms_child_pid, signal.SIGTERM)
            wait_unlock(args.task_type)
            process_manager(args)
    else:
        if args.start or args.restart:
            run(args)
        else:
            print('ppms 并未启动，不能执行任何操作。')
            exit(1)


def main(args):
    if args.no_daemon:
        signal.signal(signal.SIGINT, sigint_handler)

    if args.no_daemon:
        process_manager(args)
    else:
        if args.debug:
            with daemon.DaemonContext(working_directory=os.getcwd(), stdout=sys.stdout, stderr=sys.stderr):
                process_manager(args)
        else:
            with daemon.DaemonContext(working_directory=os.getcwd()):
                process_manager(args)


if __name__ == '__main__':
    try:
        main(parser_cmd_options())
    except Exception as e:
        # 使用异常防止PID被删除两次的问题
        cleanup()
        raise Exception(e)
