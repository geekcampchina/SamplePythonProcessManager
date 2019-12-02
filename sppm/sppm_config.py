#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SppmConfig类从环境变量指定的文件读取运行所需要的参数，参数用于处理进程信息，运行状态等。
"""

import os
import sys
from pathlib import Path

_SppmConfigSingletonObj = None
ENV_VAR_NAME = 'SPPM_ENV'
DEFAULT_CONFIG_FILENAME = '.sppm_env'

CONFIG_KEYS = [
    'pid',
    'child_pid',
    'lock',
    'log',
    'timeout'
]


class SppmConfig:
    def __init__(self):
        self.pid_file = ''
        self.child_pid_file = ''
        self.lock_file = ''
        self.configs = {}
        self.env_file_path = ''
        self.log_file = ''
        self.timeout = 0
        self.enable_timeout = False

        self.load_env()
        self.check_env()
        self.read_cfg()
        self.set_class_attrs()
        self.mkdirs()

    def load_env(self):
        if ENV_VAR_NAME not in os.environ:
            self.env_file_path = Path(sys.argv[0]).absolute().parent / DEFAULT_CONFIG_FILENAME
        else:
            self.env_file_path = os.environ[ENV_VAR_NAME]

    def check_env(self):
        """
        检查环境变量文件
        :return:菜单
        """
        if not os.path.exists(self.env_file_path):
            raise FileNotFoundError('%s 文件不存在' % self.env_file_path)

        if not os.path.isfile(self.env_file_path):
            raise IOError('%s 不是文件或无法识别' % self.env_file_path)

    def read_cfg(self):
        """
        读取配置文件内容
        :return:
        """
        with open(self.env_file_path, 'r') as f:
            lines = f.readlines()

            for line in lines:
                line = line.strip()

                if not line:
                    raise ValueError('内容无法识别：%s' % line)

                sep = '='
                index = line.find(sep)

                if index == -1:
                    raise ValueError('内容无法识别：%s' % line)

                key = line[:index]
                value = line[index + len(sep):]

                if key == 'timeout':
                    # 如果value不是整数，会抛出异常提示用户
                    timeout = int(value)

                    if timeout < 0:
                        raise ValueError('参数 timeout 的值不能小于 0' % value)
                else:
                    if not os.path.isabs(value):
                        raise ValueError('仅支持绝对路径：%s' % value)

                self.configs[key] = value

    def set_class_attrs(self):
        """
        设置类属性
        :return:
        """
        for key in CONFIG_KEYS:
            if key not in self.configs:
                raise ValueError('未配置参数 %s' % key)

        self.pid_file = self.configs['pid']
        self.child_pid_file = self.configs['child_pid']
        self.lock_file = self.configs['lock']
        self.log_file = self.configs['log']
        self.timeout = int(self.configs['timeout'])
        self.enable_timeout = self.timeout > 0

    def mkdirs(self):
        """
        创建配置文件传入的文件夹
        :return:
        """
        file_list = [
            self.pid_file,
            self.child_pid_file,
            self.lock_file,
            self.log_file
        ]

        for file in file_list:
            file_path = Path(file)
            # 递归创建文件夹
            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True)

    @staticmethod
    def get_instance():
        """
        单例模式
        :return:
        """
        global _SppmConfigSingletonObj

        if not _SppmConfigSingletonObj:
            _SppmConfigSingletonObj = SppmConfig()

        return _SppmConfigSingletonObj
