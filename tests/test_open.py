import os
import pathlib
import sys
from typing import Optional
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture  # type: ignore
from pytest_subprocess.fake_process import FakeProcess  # type: ignore

import shopen

from .testutil import (
    assert_cmd_call,
    assert_cmd_calls,
    no_such_command_callback,
    register_openers,
)


@pytest.fixture
def tmpfile(tmp_path: pathlib.Path):
    somefile = tmp_path.joinpath("somefile.txt")
    somefile.touch()
    return somefile


@pytest.fixture
def os_startfile(mocker: MockerFixture) -> Optional[Mock]:
    if not hasattr(os, "startfile"):
        return None
    mocker.patch("os.startfile")
    return os.startfile


def test_empty():
    with pytest.raises(TypeError):
        shopen.open()


@pytest.mark.skipif(
    sys.platform != "win32", reason="os.startfile currently only supports win32"
)
def test_os_startfile(
    tmpfile: pathlib.Path, os_startfile: Mock, fp: FakeProcess
):
    shopen.open(tmpfile, "open")
    os_startfile.assert_called_once_with(tmpfile, "open")
    assert not fp.calls


@pytest.mark.skipif(
    sys.platform != "darwin", reason="testing darwin-specific behavior"
)
def test_plat_darwin_open(tmpfile: pathlib.Path, fp: FakeProcess):
    register_openers(fp, ["open"])
    shopen.open(tmpfile, "open")
    assert_cmd_calls(["open"], fp)


@pytest.mark.skipif(
    sys.platform in ("win32", "darwin"),
    reason="testing platform-specific behavior for linux, etc",
)
def test_plat_linux_etc_xdg_open(tmpfile: pathlib.Path, fp: FakeProcess):
    register_openers(fp, ["xdg-open"])
    shopen.open(tmpfile, "open")
    assert_cmd_calls(["xdg-open"], fp)


@pytest.mark.skipif(
    sys.platform in ("win32", "darwin"),
    reason="testing platform-specific behavior for linux, etc",
)
def test_plat_linux_etc_open(tmpfile: pathlib.Path, fp: FakeProcess):
    """If xdg-open isn't available, runs the `open` command."""
    fp.register(["xdg-open", fp.any()], callback=no_such_command_callback)
    register_openers(fp, ["open"])
    shopen.open(tmpfile, "open")
    assert_cmd_calls(["xdg-open", "open"], fp)


def test_default_op_open(
    tmpfile: pathlib.Path, os_startfile: Mock, fp: FakeProcess
):
    register_openers(fp)
    shopen.open(tmpfile)
    if sys.platform == "win32":
        os_startfile.assert_called_once()
    else:
        assert_cmd_call({"xdg-open", "open"}, fp)


def test_string_path(
    tmpfile: pathlib.Path, os_startfile: Mock, fp: FakeProcess
):
    register_openers(fp)
    shopen.open(str(tmpfile))
    if sys.platform == "win32":
        os_startfile.assert_called_once()
    else:
        assert_cmd_call({"xdg-open", "open"}, fp)
