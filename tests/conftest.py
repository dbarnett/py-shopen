import os
import pathlib
from dataclasses import dataclass
from typing import Dict, Optional
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture  # type: ignore
from pytest_subprocess.fake_process import FakeProcess  # type: ignore

from .testutil import no_such_command_callback


@dataclass
class OpenerMocker:
    mocker: MockerFixture
    fp: FakeProcess
    os_startfile: Optional[Mock] = None

    def mock_all(self):
        self.mock_processes()
        self.mock_os_startfile()

    def mock_os_startfile(self):
        if not hasattr(os, "startfile"):
            return None
        self.mocker.patch("os.startfile")
        self.os_startfile = os.startfile

    def mock_processes(self, commands: Optional[Dict[str, bool]] = None):
        if commands is None:
            commands = {c: True for c in ("xdg-open", "open", "editor")}
        for command, succeed in commands.items():
            callback = None if succeed else no_such_command_callback
            self.fp.register([command, self.fp.any()], callback=callback)

    def verify_no_interactions(self):
        if self.os_startfile:
            self.os_startfile.assert_not_called()
        assert not self.fp.calls


@pytest.fixture
def mocked_openers(mocker: MockerFixture, fp: FakeProcess) -> OpenerMocker:
    return OpenerMocker(mocker=mocker, fp=fp)


@pytest.fixture
def tmpfile(tmp_path: pathlib.Path):
    somefile = tmp_path.joinpath("somefile.txt")
    somefile.touch()
    return somefile
