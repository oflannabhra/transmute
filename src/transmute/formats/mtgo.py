"""Handler for Magic Online (MTGO) CSV format."""

import contextlib
from typing import ClassVar

from transmute.core.enums import Finish
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class MTGOHandler(FormatHandler):
    """
    Handler for Magic Online (MTGO) CSV format.

    MTGO export format:
    Card Name,Quantity,ID #,Rarity,Set,Collector #,Premium

    Premium is "Yes" for foils.
    ID #, Rarity, Collector # are optional.
    Set is the 3-letter set code.
    """

    name: ClassVar[str] = "mtgo"
    display_name: ClassVar[str] = "MTGO"
    required_columns: ClassVar[set[str]] = {"Card Name", "Quantity"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        # Parse MTGO ID
        mtgo_id = None
        id_str = row.get("ID #", "")
        if id_str:
            with contextlib.suppress(ValueError):
                mtgo_id = int(id_str)

        card = Card(
            name=row["Card Name"],
            set_code=row.get("Set"),
            collector_number=row.get("Collector #"),
            rarity=row.get("Rarity"),
            mtgo_id=mtgo_id,
        )

        # Parse premium (foil)
        premium = row.get("Premium", "").lower()
        finish = Finish.FOIL if premium == "yes" else Finish.NONFOIL

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        premium = "Yes" if entry.finish in (Finish.FOIL, Finish.ETCHED) else "No"

        return {
            "Card Name": entry.card.name,
            "Quantity": str(entry.quantity),
            "ID #": str(entry.card.mtgo_id) if entry.card.mtgo_id else "",
            "Rarity": entry.card.rarity or "",
            "Set": entry.card.set_code or "",
            "Collector #": entry.card.collector_number or "",
            "Premium": premium,
        }

    def get_headers(self) -> list[str]:
        return [
            "Card Name",
            "Quantity",
            "ID #",
            "Rarity",
            "Set",
            "Collector #",
            "Premium",
        ]
