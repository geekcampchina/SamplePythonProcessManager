from pathlib import Path

from happy_python.happy_log import HappyLogLevel


def get_version():
    version_file = Path(__file__).parent / 'version.txt'

    with open(str(version_file), 'r', encoding='utf-8') as f:
        __version__ = f.read().strip()
        return __version__


def build_sppm_help(parser):
    parser.add_argument('--no-daemon',
                        help='不使用进程管理模式',
                        required=False,
                        action='store_true')

    parser.add_argument('-l',
                        '--log-level',
                        help='日志级别，0（CRITICAL）、1（ERROR）、2（WARNING）、3（INFO）、4（DEBUG）、5（TRACE），默认等级3',
                        type=int,
                        choices=HappyLogLevel.get_list(),
                        default=HappyLogLevel.INFO.value,
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
                        version='%(prog)s v' + get_version())

    return parser
