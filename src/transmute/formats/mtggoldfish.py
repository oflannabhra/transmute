"""Handler for MTGGoldfish CSV format."""

from typing import ClassVar

from transmute.core.enums import Finish
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class MTGGoldfishHandler(FormatHandler):
    """
    Handler for MTGGoldfish CSV format.

    MTGGoldfish format:
    Card,Set ID,Set Name,Quantity,Foil,Variation
    Goblin Arsonist,m12,Magic 2012,4,True,""

    Foil values: FOIL, REGULAR, FOIL_ETCHED, True, False
    """

    name: ClassVar[str] = "mtggoldfish"
    display_name: ClassVar[str] = "MTGGoldfish"
    required_columns: ClassVar[set[str]] = {"Card", "Set ID", "Quantity"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Card"],
            set_code=row.get("Set ID"),
            set_name=row.get("Set Name"),
        )

        # Parse foil - handles FOIL, REGULAR, FOIL_ETCHED, True, False
        foil_str = row.get("Foil", "").strip()
        finish = Finish.from_string(foil_str)

        # Store variation in extras if present
        variation = row.get("Variation", "")
        extras = {"variation": variation} if variation else {}

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
            extras=extras,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        if entry.finish == Finish.FOIL:
            foil_str = "FOIL"
        elif entry.finish == Finish.ETCHED:
            foil_str = "FOIL_ETCHED"
        else:
            foil_str = "REGULAR"

        return {
            "Card": entry.card.name,
            "Set ID": entry.card.set_code or "",
            "Set Name": entry.card.set_name or "",
            "Quantity": str(entry.quantity),
            "Foil": foil_str,
            "Variation": entry.extras.get("variation", ""),
        }

    def get_headers(self) -> list[str]:
        return ["Card", "Set ID", "Set Name", "Quantity", "Foil", "Variation"]
