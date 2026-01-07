"""Main converter for transforming between formats."""

from collections.abc import Callable
from pathlib import Path

from transmute.core.models import CardEntry, Collection
from transmute.formats import FormatRegistry
from transmute.scryfall.enrichment import CardEnricher


class Converter:
    """Main converter orchestrating the transformation between formats."""

    def __init__(
        self,
        use_scryfall: bool = False,
        on_progress: Callable[[str, int, int], None] | None = None,
        on_error: Callable[[CardEntry, Exception], None] | None = None,
    ) -> None:
        self.use_scryfall = use_scryfall
        self.on_progress = on_progress
        self.on_error = on_error
        self._enricher: CardEnricher | None = None

    @property
    def enricher(self) -> CardEnricher:
        if self._enricher is None:
            self._enricher = CardEnricher(
                on_progress=lambda cur, tot: self._report_progress("Enriching", cur, tot),
                on_error=self.on_error,
            )
        return self._enricher

    def _report_progress(self, stage: str, current: int, total: int) -> None:
        if self.on_progress:
            self.on_progress(stage, current, total)

    def convert(
        self,
        input_path: Path,
        output_path: Path,
        input_format: str | None = None,
        output_format: str | None = None,
    ) -> None:
        """
        Convert a collection file from one format to another.

        Args:
            input_path: Path to input CSV file
            output_path: Path to output CSV file
            input_format: Input format name (auto-detected if None)
            output_format: Output format name (required)

        Raises:
            ValueError: If input format cannot be detected or output format not specified
            FormatNotFoundError: If specified format is not registered
        """
        if output_format is None:
            raise ValueError("Output format must be specified")

        # Get handlers
        if input_format:
            in_handler = FormatRegistry.get(input_format)
        else:
            in_handler = FormatRegistry.detect_format(input_path)
            if in_handler is None:
                raise ValueError(f"Could not auto-detect format for {input_path}")

        out_handler = FormatRegistry.get(output_format)

        # Read input
        self._report_progress("Reading", 0, 1)
        collection = in_handler.read(input_path)
        self._report_progress("Reading", 1, 1)

        # Enrich with Scryfall data if requested
        if self.use_scryfall:
            collection = self.enricher.enrich_collection(collection)

        # Write output
        self._report_progress("Writing", 0, 1)
        out_handler.write(collection, output_path)
        self._report_progress("Writing", 1, 1)

    def convert_collection(
        self,
        collection: Collection,
        output_format: str,
    ) -> Collection:
        """
        Convert a collection to a different format representation.

        This doesn't write to a file, just transforms the data.
        Useful for programmatic usage.

        Args:
            collection: The collection to convert
            output_format: Target format name

        Returns:
            The same collection (possibly enriched)
        """
        # Enrich with Scryfall data if requested
        if self.use_scryfall:
            collection = self.enricher.enrich_collection(collection)

        return collection
