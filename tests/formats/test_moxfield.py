"""Tests for Moxfield format handler."""

from pathlib import Path

import pytest

from transmute.core.enums import Condition, Finish, Language
from transmute.formats.moxfield import MoxfieldHandler


@pytest.fixture
def handler() -> MoxfieldHandler:
    return MoxfieldHandler()


@pytest.fixture
def sample_row() -> dict[str, str]:
    return {
        "Count": "4",
        "Tradelist Count": "2",
        "Name": "Goblin Arsonist",
        "Edition": "m12",
        "Condition": "NM",
        "Language": "English",
        "Foil": "foil",
        "Alter": "",
        "Proxy": "",
        "Purchase Price": "5.99",
        "Collector Number": "136",
    }


class TestMoxfieldHandler:
    def test_parse_row_basic(self, handler: MoxfieldHandler, sample_row: dict[str, str]) -> None:
        entry = handler.parse_row(sample_row)

        assert entry.card.name == "Goblin Arsonist"
        assert entry.card.set_code == "m12"
        assert entry.card.collector_number == "136"
        assert entry.quantity == 4
        assert entry.trade_quantity == 2
        assert entry.finish == Finish.FOIL
        assert entry.condition == Condition.NEAR_MINT
        assert entry.language == Language.ENGLISH

    def test_parse_row_nonfoil(self, handler: MoxfieldHandler, sample_row: dict[str, str]) -> None:
        sample_row["Foil"] = ""
        entry = handler.parse_row(sample_row)
        assert entry.finish == Finish.NONFOIL

    def test_format_row(self, handler: MoxfieldHandler, sample_row: dict[str, str]) -> None:
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)

        assert formatted["Name"] == "Goblin Arsonist"
        assert formatted["Count"] == "4"
        assert formatted["Tradelist Count"] == "2"
        assert formatted["Edition"] == "m12"
        assert formatted["Foil"] == "foil"
        assert formatted["Collector Number"] == "136"

    def test_round_trip(self, handler: MoxfieldHandler, sample_row: dict[str, str]) -> None:
        """Parsing then formatting should preserve data."""
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)
        entry2 = handler.parse_row(formatted)

        assert entry.card.name == entry2.card.name
        assert entry.card.collector_number == entry2.card.collector_number
        assert entry.quantity == entry2.quantity
        assert entry.finish == entry2.finish

    def test_read_file(self, handler: MoxfieldHandler, moxfield_csv: Path) -> None:
        """Handler should read the sample file."""
        collection = handler.read(moxfield_csv)

        assert len(collection) == 1
        entry = collection.entries[0]
        assert entry.card.name == "Goblin Arsonist"
        assert entry.card.collector_number == "136"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL

    def test_detect_format(self, handler: MoxfieldHandler, moxfield_csv: Path) -> None:
        """Handler should detect its own format."""
        assert handler.detect(moxfield_csv) is True

    def test_get_headers(self, handler: MoxfieldHandler) -> None:
        """Headers should be in correct order."""
        headers = handler.get_headers()
        assert headers[0] == "Count"
        assert "Name" in headers
        assert "Edition" in headers
        assert "Collector Number" in headers
