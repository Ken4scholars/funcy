import re, time

from funcy.debug import *


def test_tap():
    assert capture(tap, 42) == '42\n'
    assert capture(tap, 42, label='Life and ...') == 'Life and ...: 42\n'


def test_log_calls():
    log = []

    @log_calls(log.append)
    def f(x, y):
        return x + y

    f(1, 2)
    f('a', 'b')
    assert log == [
        "Call f(1, 2)",
        "-> 3 from f(1, 2)",
        "Call f('a', 'b')",
        "-> 'ab' from f('a', 'b')",
    ]


def test_log_calls_raise():
    log = []

    @log_calls(log.append)
    def f():
        raise Exception('something bad')

    try:
        f()
    except:
        pass
    assert log == [
        "Call f()",
        "-> raised Exception: something bad in f()",
    ]


def test_log_durations():
    log = []

    @log_durations(log.append)
    def f():
        time.sleep(0.010)

    f()
    m = re.search(r'^\s*(\d+\.\d+) ms in f\(\)$', log[0])
    assert m
    assert 10 <= float(m.group(1)) < 20


### An utility to capture stdout

import sys
from cStringIO import StringIO

def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        return sys.stdout.read()
    finally:
        sys.stdout = out
