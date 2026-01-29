"""Tests for Archidekt format handler."""

from pathlib import Path

import pytest

from transmute.core.enums import Condition, Finish
from transmute.formats.archidekt import ArchidektHandler


@pytest.fixture
def handler() -> ArchidektHandler:
    return ArchidektHandler()


@pytest.fixture
def sample_row() -> dict[str, str]:
    return {
        "Quantity": "4",
        "Name": "Goblin Arsonist",
        "Set Code": "m12",
        "Set Name": "Magic 2012",
        "Collector Number": "136",
        "Condition": "NM",
        "Language": "en",
        "Foil": "true",
        "Scryfall ID": "c24751fd-5e9b-4d7d-83ba-e306b439bbe1",
        "Oracle ID": "c1177f22-a1cf-4da3-a68d-ff954e878403",
    }


class TestArchidektHandler:
    def test_parse_row_basic(self, handler: ArchidektHandler, sample_row: dict[str, str]) -> None:
        entry = handler.parse_row(sample_row)

        assert entry.card.name == "Goblin Arsonist"
        assert entry.card.set_code == "m12"
        assert entry.card.set_name == "Magic 2012"
        assert entry.card.collector_number == "136"
        assert entry.card.scryfall_id == "c24751fd-5e9b-4d7d-83ba-e306b439bbe1"
        assert entry.card.oracle_id == "c1177f22-a1cf-4da3-a68d-ff954e878403"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL
        assert entry.condition == Condition.NEAR_MINT

    def test_parse_row_nonfoil(self, handler: ArchidektHandler, sample_row: dict[str, str]) -> None:
        sample_row["Foil"] = "false"
        entry = handler.parse_row(sample_row)
        assert entry.finish == Finish.NONFOIL

    def test_format_row(self, handler: ArchidektHandler, sample_row: dict[str, str]) -> None:
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)

        assert formatted["Name"] == "Goblin Arsonist"
        assert formatted["Quantity"] == "4"
        assert formatted["Set Code"] == "m12"
        assert formatted["Collector Number"] == "136"
        assert formatted["Scryfall ID"] == "c24751fd-5e9b-4d7d-83ba-e306b439bbe1"
        assert formatted["Oracle ID"] == "c1177f22-a1cf-4da3-a68d-ff954e878403"

    def test_round_trip(self, handler: ArchidektHandler, sample_row: dict[str, str]) -> None:
        """Parsing then formatting should preserve data."""
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)
        entry2 = handler.parse_row(formatted)

        assert entry.card.name == entry2.card.name
        assert entry.card.collector_number == entry2.card.collector_number
        assert entry.card.scryfall_id == entry2.card.scryfall_id
        assert entry.card.oracle_id == entry2.card.oracle_id
        assert entry.quantity == entry2.quantity
        assert entry.finish == entry2.finish

    def test_read_file(self, handler: ArchidektHandler, archidekt_csv: Path) -> None:
        """Handler should read the sample file."""
        collection = handler.read(archidekt_csv)

        assert len(collection) == 1
        entry = collection.entries[0]
        assert entry.card.name == "Goblin Arsonist"
        assert entry.card.collector_number == "136"
        assert entry.card.scryfall_id == "c24751fd-5e9b-4d7d-83ba-e306b439bbe1"
        assert entry.card.oracle_id == "c1177f22-a1cf-4da3-a68d-ff954e878403"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL

    def test_detect_format(self, handler: ArchidektHandler, archidekt_csv: Path) -> None:
        """Handler should detect its own format."""
        assert handler.detect(archidekt_csv) is True

    def test_get_headers(self, handler: ArchidektHandler) -> None:
        """Headers should be in correct order."""
        headers = handler.get_headers()
        assert headers[0] == "Quantity"
        assert "Name" in headers
        assert "Scryfall ID" in headers
        assert "Oracle ID" in headers
