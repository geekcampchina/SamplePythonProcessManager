#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    setup
    ~~~~
    sppm 是一个进程管理的库。
    :copyright: (c) 2018 by Chengdu Geek Camp.
    :license: MIT, see LICENSE for more details.
"""

from setuptools import setup
from os.path import join, dirname
from happy_python.version import __version__

with open(join(dirname(__file__), 'sppm/version.py'), 'r', encoding='utf-8') as f:
    exec(f.read())

with open(join(dirname(__file__), 'requirements.txt'), 'r', encoding='utf-8') as f:
    pkgs = f.read()
    print('pkgs', pkgs)
    install_requires = pkgs.split("\n")

setup(
    name='sppm',
    version=__version__,
    url='https://github.com/geekcampchina/SamplePythonProcessManager',
    license='GPL',
    author='Chengdu Geek Camp',
    author_email='info@cdgeekcamp.com',
    description="一个进程管理的库, 控制进程的前后台运行, 重启",
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