"""Handler for Moxfield CSV format."""

from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class MoxfieldHandler(FormatHandler):
    """
    Handler for Moxfield CSV format.

    Moxfield export format:
    Count,Tradelist Count,Name,Edition,Condition,Language,Foil,Alter,Proxy,Purchase Price

    Edition is the set code (lowercase).
    """

    name: ClassVar[str] = "moxfield"
    display_name: ClassVar[str] = "Moxfield"
    required_columns: ClassVar[set[str]] = {"Count", "Name", "Edition"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Name"],
            set_code=row.get("Edition"),
        )

        # Parse foil
        foil_str = row.get("Foil", "")
        finish = Finish.from_string(foil_str)

        # Parse condition
        condition = Condition.from_string(row.get("Condition"))

        # Parse language
        language = Language.from_string(row.get("Language"))

        # Trade quantity
        trade_qty_str = row.get("Tradelist Count", "")
        trade_quantity = int(trade_qty_str) if trade_qty_str else None

        # Extras
        extras = {}
        if row.get("Proxy"):
            extras["proxy"] = row["Proxy"]

        return CardEntry(
            card=card,
            quantity=int(row.get("Count", 1)),
            finish=finish,
            condition=condition,
            language=language,
            trade_quantity=trade_quantity,
            is_altered=row.get("Alter", "").lower() in ("true", "yes", "1"),
            extras=extras,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "foil" if entry.finish in (Finish.FOIL, Finish.ETCHED) else ""
        condition_str = entry.condition.value if entry.condition else ""

        return {
            "Count": str(entry.quantity),
            "Tradelist Count": str(entry.trade_quantity) if entry.trade_quantity else "",
            "Name": entry.card.name,
            "Edition": entry.card.set_code or "",
            "Condition": condition_str,
            "Language": entry.language.value if entry.language != Language.ENGLISH else "English",
            "Foil": foil_str,
            "Alter": "true" if entry.is_altered else "",
            "Proxy": entry.extras.get("proxy", ""),
            "Purchase Price": str(entry.purchase_price) if entry.purchase_price else "",
        }

    def get_headers(self) -> list[str]:
        return [
            "Count",
            "Tradelist Count",
            "Name",
            "Edition",
            "Condition",
            "Language",
            "Foil",
            "Alter",
            "Proxy",
            "Purchase Price",
        ]
