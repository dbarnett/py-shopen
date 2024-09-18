from typing import Sequence, Tuple

from pytest_subprocess.fake_process import FakeProcess


def register_openers(fp: FakeProcess, commands=("xdg-open", "open")):
    for command in commands:
        fp.register([command, fp.any()])


def assert_calls(calls: Sequence[Tuple[str, ...]], fp: FakeProcess):
    assert all(
        a == b
        for actual, expected in zip(fp.calls, calls)
        for a, b in zip(actual, expected)
    ), f"Calls didn't match.\nExpected: {calls}\nActual: {fp.calls}"


def no_such_command_callback(process):
    raise FileNotFoundError(2, "No such file or directory")
