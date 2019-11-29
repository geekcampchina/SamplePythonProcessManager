# Sample Python Process Manager

## 介绍

由于爬虫系统需要部署在服务器, 长期运行, 所以需要使程序可以在后台运行, 并且退出终端等操作不会影响其运行。而使用简单的守护进程或者nohup的方式启动程序, 
每次启动或者停止程序前都需要额外的操作, 无法达到进程管理的目的。为了达到进程管理的目的, 并且做到优雅的停止或重启进程, 所以创建了该库。本库操作方法简单, 只需要在使用本库后启动程序时添加[--start|--stop|--restart]参数, 就可以达到基本的进程管理的效果。

## 使用场景
- 需要长时间驻留后台的程序
- 需要进行进程管理的程序
- 不建议使用于执行完毕会自动退出的程序。

## 安装
一般使用pip安装
```bash
pip install sppm
```

## 例子

#### 文件锁模式
假设原有一个程序`example.py`:
```python
from time import sleep


def foo():
    n = 0
    while True:
        print('Run %d time(s) task->%s.' % (n, "foo"))
        n += 1
        # 模拟任务执行需要两秒
        sleep(2)


    if __name__ == "__main__":
        foo()
```

现在需要使用`sppm`管理进程

导入`sppm`
```python
import sppm
```

使用[sppm_start](#sppm-start)将启动函数传递给`sppm`, 指定任务名称为`foo`
```python
sppm.sppm_start("foo", foo)
```

至此已经可以采用`sppm`的方式启动程序, 为了能够使用`sppm`停止和重启程序, 需要在每次任务处理完时使用[signal_monitor](#signal-monitor)判断是否需要退出
```python
if sppm.signal_monitor():
        break
```

修改完成后, 代码如下:
```python
from time import sleep
import sppm


def foo():

    n = 0
    while True:
        print('Run %d time(s) task->%s.' % (n, "foo"))
        n += 1
        # 模拟任务执行需要两秒
        sleep(2)
        if sppm.signal_monitor():
            break


if __name__ == "__main__":
    sppm.sppm_start("foo", foo)
```

#### 阻塞模式
除了以上方法, 还有一种启动方法阻塞情况下利用文件锁通信, 父进程根据文件锁判断子进程状态，是否可以关闭。

假设原有一个程序`example_block.py`:
```python
from time import sleep


def bar():
    n = 0
    while True:
        print('Run %d time(s) task->%s.' % (n, "bar"))
        n += 1
        # 模拟任务执行需要两秒
        sleep(2)


    if __name__ == "__main__":
        bar()
```

使用方式

导入`sppm`
```python
import sppm
```

使用[sppm_block_start](#sppm-block-start)将启动函数传递给`sppm`, 指定任务名称为`bar`
```python
sppm.sppm_block_start("bar", bar)
```

使用[lock](#lock)执行任务前添加文件锁
```python
    sppm.lock()
```

使用[signal_monitor](#signal-monitor)判断是否需要退出
```python
if sppm.signal_monitor():
        break
```

修改完成后, 代码如下:
```python
from time import sleep
import sppm


def bar():
    n = 0
    while True:
        sppm.lock()
        print('Run %d time(s) task->%s.' % (n, "bar"))
        n += 1
        # 模拟任务执行需要两秒
        sleep(2)
        if sppm.signal_monitor():
            break


if __name__ == "__main__":
    sppm.sppm_block_start("bar", bar)
```
#### 启动方式
终端进入`foo.py`所在文件夹  

参数说明
>-h或者--help查看参数帮助  
>[--start|--stop|--restart]执行文件时必须选择其中一个参数  
>--no-daemon参数代表后台执行, 不显示执行过程的输出结果, 对--restart参数也有效  
>--debug参数代表后台执行, 显示执行过程的输出结果, 对--restart参数也有效  


启动程序
```bash
python example.py --start
```

启动程序, 不使用后台执行
```bash
python example.py --start --no-daemon
```

启动程序, 使用后台执行, 但显示输出结果
```bash
python example.py --start --debug
```

停止程序
```bash
python example.py --stop
```

重启程序
```bash
python example.py --restart
```

#### 使用说明

<span id="sppm-start"></span>
>`sppm_start(task_name, child_callback=None, *child_args)`  
>>将原启动函数传递给`sppm`, 这种启动方式不需要利用文件通信, 另一种启动方式[sppm_block_start](#sppm-block-start)需要利用文件锁通信
>>>参数:
>>> - task_name(_str_) - 启动的任务名称, 必需的
>>> - child_callback(_callable, optional_) - 原启动函数, 默认为`None`
>>> - child_args(_any, optional_) - foo的参数, 数量可变

<span id="sppm-block-start"></span>
>`sppm_block_start(task_name, child_callback=None, *child_args)`  
>>将原启动函数传递给`sppm`, 这种启动方式利用文件通信, 另一种启动方式[sppm_start](#sppm-start)不需要利用文件锁通信。  
>>这种启动方式通过读取文件锁, 判断子进程工作状态以及是否陷入忙等待, 使用这种方式启动还需要使用`lock`函数指定文件锁位置以及修改子程序状态
>>>参数:
>>> - task_name(_str_) - 启动的任务名称, 必需的
>>> - child_callback(_callable, optional_) - 原启动函数, 默认为`None`
>>> - child_args(_any, optional_) - foo的参数, 数量可变

<span id="signal-monitor"></span>
>`signal_monitor(exit_callback=None, *exit_args)`
>>任务处理完成后是否需要退出。  
>>为了达到优雅退出的目的, 需要将退出操作告知`sppm`，由`sppm`关闭程序前代为执行,比如一些关闭文件句柄的操作、删除中间文件的操作。
>>>参数:
>>> - exit_callback(_callable, optional_) - 退出函数时的处理函数, 默认值`None`不作任何处理
>>> - args(_any, optional_) - exit_callback的参数, 数量可变

>>>返回值:is_exit  
>>>返回类型:bool  
>>>`True`代表程序收到了退出信号, 已经执行`exit_callback`,`False`代表没有收到退出信号

<span id="lock"></span>
>`lock(is_working=False)`
>>标记文件锁  
>>使用该函数, sppm会在指定的文件位置创建一个lock文件, 写入子进程pid、写入时间、工作状态, sppm会根据写入时间以及工作状态来判断能否终止进程。防止进程在工作状态被错误停止, 优雅终止进程。 
>>>参数:
>>> - is_working(_bool, optional_) - 进程工作状态, `True`代表正在进行业务处理中 `False`代表未进行业务处理, 为`True`时sppm不会杀死进程, 直到被修改为`False`, 默认为`False`

## 补充

1.  示例中[文件锁模式](#文件锁模式) 完整代码可以在`examples/example.py`查看
2.  示例中[阻塞模式](#阻塞模式) 完整代码可以在`examples/example_block.py`查看

## 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
