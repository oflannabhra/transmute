HELVAULT_SUPPLEMENTAL_HEADERS = [
    "collector_number",
    "oracle_id",
    "scryfall_id",
]
HELVAULT_HEADER_MAP = {
    "name_header": "name",
    "quantity_header": "quantity",
    "set_code_header": "set_code",
    "set_name_header": "set_name",
    "foil_header": "extras",
    "language_header": "language",
}

GOLDFISH_SUPPLEMENTAL_HEADERS = [
    "Variation"
]
GOLDFISH_HEADER_MAP = {
    "name_header": "Card",
    "quantity_header": "Quantity",
    "set_code_header": "Set ID",
    "set_name_header": "Set Name",
    "foil_header": "Foil",
}

SCRYFALL_API = "https://api.scryfall.com/cards/named?exact="
SCRYFALL_ID_KEY = "id"
SCRYFALL_LANGUAGE_KEY = "lang"
SCRYFALL_SETCODE_KEY = "set"
