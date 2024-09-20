import os
import pathlib
import sys
from typing import Optional
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture
from pytest_subprocess import FakeProcess

import shopen

from .testutil import no_such_command_callback, register_openers


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
        shopen.open(operation="edit")


@pytest.mark.skipif(
    sys.platform != "win32", reason="os.startfile currently only supports win32"
)
def test_os_startfile(
    tmpfile: pathlib.Path, os_startfile: Mock, fp: FakeProcess
):
    shopen.open(tmpfile, "edit")
    os_startfile.assert_called_once_with(tmpfile, "edit")
    assert not fp.calls


@pytest.mark.skipif(
    sys.platform == "win32", reason="testing non-Windows scenarios"
)
def test_plat_nonwindows_editor(tmpfile: pathlib.Path, fp: FakeProcess):
    register_openers(fp, ["editor"])
    shopen.open(tmpfile, "edit")
    assert ["editor", tmpfile] in fp.calls


@pytest.mark.skipif(
    sys.platform == "win32", reason="testing non-Windows scenarios"
)
def test_plat_nonwindows_env(
    tmpfile: pathlib.Path, monkeypatch: pytest.MonkeyPatch, fp: FakeProcess
):
    fp.register(["editor", fp.any()], callback=no_such_command_callback)
    monkeypatch.setenv("EDITOR", "someeditor")
    fp.register(["someeditor", fp.any()])
    shopen.open(tmpfile, "edit")
    assert ["someeditor", tmpfile] in fp.calls


@pytest.mark.skipif(
    sys.platform in ("win32", "darwin"),
    reason="testing platform-specific behavior for linux, etc",
)
def test_plat_nonwindows_xdg_open(
    tmpfile: pathlib.Path, monkeypatch: pytest.MonkeyPatch, fp: FakeProcess
):
    fp.register(["editor", fp.any()], callback=no_such_command_callback)
    monkeypatch.delenv("EDITOR", raising=False)
    register_openers(fp, ["xdg-open"])
    shopen.open(tmpfile, "edit")
    assert ["xdg-open", tmpfile] in fp.calls


@pytest.mark.skipif(
    sys.platform == "win32", reason="testing non-Windows scenarios"
)
def test_plat_nonwindows_open(
    tmpfile: pathlib.Path, monkeypatch: pytest.MonkeyPatch, fp: FakeProcess
):
    fp.register(["editor", fp.any()], callback=no_such_command_callback)
    monkeypatch.delenv("EDITOR", raising=False)
    fp.register(["xdg-open", fp.any()], callback=no_such_command_callback)
    register_openers(fp, ["open"])
    shopen.open(tmpfile, "edit")
    assert ["open", tmpfile] in fp.calls
