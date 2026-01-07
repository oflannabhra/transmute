"""Handler for Helvault CSV format."""

from typing import ClassVar

from transmute.core.enums import Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class HelvaultHandler(FormatHandler):
    """
    Handler for Helvault CSV format.

    Helvault format:
    collector_number,extras,language,name,oracle_id,quantity,scryfall_id,set_code,set_name
    "136","foil","en","Goblin Arsonist","...","4","...","m12","Magic 2012"
    """

    name: ClassVar[str] = "helvault"
    display_name: ClassVar[str] = "Helvault"
    required_columns: ClassVar[set[str]] = {"name", "set_code", "quantity", "scryfall_id"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["name"],
            set_code=row.get("set_code"),
            set_name=row.get("set_name"),
            collector_number=row.get("collector_number"),
            scryfall_id=row.get("scryfall_id"),
            oracle_id=row.get("oracle_id"),
        )

        # Parse foil from "extras" field
        extras = row.get("extras", "").lower()
        finish = Finish.FOIL if "foil" in extras else Finish.NONFOIL

        # Parse language
        lang_str = row.get("language", "en")
        language = Language.from_string(lang_str)

        return CardEntry(
            card=card,
            quantity=int(row.get("quantity", 1)),
            finish=finish,
            language=language,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        extras = "foil" if entry.finish == Finish.FOIL else ""

        return {
            "collector_number": entry.card.collector_number or "",
            "extras": extras,
            "language": entry.language.value,
            "name": entry.card.name,
            "oracle_id": entry.card.oracle_id or "",
            "quantity": str(entry.quantity),
            "scryfall_id": entry.card.scryfall_id or "",
            "set_code": entry.card.set_code or "",
            "set_name": entry.card.set_name or "",
        }

    def get_headers(self) -> list[str]:
        return [
            "collector_number",
            "extras",
            "language",
            "name",
            "oracle_id",
            "quantity",
            "scryfall_id",
            "set_code",
            "set_name",
        ]
