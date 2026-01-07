"""Handler for Deckbox CSV format."""

from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class DeckboxHandler(FormatHandler):
    """
    Handler for Deckbox CSV format.

    Deckbox export format:
    Count,Tradelist Count,Name,Edition,Card Number,Condition,Language,Foil,
    Signed,Artist Proof,Altered Art,Misprint,Promo,Textless,My Price

    Edition is the FULL SET NAME (not code).
    Foil is "foil" for foils, empty otherwise.
    """

    name: ClassVar[str] = "deckbox"
    display_name: ClassVar[str] = "Deckbox"
    required_columns: ClassVar[set[str]] = {"Count", "Name", "Edition"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Name"],
            set_name=row.get("Edition"),  # Deckbox uses full set names
            collector_number=row.get("Card Number"),
        )

        # Parse foil - Deckbox uses "foil" string
        foil_str = row.get("Foil", "").lower()
        finish = Finish.FOIL if foil_str == "foil" else Finish.NONFOIL

        # Parse condition
        condition = Condition.from_string(row.get("Condition"))

        # Parse language
        language = Language.from_string(row.get("Language"))

        # Trade quantity
        trade_qty_str = row.get("Tradelist Count", "")
        trade_quantity = int(trade_qty_str) if trade_qty_str else None

        # Extras
        extras = {}
        if row.get("My Price"):
            extras["my_price"] = row["My Price"]

        return CardEntry(
            card=card,
            quantity=int(row.get("Count", 1)),
            finish=finish,
            condition=condition,
            language=language,
            trade_quantity=trade_quantity,
            is_signed=row.get("Signed", "").lower() in ("signed", "true", "yes", "1"),
            is_altered=row.get("Altered Art", "").lower() in ("true", "yes", "1"),
            is_promo=row.get("Promo", "").lower() in ("true", "yes", "1"),
            extras=extras,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "foil" if entry.finish in (Finish.FOIL, Finish.ETCHED) else ""
        condition_str = entry.condition.value if entry.condition else ""

        return {
            "Count": str(entry.quantity),
            "Tradelist Count": str(entry.trade_quantity) if entry.trade_quantity else "",
            "Name": entry.card.name,
            "Edition": entry.card.set_name or "",
            "Card Number": entry.card.collector_number or "",
            "Condition": condition_str,
            "Language": entry.language.name.replace("_", " ").title(),
            "Foil": foil_str,
            "Signed": "signed" if entry.is_signed else "",
            "Artist Proof": "",
            "Altered Art": "true" if entry.is_altered else "",
            "Misprint": "",
            "Promo": "true" if entry.is_promo else "",
            "Textless": "",
            "My Price": entry.extras.get("my_price", ""),
        }

    def get_headers(self) -> list[str]:
        return [
            "Count",
            "Tradelist Count",
            "Name",
            "Edition",
            "Card Number",
            "Condition",
            "Language",
            "Foil",
            "Signed",
            "Artist Proof",
            "Altered Art",
            "Misprint",
            "Promo",
            "Textless",
            "My Price",
        ]
