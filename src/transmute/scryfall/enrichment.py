"""Card enrichment service using Scryfall API."""

from collections.abc import Callable

from transmute.core.exceptions import CardNotFoundError
from transmute.core.models import Card, CardEntry, Collection
from transmute.scryfall.api import ScryfallClient


class CardEnricher:
    """Service to enrich card entries with Scryfall data."""

    def __init__(
        self,
        client: ScryfallClient | None = None,
        on_progress: Callable[[int, int], None] | None = None,
        on_error: Callable[[CardEntry, Exception], None] | None = None,
    ) -> None:
        self.client = client or ScryfallClient()
        self.on_progress = on_progress
        self.on_error = on_error

    def enrich_entry(self, entry: CardEntry) -> CardEntry:
        """
        Enrich a single card entry with Scryfall data.

        Fills in missing fields like scryfall_id, oracle_id, etc.
        """
        card = entry.card

        # If we already have a scryfall_id, use it for lookup
        if card.scryfall_id:
            scryfall_card = self.client.get_card_by_scryfall_id(card.scryfall_id)
        else:
            # Otherwise look up by name and set
            scryfall_card = self.client.get_card_by_name(card.name, card.set_code)

        # Merge data - prefer existing data, fill in blanks from Scryfall
        entry.card = Card(
            name=card.name or scryfall_card.name,
            scryfall_id=card.scryfall_id or scryfall_card.scryfall_id,
            oracle_id=card.oracle_id or scryfall_card.oracle_id,
            set_code=card.set_code or scryfall_card.set_code,
            set_name=card.set_name or scryfall_card.set_name,
            collector_number=card.collector_number or scryfall_card.collector_number,
            rarity=card.rarity or scryfall_card.rarity,
            mana_cost=card.mana_cost or scryfall_card.mana_cost,
            type_line=card.type_line or scryfall_card.type_line,
            colors=card.colors or scryfall_card.colors,
            mtgo_id=card.mtgo_id or scryfall_card.mtgo_id,
            arena_id=card.arena_id or scryfall_card.arena_id,
            tcgplayer_id=card.tcgplayer_id or scryfall_card.tcgplayer_id,
            cardmarket_id=card.cardmarket_id or scryfall_card.cardmarket_id,
        )

        return entry

    def enrich_collection(self, collection: Collection) -> Collection:
        """Enrich all entries in a collection with Scryfall data."""
        total = len(collection)

        for i, entry in enumerate(collection.entries):
            try:
                collection.entries[i] = self.enrich_entry(entry)
            except CardNotFoundError as e:
                if self.on_error:
                    self.on_error(entry, e)

            if self.on_progress:
                self.on_progress(i + 1, total)

        return collection
