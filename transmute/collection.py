from enum import Enum

HELVAULT_OUT_HEADERS = [
    "collector_number",
    "extras",
    "language",
    "name",
    "oracle_id",
    "quantity",
    "scryfall_id",
    "set_code",
    "set_name"
]

GOLDFISH_OUT_HEADERS = [
    "Card",
    "Set ID",
    "Set Name",
    "Quantity",
    "Foil",
    "Variation"
]


class CollectionType(Enum):
    helvault = "hel"
    goldfish = "gld"


class MTGCollection:
    
    def __init__(self, type: CollectionType) -> None:
        self.type = type
        self.name_header = None
        self.set_code_header = None
        self.set_code_header = None
        self.quantity_header = None
        self.foil_header = None
        self.foil_value = None
        self.requires_scryfall = False
        self.output_headers = None        
        self.scryfall_id_header = None
        self.current_row = None

        self.initialize()

    def initialize(self):
        if self.type is CollectionType.helvault:
            self.name_header = "name"
            self.set_code_header = "set_code"
            self.set_name_header = "set_name"
            self.quantity_header = "quantity"
            self.foil_header = "extras"
            self.foil_value = "foil"
            self.language_header = "language"
            self.requires_scryfall = True
            self.output_headers = HELVAULT_OUT_HEADERS
            self.scryfall_id_header = "scryfall_id"
        
        elif self.type is CollectionType.goldfish:
            self.name_header = "Card"
            self.set_code_header = "Set ID"
            self.set_name_header = "Set Name"
            self.quantity_header = "Quantity"
            self.foil_header = "Foil"
            self.foil_value = "True"
            self.language_header = None
            self.requires_scryfall = False
            self.output_headers = GOLDFISH_OUT_HEADERS
            self.scryfall_id_header = None

        else:
            raise Exception("unsupported collection type")
