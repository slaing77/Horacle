import pytest
from unittest.mock import patch

@pytest.fixture
def mock_requests_post():
    with patch("requests.post") as mock_post:
        yield mock_post

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get
