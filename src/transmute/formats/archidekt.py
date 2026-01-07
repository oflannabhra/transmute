"""Handler for Archidekt CSV format."""

from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class ArchidektHandler(FormatHandler):
    """
    Handler for Archidekt CSV format.

    Archidekt is very flexible with column mapping. Common export format:
    Quantity,Name,Set Code,Set Name,Collector Number,Condition,Language,
    Foil,Scryfall ID

    They also support importing with just Scryfall ID for exact matching.
    """

    name: ClassVar[str] = "archidekt"
    display_name: ClassVar[str] = "Archidekt"
    required_columns: ClassVar[set[str]] = {"Quantity", "Name"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Name"],
            set_code=row.get("Set Code"),
            set_name=row.get("Set Name"),
            collector_number=row.get("Collector Number"),
            scryfall_id=row.get("Scryfall ID"),
        )

        # Parse foil
        foil_str = row.get("Foil", "")
        finish = Finish.from_string(foil_str)

        # Parse condition
        condition = Condition.from_string(row.get("Condition"))

        # Parse language
        language = Language.from_string(row.get("Language"))

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
            condition=condition,
            language=language,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "true" if entry.finish in (Finish.FOIL, Finish.ETCHED) else ""
        condition_str = entry.condition.value if entry.condition else ""

        return {
            "Quantity": str(entry.quantity),
            "Name": entry.card.name,
            "Set Code": entry.card.set_code or "",
            "Set Name": entry.card.set_name or "",
            "Collector Number": entry.card.collector_number or "",
            "Condition": condition_str,
            "Language": entry.language.value,
            "Foil": foil_str,
            "Scryfall ID": entry.card.scryfall_id or "",
        }

    def get_headers(self) -> list[str]:
        return [
            "Quantity",
            "Name",
            "Set Code",
            "Set Name",
            "Collector Number",
            "Condition",
            "Language",
            "Foil",
            "Scryfall ID",
        ]
