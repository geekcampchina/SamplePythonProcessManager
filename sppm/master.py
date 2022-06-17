#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import signal
import sys

import daemon

from sppm.child import start_child
from sppm.cmd_action import action_stop, action_reload, action_shutdown, action_restart, action_status, action_start
from sppm.process_status_lock import ProcessStatusLock
from sppm.settings import hlog, SPPM_CONFIG
from sppm.signal_handler import sigint_handler
from sppm.utils import cleanup
from sppm_help import build_sppm_help

exit_status = 0


def default_build_sppm_help(child_help_desc):
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description=child_help_desc,
                                     usage='%(prog)s --no-daemon -v -l '
                                           '[--start|--stop|--reload|--shutdown|--restart|--status]')

    return build_sppm_help(parser)


def process_manager(cmd_args, child_callback, *child_args, **child_kwargs):
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
                action_reload(child_pid, start_child, cmd_args.no_daemon, child_callback, *child_args, **child_kwargs)
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
            action_start(cmd_args.no_daemon, start_child, child_callback, *child_args, **child_kwargs)
        else:
            hlog.error('sppm 并未启动，不能执行任何操作。')
            exit_status = 1


def _sppm_start(cmd_args, child_callback, *child_args, **child_kwargs):
    """
    sppm启动方法
    @param cmd_args: parser.parse_args() 结果
    @param child_callback: 子进程启动函数
    @param child_args: 子进程启动函数的参数
    @return:
    """
    from setproctitle import setproctitle

    setproctitle('sppm: master process %s %s' % (sys.executable, ' '.join(sys.argv)))

    try:
        if cmd_args.no_daemon or cmd_args.stop or cmd_args.shutdown or cmd_args.reload or cmd_args.restart:
            # 前台运行收到 CTRL+C 信号，直接回调，然后退出。
            signal.signal(signal.SIGINT, sigint_handler)

        hlog.set_level(cmd_args.log_level)

        # 一些动作不需要守护进程执行
        if cmd_args.no_daemon or cmd_args.stop or cmd_args.shutdown or cmd_args.status:
            process_manager(cmd_args, child_callback, *child_args, **child_kwargs)
        else:
            log_file_descriptors = []

            log_handler: logging.StreamHandler
            for log_handler in logging.getLogger().handlers:
                log_file_descriptors.append(log_handler.stream)

            with daemon.DaemonContext(files_preserve=log_file_descriptors, working_directory=os.getcwd()):
                process_manager(cmd_args, child_callback, *child_args, **child_kwargs)
    except Exception as e:
        # 使用异常防止PID被删除两次的问题
        cleanup()
        raise Exception(e)

    exit(exit_status)


def sppm_start(child_callback, child_help_desc, *child_args, **child_kwargs):
    parser = default_build_sppm_help(child_help_desc)
    cmd_args = parser.parse_args()

    _sppm_start(cmd_args, child_callback, child_help_desc, *child_args, **child_kwargs)


def sppm_start_shell(child_callback, cmd_args):
    _sppm_start(cmd_args, child_callback, shell=cmd_args.shell[0])
