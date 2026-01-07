"""Handler for ManaBox CSV format."""

from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class ManaBoxHandler(FormatHandler):
    """
    Handler for ManaBox CSV format.

    ManaBox is flexible with columns but typically exports:
    Name,Set code,Set name,Collector number,Foil,Rarity,Quantity,
    ManaBox ID,Scryfall ID,Purchase price,Misprint,Altered,
    Condition,Language,Purchase price currency

    Required minimum: Name + (Set code OR Set name OR Scryfall ID)
    """

    name: ClassVar[str] = "manabox"
    display_name: ClassVar[str] = "ManaBox"
    required_columns: ClassVar[set[str]] = {"Name", "Quantity"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Name"],
            set_code=row.get("Set code"),
            set_name=row.get("Set name"),
            collector_number=row.get("Collector number"),
            scryfall_id=row.get("Scryfall ID"),
            rarity=row.get("Rarity"),
        )

        # Parse foil
        foil_str = row.get("Foil", "")
        finish = Finish.from_string(foil_str)

        # Parse condition
        condition = Condition.from_string(row.get("Condition"))

        # Parse language
        language = Language.from_string(row.get("Language"))

        # Extras
        extras = {}
        if row.get("ManaBox ID"):
            extras["manabox_id"] = row["ManaBox ID"]
        if row.get("Misprint"):
            extras["misprint"] = row["Misprint"]
        if row.get("Purchase price currency"):
            extras["currency"] = row["Purchase price currency"]

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
            condition=condition,
            language=language,
            is_altered=row.get("Altered", "").lower() in ("true", "yes", "1"),
            extras=extras,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "foil" if entry.finish in (Finish.FOIL, Finish.ETCHED) else ""
        condition_str = entry.condition.value if entry.condition else ""

        return {
            "Name": entry.card.name,
            "Set code": entry.card.set_code or "",
            "Set name": entry.card.set_name or "",
            "Collector number": entry.card.collector_number or "",
            "Foil": foil_str,
            "Rarity": entry.card.rarity or "",
            "Quantity": str(entry.quantity),
            "ManaBox ID": entry.extras.get("manabox_id", ""),
            "Scryfall ID": entry.card.scryfall_id or "",
            "Purchase price": str(entry.purchase_price) if entry.purchase_price else "",
            "Misprint": entry.extras.get("misprint", ""),
            "Altered": "true" if entry.is_altered else "",
            "Condition": condition_str,
            "Language": entry.language.value,
            "Purchase price currency": entry.extras.get("currency", ""),
        }

    def get_headers(self) -> list[str]:
        return [
            "Name",
            "Set code",
            "Set name",
            "Collector number",
            "Foil",
            "Rarity",
            "Quantity",
            "ManaBox ID",
            "Scryfall ID",
            "Purchase price",
            "Misprint",
            "Altered",
            "Condition",
            "Language",
            "Purchase price currency",
        ]
