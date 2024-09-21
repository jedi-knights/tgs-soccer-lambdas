# tests/conftest.py
import logging
import pytest

@pytest.fixture
def test_logger():
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.write("\n")