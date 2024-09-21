import sys

import pytest

import shopen


def test_empty(mocked_openers):
    mocked_openers.mock_all()
    with pytest.raises(TypeError):
        shopen.open(operation="edit")
    mocked_openers.verify_no_interactions()


def test_simple_success(mocked_openers, tmpfile):
    mocked_openers.mock_all()
    shopen.open(tmpfile, "edit")
    if sys.platform == "win32":
        mocked_openers.os_startfile.assert_called_once_with(tmpfile, "edit")
        assert not mocked_openers.fp.calls
    else:
        assert ["editor", tmpfile] in mocked_openers.fp.calls


@pytest.mark.skipif(
    sys.platform == "win32", reason="testing non-Windows env scenario"
)
def test_plat_nonwindows_env(mocked_openers, tmpfile, monkeypatch):
    mocked_openers.mock_os_startfile()
    mocked_openers.mock_processes({"editor": False, "someeditor": True})
    monkeypatch.setenv("EDITOR", "someeditor")
    shopen.open(tmpfile, "edit")
    assert ["someeditor", tmpfile] in mocked_openers.fp.calls


@pytest.mark.skipif(
    sys.platform in {"win32", "darwin"},
    reason="testing platform-specific behavior for linux, etc",
)
def test_plat_nonwindows_xdg_open(mocked_openers, tmpfile, monkeypatch):
    mocked_openers.mock_processes({"editor": False, "xdg-open": True})
    monkeypatch.delenv("EDITOR", raising=False)
    shopen.open(tmpfile, "edit")
    assert ["xdg-open", tmpfile] in mocked_openers.fp.calls


@pytest.mark.skipif(
    sys.platform == "win32", reason="testing non-Windows scenarios"
)
def test_plat_nonwindows_open(mocked_openers, tmpfile, monkeypatch):
    mocked_openers.mock_processes(
        {"editor": False, "xdg-open": False, "open": True}
    )
    monkeypatch.delenv("EDITOR", raising=False)
    shopen.open(tmpfile, "edit")
    assert ["open", tmpfile] in mocked_openers.fp.calls
