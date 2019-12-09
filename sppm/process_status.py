#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

import psutil

from sppm.utils import to_uptime_format


class ProcessStatus:
    def __init__(self, resource_file):
        # 父进程编号
        self.ppid = 0
        # 进程编号
        self.pid = 0
        # 进程存活时间，单位秒
        self.uptime = 0
        # 进程是否处于活跃期
        self.active = False
        # 上次活跃时间
        self.last_active_time = datetime.now()
        # 进程是否存在
        self.alive = False
        self.resource_file = resource_file
        # 进程创建时间
        self.create_time = datetime.now()

        self.load_status()

    def load_status(self):
        self.read_resource_file()

        process = psutil.Process(self.pid)
        self.ppid = process.ppid()
        self.alive = process.is_running()
        self.create_time = datetime.fromtimestamp(process.create_time())
        self.uptime = datetime.now().timestamp() - process.create_time()

    def read_resource_file(self):
        """
        读取配置文件内容
        :return:
        """
        total_line_num = 3

        with open(self.resource_file, 'r') as f:
            lines = f.readlines()

            if len(lines) != total_line_num:
                raise ValueError('无效的资源文件：%s' % self.resource_file)

            self.pid = int(lines[0])
            self.last_active_time = datetime.fromtimestamp(float(lines[1]))
            self.active = bool(int(lines[2]))

    def __str__(self):
        return 'pid                  : %d\n' \
               'ppid                 : %d\n' \
               'alive                : %s\n' \
               'uptime               : %d second(s)\n' \
               'human readable uptime: %s\n' \
               'create time          : %s\n' \
               'active               : %s\n' \
               'last active time     : %s' \
               % (
                   self.pid,
                   self.ppid,
                   str(self.alive).lower(),
                   self.uptime,
                   to_uptime_format(self.uptime),
                   self.create_time.strftime('%F %T.%f'),
                   str(self.active).lower(),
                   self.last_active_time.strftime('%F %T.%f')
               )
