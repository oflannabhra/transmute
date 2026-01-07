"""Handler for MTG Studio CSV format."""

from typing import ClassVar

from transmute.core.enums import Finish
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class MTGStudioHandler(FormatHandler):
    """
    Handler for MTG Studio CSV format.

    MTG Studio export format:
    Name,Edition,Qty,Foil

    Edition is the 3-letter set code.
    Foil should be "Yes" or "No".
    """

    name: ClassVar[str] = "mtgstudio"
    display_name: ClassVar[str] = "MTG Studio"
    required_columns: ClassVar[set[str]] = {"Name", "Edition", "Qty"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Name"],
            set_code=row.get("Edition"),
        )

        # Parse foil - Yes/No
        foil_str = row.get("Foil", "").lower()
        finish = Finish.FOIL if foil_str == "yes" else Finish.NONFOIL

        return CardEntry(
            card=card,
            quantity=int(row.get("Qty", 1)),
            finish=finish,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "Yes" if entry.finish in (Finish.FOIL, Finish.ETCHED) else "No"

        return {
            "Name": entry.card.name,
            "Edition": entry.card.set_code or "",
            "Qty": str(entry.quantity),
            "Foil": foil_str,
        }

    def get_headers(self) -> list[str]:
        return ["Name", "Edition", "Qty", "Foil"]
