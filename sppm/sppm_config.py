#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SppmConfig类从环境变量指定的文件读取运行所需要的参数，参数用于处理进程信息，运行状态等。
"""

import os

_SppmConfigSingletonObj = None
ENV_VAR_NAME = 'SPPM_ENV'

CONFIG_KEYS = [
    'pid',
    'child_pid',
    'lock'
]


class SppmConfig:
    def __init__(self):
        self.pid_file = ''
        self.child_pid_file = ''
        self.lock_file = ''
        self.configs = {}
        self.env_file_path = os.environ[ENV_VAR_NAME]

        self.check_env()
        self.read_cfg()
        self.set_class_attrs()

    def check_env(self):
        """
        检查环境变量文件
        :return:
        """
        if ENV_VAR_NAME not in os.environ:
            raise EnvironmentError('未设置环境变量 SPPM_ENV ')

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
