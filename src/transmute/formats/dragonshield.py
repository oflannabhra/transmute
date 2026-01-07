"""Handler for DragonShield MTG Card Manager CSV format."""

import contextlib
from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from transmute.core.enums import Condition, Finish, Language
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class DragonShieldHandler(FormatHandler):
    """
    Handler for DragonShield MTG Card Manager CSV format.

    DragonShield export format:
    Folder Name,Quantity,Trade Quantity,Card Name,Set Code,Set Name,
    Card Number,Condition,Printing,Language,Price Bought,Date Bought,
    LOW,MID,MARKET

    Printing: Normal, Foil
    """

    name: ClassVar[str] = "dragonshield"
    display_name: ClassVar[str] = "DragonShield"
    required_columns: ClassVar[set[str]] = {"Card Name", "Set Code", "Quantity"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        card = Card(
            name=row["Card Name"],
            set_code=row.get("Set Code"),
            set_name=row.get("Set Name"),
            collector_number=row.get("Card Number"),
        )

        # Parse foil from Printing field
        printing = row.get("Printing", "").lower()
        finish = Finish.FOIL if "foil" in printing else Finish.NONFOIL

        # Parse condition - DragonShield uses "NearMint" style
        condition_str = row.get("Condition", "")
        # Normalize "NearMint" -> "Near Mint"
        condition_str = condition_str.replace("NearMint", "Near Mint")
        condition_str = condition_str.replace("LightlyPlayed", "Lightly Played")
        condition_str = condition_str.replace("ModeratelyPlayed", "Moderately Played")
        condition_str = condition_str.replace("HeavilyPlayed", "Heavily Played")
        condition = Condition.from_string(condition_str)

        # Parse language
        language = Language.from_string(row.get("Language"))

        # Trade quantity
        trade_qty_str = row.get("Trade Quantity", "")
        trade_quantity = int(trade_qty_str) if trade_qty_str else None

        # Purchase price
        price_str = row.get("Price Bought", "")
        purchase_price = Decimal(price_str) if price_str else None

        # Purchase date
        date_str = row.get("Date Bought", "")
        purchase_date = None
        if date_str:
            with contextlib.suppress(ValueError):
                purchase_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Extras
        extras = {}
        if row.get("Folder Name"):
            extras["folder"] = row["Folder Name"]
        if row.get("LOW"):
            extras["price_low"] = row["LOW"]
        if row.get("MID"):
            extras["price_mid"] = row["MID"]
        if row.get("MARKET"):
            extras["price_market"] = row["MARKET"]

        return CardEntry(
            card=card,
            quantity=int(row.get("Quantity", 1)),
            finish=finish,
            condition=condition,
            language=language,
            trade_quantity=trade_quantity,
            purchase_price=purchase_price,
            purchase_date=purchase_date,
            extras=extras,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        printing = "Foil" if entry.finish in (Finish.FOIL, Finish.ETCHED) else "Normal"

        # DragonShield uses "NearMint" style
        condition_str = ""
        if entry.condition:
            condition_map = {
                Condition.MINT: "Mint",
                Condition.NEAR_MINT: "NearMint",
                Condition.LIGHTLY_PLAYED: "LightlyPlayed",
                Condition.MODERATELY_PLAYED: "ModeratelyPlayed",
                Condition.HEAVILY_PLAYED: "HeavilyPlayed",
                Condition.DAMAGED: "Damaged",
            }
            condition_str = condition_map.get(entry.condition, "")

        date_str = ""
        if entry.purchase_date:
            date_str = entry.purchase_date.strftime("%Y-%m-%d")

        return {
            "Folder Name": entry.extras.get("folder", ""),
            "Quantity": str(entry.quantity),
            "Trade Quantity": str(entry.trade_quantity) if entry.trade_quantity else "0",
            "Card Name": entry.card.name,
            "Set Code": entry.card.set_code or "",
            "Set Name": entry.card.set_name or "",
            "Card Number": entry.card.collector_number or "",
            "Condition": condition_str,
            "Printing": printing,
            "Language": entry.language.name.replace("_", " ").title(),
            "Price Bought": str(entry.purchase_price) if entry.purchase_price else "",
            "Date Bought": date_str,
            "LOW": entry.extras.get("price_low", ""),
            "MID": entry.extras.get("price_mid", ""),
            "MARKET": entry.extras.get("price_market", ""),
        }

    def get_headers(self) -> list[str]:
        return [
            "Folder Name",
            "Quantity",
            "Trade Quantity",
            "Card Name",
            "Set Code",
            "Set Name",
            "Card Number",
            "Condition",
            "Printing",
            "Language",
            "Price Bought",
            "Date Bought",
            "LOW",
            "MID",
            "MARKET",
        ]
