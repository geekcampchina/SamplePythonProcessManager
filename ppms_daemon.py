#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


def main():
    parser = argparse.ArgumentParser(prog='daemon',
                                     description='Python Process Manager Sample',
                                     usage='%(prog)s --no-daemon [-f|-b] -B <baz> -V',
                                     epilog="Python编写的进程管理程序示例")

    parser.add_argument('--no-daemon',
                        help='不使用进程管理模式',
                        required=False,
                        action='store_true')

    # 定义互斥组，组中至少有一个参数是必须的:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f',
                       '--foo',
                       help='以子进程方式运行任务foo',
                       action='store_true')
    group.add_argument('-b',
                       '--bar',
                       help='以子进程方式运行任务bar',
                       action='store_true')

    parser.add_argument('-B',
                        '--baz',
                        help='参数baz',
                        required=False,
                        type=int,
                        action='store',
                        default=8888,
                        dest='baz')

    parser.add_argument('-V',
                        '--version',
                        help='显示版本信息',
                        action='version',
                        version='%(prog)s v1.0.1')

    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()
