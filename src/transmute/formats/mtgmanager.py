"""Handler for MTG Manager CSV format."""

import contextlib
from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class MTGManagerHandler(FormatHandler):
    """
    Handler for MTG Manager CSV format.

    MTG Manager export format:
    Quantity,Name,Code,PurchasePrice,Foil,Condition,Language,PurchaseDate

    Foil: 0 or 1
    Condition: 0 (Mint) to 5 (Damaged) - numeric scale
    Language: 0 (English), 1 (German), etc. - numeric codes
    Code: 3-letter set code
    """

    name: ClassVar[str] = "mtgmanager"
    display_name: ClassVar[str] = "MTG Manager"
    required_columns: ClassVar[set[str]] = {"Quantity", "Name", "Code"}

    # MTG Manager uses numeric codes for condition
    CONDITION_MAP = {
        "0": Condition.MINT,
        "1": Condition.NEAR_MINT,
        "2": Condition.LIGHTLY_PLAYED,
        "3": Condition.MODERATELY_PLAYED,
        "4": Condition.HEAVILY_PLAYED,
        "5": Condition.DAMAGED,
    }

    CONDITION_REVERSE = {v: k for k, v in CONDITION_MAP.items()}

    # MTG Manager uses numeric codes for language
    LANGUAGE_MAP = {
        "0": Language.ENGLISH,
        "1": Language.GERMAN,
        "2": Language.FRENCH,
        "3": Language.ITALIAN,
        "4": Language.SPANISH,
        "5": Language.PORTUGUESE,
        "6": Language.JAPANESE,
        "7": Language.SIMPLIFIED_CHINESE,
        "8": Language.RUSSIAN,
        "9": Language.KOREAN,
    }

    LANGUAGE_REVERSE = {v: k for k, v in LANGUAGE_MAP.items()}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Name"],
            set_code=row.get("Code"),
        )

        # Parse foil - 0 or 1
        foil_str = row.get("Foil", "0")
        finish = Finish.FOIL if foil_str == "1" else Finish.NONFOIL

        # Parse condition - numeric
        condition_str = row.get("Condition", "")
        condition = self.CONDITION_MAP.get(condition_str)

        # Parse language - numeric
        language_str = row.get("Language", "0")
        language = self.LANGUAGE_MAP.get(language_str, Language.ENGLISH)

        # Purchase price
        price_str = row.get("PurchasePrice", "")
        purchase_price = Decimal(price_str) if price_str else None

        # Purchase date - format: M/D/YYYY
        date_str = row.get("PurchaseDate", "")
        purchase_date = None
        if date_str:
            try:
                purchase_date = datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                with contextlib.suppress(ValueError):
                    purchase_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
            condition=condition,
            language=language,
            purchase_price=purchase_price,
            purchase_date=purchase_date,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        foil_str = "1" if entry.finish in (Finish.FOIL, Finish.ETCHED) else "0"

        # Convert condition to numeric
        condition_str = ""
        if entry.condition:
            condition_str = self.CONDITION_REVERSE.get(entry.condition, "")

        # Convert language to numeric
        language_str = self.LANGUAGE_REVERSE.get(entry.language, "0")

        # Format date as M/D/YYYY
        date_str = ""
        if entry.purchase_date:
            date_str = entry.purchase_date.strftime("%-m/%-d/%Y")

        return {
            "Quantity": str(entry.quantity),
            "Name": entry.card.name,
            "Code": entry.card.set_code or "",
            "PurchasePrice": str(entry.purchase_price) if entry.purchase_price else "",
            "Foil": foil_str,
            "Condition": condition_str,
            "Language": language_str,
            "PurchaseDate": date_str,
        }

    def get_headers(self) -> list[str]:
        return [
            "Quantity",
            "Name",
            "Code",
            "PurchasePrice",
            "Foil",
            "Condition",
            "Language",
            "PurchaseDate",
        ]
