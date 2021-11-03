import functools
import time
from contextvars import ContextVar

from pptree import print_tree, Node

_var = ContextVar('echo')


def _echo_wrap(func, *, name):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            parent = _var.get()
        except LookupError:
            parent = None

        node = Node(name, parent)
        token = _var.set(node)

        try:
            return func(*args, **kwargs)
        finally:
            _var.reset(token)
            if parent is None:
                print('[%s] blinker echo:' % time.strftime('%F %H:%M:%S'))
                print_tree(node)

    return wrapper


def _patch_connect(connect):
    @functools.wraps(connect)
    def wrapper(self, receiver, *args, **kwargs):
        receiver = _echo_wrap(receiver, name='[r]' + receiver.__name__)
        return connect(self, receiver, *args, **kwargs)

    return wrapper


def _patch_send(send):
    @functools.wraps(send)
    def wrapper(self, *args, **kwargs):
        _send = _echo_wrap(send, name='[s]' + self.name)
        return _send(self, *args, **kwargs)

    return wrapper


def patch():
    from blinker import Signal

    Signal.send = _patch_send(Signal.send)
    Signal.connect = _patch_connect(Signal.connect)
