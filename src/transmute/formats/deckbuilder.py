"""Handler for Decked Builder CSV format."""

import contextlib
from typing import ClassVar

from transmute.core.enums import Finish
from transmute.core.models import Card, CardEntry
from transmute.formats.base import FormatHandler


class DeckBuilderHandler(FormatHandler):
    """
    Handler for Decked Builder CSV format.

    Decked Builder export format:
    Total Qty,Reg Qty,Foil Qty,Card,Set,Mana Cost,Card Type,Color,Rarity,
    Mvid,Single Price,Single Foil Price,Total Price,Price Source,Notes

    Foils are indicated by Foil Qty column (separate from Reg Qty).
    """

    name: ClassVar[str] = "deckbuilder"
    display_name: ClassVar[str] = "Decked Builder"
    required_columns: ClassVar[set[str]] = {"Total Qty", "Card", "Set"}

    def parse_row(self, row: dict[str, str]) -> CardEntry:
        # Parse Mvid
        mvid = None
        mvid_str = row.get("Mvid", "")
        if mvid_str:
            with contextlib.suppress(ValueError):
                mvid = int(mvid_str)

        card = Card(
            name=row["Card"],
            set_name=row.get("Set"),
            mana_cost=row.get("Mana Cost"),
            type_line=row.get("Card Type"),
            rarity=row.get("Rarity"),
            mvid=mvid,
        )

        # Parse color
        color_str = row.get("Color", "")
        if color_str:
            card.colors = [color_str]

        # Determine foil status from quantities
        reg_qty = int(row.get("Reg Qty", 0) or 0)
        foil_qty = int(row.get("Foil Qty", 0) or 0)
        total_qty = int(row.get("Total Qty", 1) or 1)

        # If all cards are foil
        if foil_qty > 0 and reg_qty == 0:
            finish = Finish.FOIL
            quantity = foil_qty
        elif reg_qty > 0 and foil_qty == 0:
            finish = Finish.NONFOIL
            quantity = reg_qty
        else:
            # Mixed - use total, default to nonfoil
            finish = Finish.NONFOIL
            quantity = total_qty

        # Extras for prices
        extras = {}
        if row.get("Single Price"):
            extras["single_price"] = row["Single Price"]
        if row.get("Single Foil Price"):
            extras["single_foil_price"] = row["Single Foil Price"]
        if row.get("Total Price"):
            extras["total_price"] = row["Total Price"]
        if row.get("Price Source"):
            extras["price_source"] = row["Price Source"]
        if row.get("Notes"):
            extras["notes"] = row["Notes"]

        return CardEntry(
            card=card,
            quantity=quantity,
            finish=finish,
            extras=extras,
        )

    def format_row(self, entry: CardEntry) -> dict[str, str]:
        if entry.finish in (Finish.FOIL, Finish.ETCHED):
            reg_qty = 0
            foil_qty = entry.quantity
        else:
            reg_qty = entry.quantity
            foil_qty = 0

        color_str = entry.card.colors[0] if entry.card.colors else ""

        return {
            "Total Qty": str(entry.quantity),
            "Reg Qty": str(reg_qty),
            "Foil Qty": str(foil_qty),
            "Card": entry.card.name,
            "Set": entry.card.set_name or entry.card.set_code or "",
            "Mana Cost": entry.card.mana_cost or "",
            "Card Type": entry.card.type_line or "",
            "Color": color_str,
            "Rarity": entry.card.rarity or "",
            "Mvid": str(entry.card.mvid) if entry.card.mvid else "",
            "Single Price": entry.extras.get("single_price", ""),
            "Single Foil Price": entry.extras.get("single_foil_price", ""),
            "Total Price": entry.extras.get("total_price", ""),
            "Price Source": entry.extras.get("price_source", ""),
            "Notes": entry.extras.get("notes", ""),
        }

    def get_headers(self) -> list[str]:
        return [
            "Total Qty",
            "Reg Qty",
            "Foil Qty",
            "Card",
            "Set",
            "Mana Cost",
            "Card Type",
            "Color",
            "Rarity",
            "Mvid",
            "Single Price",
            "Single Foil Price",
            "Total Price",
            "Price Source",
            "Notes",
        ]
