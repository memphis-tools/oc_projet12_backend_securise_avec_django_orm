import pytest
from click.testing import CliRunner


@pytest.fixture
def get_runner():
    return CliRunner()
