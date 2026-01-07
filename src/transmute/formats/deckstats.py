"""Handler for Deckstats CSV format."""

from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class DeckstatsHandler(FormatHandler):
    """
    Handler for Deckstats CSV format.

    Deckstats export format:
    amount,card_name,is_foil,is_pinned,set_id,set_code,language,condition,comment

    is_foil: 0 or 1
    is_pinned: 0 or 1 (for tracking specific printings)
    """

    name: ClassVar[str] = "deckstats"
    display_name: ClassVar[str] = "Deckstats"
    required_columns: ClassVar[set[str]] = {"amount", "card_name"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["card_name"],
            set_code=row.get("set_code"),
        )

        # Store set_id in extras if present
        extras = {}
        if row.get("set_id"):
            extras["set_id"] = row["set_id"]
        if row.get("comment"):
            extras["comment"] = row["comment"]

        # Parse foil - 0 or 1
        foil_str = row.get("is_foil", "0")
        finish = Finish.FOIL if foil_str == "1" else Finish.NONFOIL

        # Parse condition
        condition = Condition.from_string(row.get("condition"))

        # Parse language
        language = Language.from_string(row.get("language"))

        # Track pinned status
        if row.get("is_pinned") == "1":
            extras["is_pinned"] = "1"

        return CardEntry(
            card=card,
            quantity=int(row.get("amount", 1)),
            finish=finish,
            condition=condition,
            language=language,
            extras=extras,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "1" if entry.finish in (Finish.FOIL, Finish.ETCHED) else "0"
        condition_str = entry.condition.value if entry.condition else ""

        return {
            "amount": str(entry.quantity),
            "card_name": entry.card.name,
            "is_foil": foil_str,
            "is_pinned": entry.extras.get("is_pinned", "0"),
            "set_id": entry.extras.get("set_id", ""),
            "set_code": entry.card.set_code or "",
            "language": entry.language.value if entry.language != Language.ENGLISH else "",
            "condition": condition_str,
            "comment": entry.extras.get("comment", ""),
        }

    def get_headers(self) -> list[str]:
        return [
            "amount",
            "card_name",
            "is_foil",
            "is_pinned",
            "set_id",
            "set_code",
            "language",
            "condition",
            "comment",
        ]
