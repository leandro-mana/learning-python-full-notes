"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_list() -> list[int]:
    """Fixture providing a sample list."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def sample_dict() -> dict[str, int]:
    """Fixture providing a sample dictionary."""
    return {"a": 1, "b": 2, "c": 3}
