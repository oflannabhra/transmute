"""Core data models for transmute."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from transmute.core.enums import Condition, Finish, Language


@dataclass
class Card:
    """
    Internal card representation aligned with Scryfall data model.

    This is the canonical representation used between format conversions.
    At minimum, name is required. Other fields can be populated via Scryfall lookup.
    """

    # Primary identification (name required, others from Scryfall)
    name: str

    # Scryfall identifiers
    scryfall_id: str | None = None  # Unique to this printing
    oracle_id: str | None = None  # Consistent across reprints

    # Set information
    set_code: str | None = None  # e.g., "m12"
    set_name: str | None = None  # e.g., "Magic 2012"
    collector_number: str | None = None  # e.g., "136" or "136a"

    # Card metadata
    rarity: str | None = None  # common, uncommon, rare, mythic
    mana_cost: str | None = None  # e.g., "{2}{R}"
    type_line: str | None = None  # e.g., "Creature - Goblin"
    colors: list[str] | None = None  # e.g., ["R"]

    # External IDs for other platforms
    mtgo_id: int | None = None
    arena_id: int | None = None
    tcgplayer_id: int | None = None
    cardmarket_id: int | None = None
    mvid: int | None = None  # Multiverse ID


@dataclass
class CardEntry:
    """
    Represents a collection entry - a card with quantity and condition info.

    This is what gets read from and written to CSV files.
    """

    card: Card
    quantity: int = 1

    # Condition and finish
    finish: Finish = field(default=Finish.NONFOIL)
    condition: Condition | None = None
    language: Language = field(default=Language.ENGLISH)

    # Collection metadata
    is_signed: bool = False
    is_altered: bool = False
    is_promo: bool = False

    # Trade/inventory tracking
    trade_quantity: int | None = None

    # Price information
    purchase_price: Decimal | None = None
    purchase_date: date | None = None

    # Format-specific extras (preserved during conversion)
    extras: dict[str, str] = field(default_factory=dict)


@dataclass
class Collection:
    """A collection of card entries."""

    entries: list[CardEntry] = field(default_factory=list)
    source_format: str | None = None

    def __iter__(self):
        return iter(self.entries)

    def __len__(self):
        return len(self.entries)

    def add(self, entry: CardEntry) -> None:
        """Add a card entry to the collection."""
        self.entries.append(entry)
