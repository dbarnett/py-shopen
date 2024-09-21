import os
import sys

import pytest

import shopen

from .testutil import OpScenario


@pytest.mark.parametrize("use_str_path", [False, True])
def test_simple_success(mocked_openers, tmpfile, use_str_path: bool):
    """First attempted opener strategy for the platform should succeed."""
    if use_str_path:
        tmpfile = str(tmpfile)
    mocked_openers.mock_all()
    shopen.open(tmpfile, "open")
    fp = mocked_openers.fp
    if sys.platform == "win32":
        mocked_openers.os_startfile.assert_called_once_with(tmpfile, "open")
        assert not fp.calls
    else:
        assert list(fp.calls) == [
            ["open" if sys.platform == "darwin" else "xdg-open", tmpfile]
        ]
        assert not hasattr(os, "startfile")


@pytest.mark.skipif(
    sys.platform in {"win32", "darwin"},
    reason="testing behavior specific to linux etc",
)
def test_fallback_success(mocked_openers, tmpfile):
    """Second attempted opener strategy for the platform should succeed."""
    mocked_openers.mock_processes({"xdg-open": False, "open": True})
    shopen.open(tmpfile, "open")
    assert list(mocked_openers.fp.calls) == [
        ["xdg-open", tmpfile],
        ["open", tmpfile],
    ]


def test_open_failed(monkeypatch, mocked_openers, tmpfile):
    monkeypatch.delattr(os, "startfile", raising=False)
    mocked_openers.mock_processes({"xdg-open": False, "open": False})
    with pytest.raises(OSError):
        shopen.open(tmpfile, "open")
    fp = mocked_openers.fp
    assert list(fp.calls) == [
        [cmd, tmpfile]
        for cmd in (
            []
            if sys.platform == "win32"
            else (
                ["open"] if sys.platform == "darwin" else ["xdg-open", "open"]
            )
        )
    ]


@pytest.mark.parametrize(
    "op_scenario",
    [
        OpScenario.NO_OPERATION,
        OpScenario.OPEN,
    ],
)
def test_default_op_open(mocked_openers, tmpfile, op_scenario: OpScenario):
    mocked_openers.mock_all()
    args, kw = op_scenario
    shopen.open(tmpfile, *args, **kw)
    fp = mocked_openers.fp
    if sys.platform == "win32":
        mocked_openers.os_startfile.assert_called_once_with(tmpfile, "open")
        assert not fp.calls
    else:
        assert list(fp.calls) == [
            ["open" if sys.platform == "darwin" else "xdg-open", tmpfile]
        ]
        assert not hasattr(os, "startfile")
