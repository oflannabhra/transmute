"""Format handlers and registry for transmute."""

from pathlib import Path

from transmute.core.exceptions import FormatNotFoundError
from transmute.formats.base import FormatHandler


class FormatRegistry:
    """Registry of all available format handlers."""

    _handlers: dict[str, FormatHandler] = {}

    @classmethod
    def register(cls, handler: FormatHandler) -> None:
        """Register a format handler."""
        cls._handlers[handler.name.lower()] = handler

    @classmethod
    def get(cls, name: str) -> FormatHandler:
        """Get a handler by name."""
        handler = cls._handlers.get(name.lower())
        if handler is None:
            raise FormatNotFoundError(f"Unknown format: {name}")
        return handler

    @classmethod
    def list_formats(cls) -> list[str]:
        """Return list of all registered format names."""
        return sorted(cls._handlers.keys())

    @classmethod
    def detect_format(cls, file_path: Path) -> FormatHandler | None:
        """Auto-detect the format of a file."""
        for handler in cls._handlers.values():
            if handler.detect(file_path):
                return handler
        return None


def _register_handlers() -> None:
    """Register all built-in format handlers."""
    # Import handlers here to avoid circular imports
    from transmute.formats.archidekt import ArchidektHandler
    from transmute.formats.cardkingdom import CardKingdomHandler
    from transmute.formats.cardsphere import CardsphereHandler
    from transmute.formats.deckbox import DeckboxHandler
    from transmute.formats.deckbuilder import DeckBuilderHandler
    from transmute.formats.deckstats import DeckstatsHandler
    from transmute.formats.dragonshield import DragonShieldHandler
    from transmute.formats.helvault import HelvaultHandler
    from transmute.formats.manabox import ManaBoxHandler
    from transmute.formats.moxfield import MoxfieldHandler
    from transmute.formats.mtggoldfish import MTGGoldfishHandler
    from transmute.formats.mtgmanager import MTGManagerHandler
    from transmute.formats.mtgo import MTGOHandler
    from transmute.formats.mtgstocks import MTGStocksHandler
    from transmute.formats.mtgstudio import MTGStudioHandler
    from transmute.formats.tcgplayer import TCGPlayerHandler

    FormatRegistry.register(ArchidektHandler())
    FormatRegistry.register(CardKingdomHandler())
    FormatRegistry.register(CardsphereHandler())
    FormatRegistry.register(DeckboxHandler())
    FormatRegistry.register(DeckBuilderHandler())
    FormatRegistry.register(DeckstatsHandler())
    FormatRegistry.register(DragonShieldHandler())
    FormatRegistry.register(HelvaultHandler())
    FormatRegistry.register(ManaBoxHandler())
    FormatRegistry.register(MoxfieldHandler())
    FormatRegistry.register(MTGGoldfishHandler())
    FormatRegistry.register(MTGManagerHandler())
    FormatRegistry.register(MTGOHandler())
    FormatRegistry.register(MTGStocksHandler())
    FormatRegistry.register(MTGStudioHandler())
    FormatRegistry.register(TCGPlayerHandler())


# Register handlers on module load
_register_handlers()

__all__ = ["FormatHandler", "FormatRegistry"]
