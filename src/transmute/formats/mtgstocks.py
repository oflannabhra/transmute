"""Handler for MTGStocks CSV format."""

from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class MTGStocksHandler(FormatHandler):
    """
    Handler for MTGStocks CSV format.

    MTGStocks export format:
    "Card","Set","Quantity","Price","Condition","Language","Foil","Signed"

    Foil: "Yes" or "No"
    Condition: M, NM, LP, MP, HP, D
    Language: en, de, fr, etc.
    """

    name: ClassVar[str] = "mtgstocks"
    display_name: ClassVar[str] = "MTGStocks"
    required_columns: ClassVar[set[str]] = {"Card", "Set", "Quantity"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Card"],
            set_name=row.get("Set"),  # MTGStocks uses full set names
        )

        # Parse foil - Yes/No
        foil_str = row.get("Foil", "").lower()
        finish = Finish.FOIL if foil_str == "yes" else Finish.NONFOIL

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
            is_signed=row.get("Signed", "").lower() == "yes",
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "Yes" if entry.finish in (Finish.FOIL, Finish.ETCHED) else "No"
        condition_str = entry.condition.value if entry.condition else "M"

        return {
            "Card": entry.card.name,
            "Set": entry.card.set_name or entry.card.set_code or "",
            "Quantity": str(entry.quantity),
            "Price": str(entry.purchase_price) if entry.purchase_price else "0.00",
            "Condition": condition_str,
            "Language": entry.language.value,
            "Foil": foil_str,
            "Signed": "Yes" if entry.is_signed else "No",
        }

    def get_headers(self) -> list[str]:
        return [
            "Card",
            "Set",
            "Quantity",
            "Price",
            "Condition",
            "Language",
            "Foil",
            "Signed",
        ]
