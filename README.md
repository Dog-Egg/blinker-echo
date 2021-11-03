# blinker-echo

一个 [blinker](https://pythonhosted.org/blinker/) 补丁，在控制台输出 signal 从 "发送" 到 "接收" 的过程

## 安装

```shell
# python 3.7及以上
pip install blinker-echo

# python 3.7以下
pip install blinker-echo contextvars
```

## 使用

```python
from blinker import signal
import blinker_echo

blinker_echo.patch()

signal_1 = signal('signal_1')
signal_2 = signal('signal_2')
signal_3 = signal('signal_3')


@signal_1.connect
def receiver_1(_):
    signal_2.send()
    signal_3.send()


@signal_1.connect
def receiver_2(_):
    pass


@signal_1.connect
def receiver_3(_):
    pass


if __name__ == '__main__':
    signal_1.send()
```

```
# 运行结果

[2021-12-01 12:00:00] blinker echo:
            ┌[r]receiver_3
            ├[r]receiver_2
 [s]signal_1┤
            │             ┌[s]signal_2
            └[r]receiver_1┤
                          └[s]signal_3
```