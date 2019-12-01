# Sample Python Process Manager

一个简化进程管理的 `Python` 库，丰富的命令行控制参数满足各种运行需求

***仅支持 Linux/Unix***

## 使用场景
- 需要不影响业务（一致性）的情况下管理进程，比如 stop/reload/restart
- 需要 `nohup`、`screen` 等运行
- 需要驻留后台

## 特点
__极少代码侵入，即可达到优雅的停止、重载（重启），不需要 `kill -9` 强制杀死进程，不影响业务数据处理或写入。__

## 安装

```bash
pip install sppm
```

## 用法

    usage: examples/example.py --no-daemon -d -v -l [--start|--stop|--reload|--shutdown|--restart|--status]

    简化进程管理的命令行工具

    optional arguments:
    -h, --help            show this help message and exit
    --no-daemon           不使用进程管理模式
    -l {0,1,2,3,4,5}, --log-level {0,1,2,3,4,5}
                          日志级别，CRITICAL|ERROR|WARNING|INFO|DEBUG|TRACE，默认等级3（INFO）
    --start               启动子进程
    --stop                等待子进程正常退出
    --reload              等待子进程正常退出，并启动新的子进程
    --shutdown            强制杀掉子进程
    --restart             强制杀掉子进程，并启动新的子进程
    --status              显示子进程状态
    -v, --version         显示版本信息

## 使用

### 代码

```python
import sppm

sppm.sppm_start(foo)
```

更多细节，请查看 `examples/example.py` 以及 `examples/example_working_lock.py`

### 管理

更多使用方法，请执行 `python3 examples/example.py -h` 查看帮助信息。

#### 启动
```bash
python3 examples/example.py --start
```

    2019-12-01 17:45:07 15048 [INFO] **** 按Ctrl+C可以终止运行 ****
    2019-12-01 17:45:07 15049 [INFO] Run 0 time(s) task->foo.
    2019-12-01 17:45:17 15049 [INFO] Run 1 time(s) task->foo.
    2019-12-01 17:45:27 15049 [INFO] Run 2 time(s) task->foo.
    2019-12-01 17:45:37 15049 [INFO] Run 3 time(s) task->foo.
    ^C2019-12-01 17:45:47 15049 [INFO] Run 4 time(s) task->foo.
    执行exit_callback函数


指定日志等级：

```bash
python3 examples/example.py --start -l 5
```

#### 查看状态
```bash
python3 examples/example.py --status
```

    pid                  : 16728
    ppid                 : 16727
    alive                : true
    uptime               : 152 second(s)
    human readable uptime: 2 minute(s), 32 second(s)
    create time          : 2019-12-01 18:32:30.300000
    active               : false
    last active time     : 2019-12-01 18:32:30.696024


#### 停止
```bash
python3 examples/example.py --stop
```

### 运行多个程序

```bash
python3 examples/example.py --start

SPPM_ENV=examples/.sppm_env_working_lock python examples/example_working_lock.py --start
```

    $ python3 examples/example.py --status
    pid                  : 17404
    ppid                 : 17403
    alive                : true
    uptime               : 48 second(s)
    human readable uptime: 48 second(s)
    create time          : 2019-12-01 18:49:47.880000
    active               : false
    last active time     : 2019-12-01 18:49:48.273476


    $ SPPM_ENV=examples/.sppm_env_working_lock python examples/example_working_lock.py --status
    pid                  : 17397
    ppid                 : 17396
    alive                : true
    uptime               : 40 second(s)
    human readable uptime: 40 second(s)
    create time          : 2019-12-01 18:49:25.690000
    active               : true
    last active time     : 2019-12-01 18:50:06.127305


### 配置文件

默认情况下，程序自动从环境变量 `SPPM_ENV` 加载 `Python` 文件目录下的 `.sppm_env`。

    $ cat examples/.sppm_env
    pid=/tmp/example.pid
    child_pid=/tmp/example_child.pid
    lock=/tmp/example.lock
    log=/tmp/example.log

运行多个程序时，每个程序必须单独配置环境变量 `SPPM_ENV` 指向不同的配置文件。