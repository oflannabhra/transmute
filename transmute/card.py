from enum import Enum
from typing import Optional
from __future__ import annotations

class Condition(Enum):
    near_mint = "NM"
    lightly_played = "LP"
    moderately_playd = "MP"
    heavily_played = "HP"
    damaged = "D"

class Card:
    def __init__(self, name: str, set_code: str, set_name: str, is_foil: bool, is_signed: bool, language: Optional[str] = None, condition: Optional[Condition] = None) -> None:
        self.name = name
        self.set_code = set_code
        self.set_name = set_name
        self.language = language
        self.condition = condition
        self.is_foil = is_foil
        self.is_signed = is_signed

    @staticmethod
    def from_dict(card_details: dict) -> Card:
        return Card(
            name = card_details.get('name'),
            set_code = card_details.get('set_code'),
            set_name = card_details.get('set_name'),
            language = card_details.get('language'),
            condition = card_details.get('condition'),
            is_foil = card_details.get('is_foil'),
            is_signed = card_details.get('is_signed')
            )
