"""Handler for TCGPlayer CSV format."""

from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class TCGPlayerHandler(FormatHandler):
    """
    Handler for TCGPlayer CSV format.

    TCGPlayer export format:
    Quantity,Name,Simple Name,Set,Card Number,Set Code,Printing,
    Condition,Language,Rarity,Product ID,SKU

    Printing: Normal, Foil
    """

    name: ClassVar[str] = "tcgplayer"
    display_name: ClassVar[str] = "TCGPlayer"
    required_columns: ClassVar[set[str]] = {"Quantity", "Name", "Set Code"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Name"],
            set_code=row.get("Set Code"),
            set_name=row.get("Set"),
            collector_number=row.get("Card Number"),
            rarity=row.get("Rarity"),
            tcgplayer_id=int(row["Product ID"]) if row.get("Product ID") else None,
        )

        # Parse foil from Printing field
        printing = row.get("Printing", "").lower()
        finish = Finish.FOIL if "foil" in printing else Finish.NONFOIL

        # Parse condition
        condition = Condition.from_string(row.get("Condition"))

        # Parse language
        language = Language.from_string(row.get("Language"))

        # Extras
        extras = {}
        if row.get("Simple Name"):
            extras["simple_name"] = row["Simple Name"]
        if row.get("SKU"):
            extras["sku"] = row["SKU"]

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
            condition=condition,
            language=language,
            extras=extras,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        printing = "Foil" if entry.finish in (Finish.FOIL, Finish.ETCHED) else "Normal"
        condition_str = entry.condition.value if entry.condition else ""

        return {
            "Quantity": str(entry.quantity),
            "Name": entry.card.name,
            "Simple Name": entry.extras.get("simple_name", entry.card.name),
            "Set": entry.card.set_name or "",
            "Card Number": entry.card.collector_number or "",
            "Set Code": entry.card.set_code or "",
            "Printing": printing,
            "Condition": condition_str,
            "Language": entry.language.name.replace("_", " ").title(),
            "Rarity": entry.card.rarity or "",
            "Product ID": str(entry.card.tcgplayer_id) if entry.card.tcgplayer_id else "",
            "SKU": entry.extras.get("sku", ""),
        }

    def get_headers(self) -> list[str]:
        return [
            "Quantity",
            "Name",
            "Simple Name",
            "Set",
            "Card Number",
            "Set Code",
            "Printing",
            "Condition",
            "Language",
            "Rarity",
            "Product ID",
            "SKU",
        ]
