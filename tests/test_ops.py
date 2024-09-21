import pytest

import shopen


def test_empty(mocked_openers):
    mocked_openers.mock_all()
    with pytest.raises(TypeError):
        shopen.open()
    mocked_openers.verify_no_interactions()
