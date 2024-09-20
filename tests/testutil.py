from typing import Sequence, Set, Tuple, Union

from pytest_subprocess.fake_process import FakeProcess  # type: ignore


def register_openers(fp: FakeProcess, commands=("xdg-open", "open")):
    for command in commands:
        fp.register([command, fp.any()])


def assert_cmd_calls(expected: Sequence[str], fp: FakeProcess):
    assert all(
        list(a)[0] == e for e, a in zip(expected, fp.calls) if a
    ), f"Missing expected call from {expected}. Actual: {list(fp.calls)}"


def assert_cmd_call(expected: Union[str, Set[str]], fp: FakeProcess):
    expected_set = expected if isinstance(expected, set) else {expected}
    assert any(
        list(a)[0] in expected_set for a in fp.calls if a
    ), f"Missing expected call from {expected_set}. Actual: {list(fp.calls)}"


def assert_calls(calls: Sequence[Tuple[str, ...]], fp: FakeProcess):
    assert all(
        a == b
        for actual, expected in zip(fp.calls, calls)
        for a, b in zip(actual, expected)
    ), f"Calls didn't match.\nExpected: {calls}\nActual: {fp.calls}"


def no_such_command_callback(process):
    raise FileNotFoundError(2, "No such file or directory")
