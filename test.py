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
