"""Tests for MTGGoldfish format handler."""

from pathlib import Path

import pytest

from transmute.core.enums import Finish
from transmute.formats.mtggoldfish import MTGGoldfishHandler


@pytest.fixture
def handler() -> MTGGoldfishHandler:
    return MTGGoldfishHandler()


@pytest.fixture
def sample_row() -> dict[str, str]:
    return {
        "Card": "Goblin Arsonist",
        "Set ID": "m12",
        "Set Name": "Magic 2012",
        "Quantity": "4",
        "Foil": "True",
        "Variation": "",
    }


class TestMTGGoldfishHandler:
    def test_parse_row_basic(
        self, handler: MTGGoldfishHandler, sample_row: dict[str, str]
    ) -> None:
        entry = handler.parse_row(sample_row)

        assert entry.card.name == "Goblin Arsonist"
        assert entry.card.set_code == "m12"
        assert entry.card.set_name == "Magic 2012"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL

    def test_parse_row_nonfoil(
        self, handler: MTGGoldfishHandler, sample_row: dict[str, str]
    ) -> None:
        sample_row["Foil"] = "REGULAR"
        entry = handler.parse_row(sample_row)
        assert entry.finish == Finish.NONFOIL

    def test_parse_row_etched(
        self, handler: MTGGoldfishHandler, sample_row: dict[str, str]
    ) -> None:
        sample_row["Foil"] = "FOIL_ETCHED"
        entry = handler.parse_row(sample_row)
        assert entry.finish == Finish.ETCHED

    def test_format_row_foil(
        self, handler: MTGGoldfishHandler, sample_row: dict[str, str]
    ) -> None:
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)

        assert formatted["Card"] == "Goblin Arsonist"
        assert formatted["Quantity"] == "4"
        assert formatted["Foil"] == "FOIL"

    def test_format_row_regular(
        self, handler: MTGGoldfishHandler, sample_row: dict[str, str]
    ) -> None:
        sample_row["Foil"] = "False"
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)
        assert formatted["Foil"] == "REGULAR"

    def test_round_trip(
        self, handler: MTGGoldfishHandler, sample_row: dict[str, str]
    ) -> None:
        """Parsing then formatting should preserve data."""
        entry = handler.parse_row(sample_row)
        formatted = handler.format_row(entry)
        entry2 = handler.parse_row(formatted)

        assert entry.card.name == entry2.card.name
        assert entry.quantity == entry2.quantity
        assert entry.finish == entry2.finish

    def test_read_file(
        self, handler: MTGGoldfishHandler, mtggoldfish_csv: Path
    ) -> None:
        """Handler should read the sample file."""
        collection = handler.read(mtggoldfish_csv)

        assert len(collection) == 1
        entry = collection.entries[0]
        assert entry.card.name == "Goblin Arsonist"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL

    def test_detect_format(
        self, handler: MTGGoldfishHandler, mtggoldfish_csv: Path
    ) -> None:
        """Handler should detect its own format."""
        assert handler.detect(mtggoldfish_csv) is True

    def test_get_headers(self, handler: MTGGoldfishHandler) -> None:
        """Headers should be in correct order."""
        headers = handler.get_headers()
        assert headers[0] == "Card"
        assert "Quantity" in headers
        assert "Foil" in headers
