"""Tests for the converter module."""

from pathlib import Path

import pytest

from transmute.converter import Converter
from transmute.core.enums import Finish


class TestConverter:
    def test_convert_helvault_to_mtggoldfish(
        self, helvault_csv: Path, tmp_path: Path
    ) -> None:
        """Convert Helvault format to MTGGoldfish format."""
        output_file = tmp_path / "output.csv"

        converter = Converter()
        converter.convert(
            input_path=helvault_csv,
            output_path=output_file,
            input_format="helvault",
            output_format="mtggoldfish",
        )

        assert output_file.exists()

        # Read back and verify
        from transmute.formats.mtggoldfish import MTGGoldfishHandler

        handler = MTGGoldfishHandler()
        collection = handler.read(output_file)

        assert len(collection) == 1
        entry = collection.entries[0]
        assert entry.card.name == "Goblin Arsonist"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL

    def test_convert_mtggoldfish_to_helvault(
        self, mtggoldfish_csv: Path, tmp_path: Path
    ) -> None:
        """Convert MTGGoldfish format to Helvault format."""
        output_file = tmp_path / "output.csv"

        converter = Converter()
        converter.convert(
            input_path=mtggoldfish_csv,
            output_path=output_file,
            input_format="mtggoldfish",
            output_format="helvault",
        )

        assert output_file.exists()

        # Read back and verify
        from transmute.formats.helvault import HelvaultHandler

        handler = HelvaultHandler()
        collection = handler.read(output_file)

        assert len(collection) == 1
        entry = collection.entries[0]
        assert entry.card.name == "Goblin Arsonist"
        assert entry.quantity == 4
        assert entry.finish == Finish.FOIL

    def test_convert_with_autodetect(
        self, helvault_csv: Path, tmp_path: Path
    ) -> None:
        """Convert with auto-detected input format."""
        output_file = tmp_path / "output.csv"

        converter = Converter()
        converter.convert(
            input_path=helvault_csv,
            output_path=output_file,
            input_format=None,  # Auto-detect
            output_format="mtggoldfish",
        )

        assert output_file.exists()

    def test_convert_requires_output_format(
        self, helvault_csv: Path, tmp_path: Path
    ) -> None:
        """Convert should raise error without output format."""
        output_file = tmp_path / "output.csv"

        converter = Converter()
        with pytest.raises(ValueError, match="Output format must be specified"):
            converter.convert(
                input_path=helvault_csv,
                output_path=output_file,
                output_format=None,
            )
