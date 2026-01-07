"""Enums for card attributes with parsing support."""

from enum import Enum


class Condition(Enum):
    """Card condition using standard grading scale."""

    MINT = "M"
    NEAR_MINT = "NM"
    LIGHTLY_PLAYED = "LP"
    MODERATELY_PLAYED = "MP"
    HEAVILY_PLAYED = "HP"
    DAMAGED = "DMG"

    @classmethod
    def from_string(cls, value: str | None) -> "Condition | None":
        """Parse condition from various format representations."""
        if not value:
            return None

        normalized = value.strip().upper()

        # Direct matches
        mapping = {
            "M": cls.MINT,
            "MINT": cls.MINT,
            "NM": cls.NEAR_MINT,
            "NEAR MINT": cls.NEAR_MINT,
            "NEARMINT": cls.NEAR_MINT,
            "LP": cls.LIGHTLY_PLAYED,
            "LIGHTLY PLAYED": cls.LIGHTLY_PLAYED,
            "LIGHTLYPLAYED": cls.LIGHTLY_PLAYED,
            "SP": cls.LIGHTLY_PLAYED,  # Some formats use SP (Slightly Played)
            "SLIGHTLY PLAYED": cls.LIGHTLY_PLAYED,
            "MP": cls.MODERATELY_PLAYED,
            "MODERATELY PLAYED": cls.MODERATELY_PLAYED,
            "MODERATELYPLAYED": cls.MODERATELY_PLAYED,
            "PLAYED": cls.MODERATELY_PLAYED,
            "HP": cls.HEAVILY_PLAYED,
            "HEAVILY PLAYED": cls.HEAVILY_PLAYED,
            "HEAVILYPLAYED": cls.HEAVILY_PLAYED,
            "DMG": cls.DAMAGED,
            "DAMAGED": cls.DAMAGED,
            "D": cls.DAMAGED,
            "POOR": cls.DAMAGED,
        }

        return mapping.get(normalized)


class Finish(Enum):
    """Card finish/printing type."""

    NONFOIL = "nonfoil"
    FOIL = "foil"
    ETCHED = "etched"

    @classmethod
    def from_string(cls, value: str | bool | int | None) -> "Finish":
        """Parse finish from various format representations."""
        if value is None:
            return cls.NONFOIL

        # Handle boolean
        if isinstance(value, bool):
            return cls.FOIL if value else cls.NONFOIL

        # Handle int (0/1)
        if isinstance(value, int):
            return cls.FOIL if value else cls.NONFOIL

        normalized = str(value).strip().upper()

        # Empty string means nonfoil
        if not normalized:
            return cls.NONFOIL

        # Check for etched first (more specific)
        if "ETCHED" in normalized or normalized == "FOIL_ETCHED":
            return cls.ETCHED

        # Check for foil indicators
        foil_indicators = {
            "FOIL",
            "YES",
            "TRUE",
            "1",
            "Y",
            "PREMIUM",
        }

        if normalized in foil_indicators:
            return cls.FOIL

        # Default to nonfoil for "REGULAR", "NO", "FALSE", "0", "N", "NORMAL"
        return cls.NONFOIL


class Language(Enum):
    """Card language codes (Scryfall format)."""

    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    JAPANESE = "ja"
    KOREAN = "ko"
    RUSSIAN = "ru"
    SIMPLIFIED_CHINESE = "zhs"
    TRADITIONAL_CHINESE = "zht"
    HEBREW = "he"
    LATIN = "la"
    ANCIENT_GREEK = "grc"
    ARABIC = "ar"
    SANSKRIT = "sa"
    PHYREXIAN = "ph"

    @classmethod
    def from_string(cls, value: str | None) -> "Language":
        """Parse language from various format representations."""
        if not value:
            return cls.ENGLISH

        normalized = value.strip().lower()

        # Code to enum mapping
        code_mapping = {member.value: member for member in cls}
        if normalized in code_mapping:
            return code_mapping[normalized]

        # Full name mapping
        name_mapping = {
            "english": cls.ENGLISH,
            "spanish": cls.SPANISH,
            "french": cls.FRENCH,
            "german": cls.GERMAN,
            "italian": cls.ITALIAN,
            "portuguese": cls.PORTUGUESE,
            "japanese": cls.JAPANESE,
            "korean": cls.KOREAN,
            "russian": cls.RUSSIAN,
            "chinese simplified": cls.SIMPLIFIED_CHINESE,
            "simplified chinese": cls.SIMPLIFIED_CHINESE,
            "chinese traditional": cls.TRADITIONAL_CHINESE,
            "traditional chinese": cls.TRADITIONAL_CHINESE,
            "chinese": cls.SIMPLIFIED_CHINESE,  # Default to simplified
            "hebrew": cls.HEBREW,
            "latin": cls.LATIN,
            "ancient greek": cls.ANCIENT_GREEK,
            "greek": cls.ANCIENT_GREEK,
            "arabic": cls.ARABIC,
            "sanskrit": cls.SANSKRIT,
            "phyrexian": cls.PHYREXIAN,
        }

        return name_mapping.get(normalized, cls.ENGLISH)
