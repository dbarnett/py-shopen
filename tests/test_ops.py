import pytest

import shopen


def test_empty(mocked_openers):
    mocked_openers.mock_all()
    with pytest.raises(TypeError):
        shopen.open()
    mocked_openers.verify_no_interactions()


def test_nonexistent_op(mocked_openers, tmpfile):
    with pytest.raises(ValueError):
        shopen.open(tmpfile, "nonexistent-operation")
    mocked_openers.verify_no_interactions()
