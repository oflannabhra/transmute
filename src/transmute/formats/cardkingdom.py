"""Handler for Card Kingdom CSV format."""

from typing import ClassVar

from transmute.core.enums import Finish
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class CardKingdomHandler(FormatHandler):
    """
    Handler for Card Kingdom CSV format.

    Card Kingdom import format (for selling):
    Card Name,Edition,Foil,Quantity

    This is a simple 4-column format used for selling to Card Kingdom.
    Foil: 1/true/yes for foils, 0/false/no otherwise.
    Edition: Set code or set name.
    """

    name: ClassVar[str] = "cardkingdom"
    display_name: ClassVar[str] = "Card Kingdom"
    required_columns: ClassVar[set[str]] = {"Card Name", "Edition", "Quantity"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Card Name"],
            set_code=row.get("Edition"),  # Could be code or name
        )

        # Parse foil - accepts 1/true/yes or 0/false/no
        foil_str = row.get("Foil", "")
        finish = Finish.from_string(foil_str)

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "1" if entry.finish in (Finish.FOIL, Finish.ETCHED) else "0"

        return {
            "Card Name": entry.card.name,
            "Edition": entry.card.set_code or entry.card.set_name or "",
            "Foil": foil_str,
            "Quantity": str(entry.quantity),
        }

    def get_headers(self) -> list[str]:
        return ["Card Name", "Edition", "Foil", "Quantity"]
