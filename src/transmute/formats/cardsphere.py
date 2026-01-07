"""Handler for Cardsphere CSV format."""

from typing import ClassVar

from transmute.core.enums import Condition, Finish
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class CardsphereHandler(FormatHandler):
    """
    Handler for Cardsphere CSV format.

    Cardsphere export format for Haves:
    Name,Set,Condition,Language,Foil,Quantity,Scryfall ID

    They use CSID (Cardsphere ID) internally and support Scryfall ID for imports.
    """

    name: ClassVar[str] = "cardsphere"
    display_name: ClassVar[str] = "Cardsphere"
    required_columns: ClassVar[set[str]] = {"Name", "Set", "Quantity"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Name"],
            set_code=row.get("Set"),
            scryfall_id=row.get("Scryfall ID"),
        )

        # Parse foil
        foil_str = row.get("Foil", "")
        finish = Finish.from_string(foil_str)

        # Parse condition - Cardsphere uses NM, LP, MP, HP, D
        condition = Condition.from_string(row.get("Condition"))

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
            condition=condition,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "Foil" if entry.finish in (Finish.FOIL, Finish.ETCHED) else ""
        condition_str = entry.condition.value if entry.condition else "NM"

        return {
            "Name": entry.card.name,
            "Set": entry.card.set_code or "",
            "Condition": condition_str,
            "Language": entry.language.value,
            "Foil": foil_str,
            "Quantity": str(entry.quantity),
            "Scryfall ID": entry.card.scryfall_id or "",
        }

    def get_headers(self) -> list[str]:
        return [
            "Name",
            "Set",
            "Condition",
            "Language",
            "Foil",
            "Quantity",
            "Scryfall ID",
        ]
