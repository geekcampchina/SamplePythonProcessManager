#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    setup
    ~~~~
    sppm 是一个进程管理的库。
    :copyright: (c) 2018 by Chengdu Geek Camp.
    :license: MIT, see LICENSE for more details.
"""

from os.path import join, dirname
from setuptools import setup

with open(join(dirname(__file__), 'sppm/version.txt'), 'r', encoding='utf-8') as f:
    __version__ = f.read().strip()

with open(join(dirname(__file__), 'requirements.txt'), 'r', encoding='utf-8') as f:
    pkgs = f.read()
    install_requires = pkgs.split("\n")

setup(
    name='sppm',
    version=__version__,
    url='https://github.com/geekcampchina/SamplePythonProcessManager',
    license='GPL',
    author='Chengdu Geek Camp',
    author_email='info@cdgeekcamp.com',
    description="一个简化进程管理的 Python 库，丰富的命令行控制参数满足各种运行需求",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=['sppm'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
