"""Tests for Helvault format handler."""

from pathlib import Path

import pytest

from transmute.core.enums import Finish, Language
from transmute.formats.helvault import HelvaultHandler


@pytest.fixture
def handler() -> HelvaultHandler:
    return HelvaultHandler()


@pytest.fixture
def sample_row() -> dict[str, str]:
    return {
        "collector_number": "136",
        "extras": "foil",
        "language": "en",
        "name": "Goblin Arsonist",
        "oracle_id": "c1177f22-a1cf-4da3-a68d-ff954e878403",
        "quantity": "4",
        "scryfall_id": "c24751fd-5e9b-4d7d-83ba-e306b439bbe1",
        "set_code": "m12",
        "set_name": "Magic 2012",
    }


class TestHelvaultHandler:
    def test_parse_row_basic(
        self, handler: HelvaultHandler, sample_row: dict[str, str]
    ) -> None:
        entry = handler.parse_row(sample_row)

        assert entry.card.name == "Goblin Arsonist"
        assert entry.card.set_code == "m12"
        assert entry.card.set_name == "Magic 2012"
        assert entry.card.collector_number == "136"
        assert entry.card.scryfall_id == "c24751fd-5e9b-4d7d-83ba-e306b439bbe1"
        assert entry.card.oracle_id == "c1177f22-a1cf-4da3-a68d-ff954e878403"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL
        assert entry.language == Language.ENGLISH

    def test_parse_row_nonfoil(
        self, handler: HelvaultHandler, sample_row: dict[str, str]
    ) -> None:
        sample_row["extras"] = ""
        entry = handler.parse_row(sample_row)
        assert entry.finish == Finish.NONFOIL

    def test_format_row(
        self, handler: HelvaultHandler, sample_row: dict[str, str]
    ) -> None:
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)

        assert formatted["name"] == "Goblin Arsonist"
        assert formatted["quantity"] == "4"
        assert formatted["extras"] == "foil"
        assert formatted["set_code"] == "m12"

    def test_round_trip(
        self, handler: HelvaultHandler, sample_row: dict[str, str]
    ) -> None:
        """Parsing then formatting should preserve data."""
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)
        entry2 = handler.parse_row(formatted)

        assert entry.card.name == entry2.card.name
        assert entry.quantity == entry2.quantity
        assert entry.finish == entry2.finish

    def test_read_file(self, handler: HelvaultHandler, helvault_csv: Path) -> None:
        """Handler should read the sample file."""
        collection = handler.read(helvault_csv)

        assert len(collection) == 1
        entry = collection.entries[0]
        assert entry.card.name == "Goblin Arsonist"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL

    def test_detect_format(self, handler: HelvaultHandler, helvault_csv: Path) -> None:
        """Handler should detect its own format."""
        assert handler.detect(helvault_csv) is True

    def test_get_headers(self, handler: HelvaultHandler) -> None:
        """Headers should be in correct order."""
        headers = handler.get_headers()
        assert headers[0] == "collector_number"
        assert "name" in headers
        assert "quantity" in headers
