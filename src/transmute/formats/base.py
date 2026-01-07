"""Base class for format handlers."""

import csv
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar

from transmute.core.models import CardEntry, Collection


class FormatHandler(ABC):
    """
    Abstract base class for CSV format handlers.

    Each format must implement:
    - name: Short identifier (e.g., "helvault")
    - display_name: Human-readable name (e.g., "Helvault")
    - required_columns: Columns that must be present for detection
    - parse_row(): Convert a CSV row to CardEntry
    - format_row(): Convert a CardEntry to CSV row dict
    - get_headers(): Return column headers for writing
    """

    # Class attributes to override
    name: ClassVar[str]
    display_name: ClassVar[str]
    file_extensions: ClassVar[list[str]] = [".csv"]
    required_columns: ClassVar[set[str]]

    # CSV dialect settings (can be overridden)
    delimiter: ClassVar[str] = ","
    quotechar: ClassVar[str] = '"'
    quoting: ClassVar[int] = csv.QUOTE_MINIMAL

    @abstractmethod
    def parse_row(self, row: dict[str, str]) -> CardEntry:
        """
        Parse a single CSV row into a CardEntry.

        Args:
            row: Dictionary from csv.DictReader

        Returns:
            CardEntry with as much data as can be extracted
        """

    @abstractmethod
    def format_row(self, entry: CardEntry) -> dict[str, str]:
        """
        Format a CardEntry as a CSV row dictionary.

        Args:
            entry: The card entry to format

        Returns:
            Dictionary mapping column names to values
        """

    @abstractmethod
    def get_headers(self) -> list[str]:
        """Return ordered list of column headers for output."""

    def read(self, file_path: Path) -> Collection:
        """
        Read a CSV file and return a Collection.

        This default implementation handles standard CSV reading.
        Override for formats with special requirements.
        """
        collection = Collection(source_format=self.name)

        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(
                f,
                delimiter=self.delimiter,
                quotechar=self.quotechar,
            )

            for row in reader:
                entry = self.parse_row(row)
                collection.add(entry)

        return collection

    def write(self, collection: Collection, file_path: Path) -> None:
        """
        Write a Collection to a CSV file.

        This default implementation handles standard CSV writing.
        Override for formats with special requirements.
        """
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=self.get_headers(),
                delimiter=self.delimiter,
                quotechar=self.quotechar,
                quoting=self.quoting,
            )

            writer.writeheader()
            for entry in collection:
                row = self.format_row(entry)
                writer.writerow(row)

    def can_read(self, file_path: Path) -> bool:
        """Check if this handler can read the given file by extension."""
        return file_path.suffix.lower() in self.file_extensions

    def detect(self, file_path: Path) -> bool:
        """
        Attempt to detect if a file matches this format.

        Default implementation checks for required columns in header.
        """
        if not self.can_read(file_path):
            return False

        try:
            with open(file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=self.delimiter)
                headers = set(reader.fieldnames or [])
                return self.required_columns.issubset(headers)
        except Exception:
            return False
