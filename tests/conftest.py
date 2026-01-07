"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to fixtures directory."""
    return FIXTURES_DIR


@pytest.fixture
def helvault_csv(fixtures_dir: Path) -> Path:
    """Return path to helvault sample CSV."""
    return fixtures_dir / "helvault.csv"


@pytest.fixture
def mtggoldfish_csv(fixtures_dir: Path) -> Path:
    """Return path to mtggoldfish sample CSV."""
    return fixtures_dir / "mtggoldfish.csv"
