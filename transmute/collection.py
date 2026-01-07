import csv
from abc import ABC, abstractmethod
from enum import Enum
from csv import register_dialect
from __future__ import annotations
from os import name

from transmute.card import *
from transmute.collection import *
from transmute.constants import *
from transmute.scryfall_api import ScryfallAPI

# TODO:
# 1) create a card type.
# 2) CollectionTypes should have an import function
# 3) CollectionTypes should have an export function
# 4) InternalCollectionType sits in the middle

    

class CollectionType(Enum):
    helvault = "hel"
    goldfish = "gld"

    def collection(self) -> BaseCollection:
        if self is CollectionType.helvault:
            return HelvaultCollection(self)
        elif self is CollectionType.goldfish:
            return GoldfishCollection(self)
    
    def get_headers(self) -> dict:
        if type is CollectionType.helvault:
            return Headers(map=HELVAULT_HEADER_MAP, supplemental=HELVAULT_SUPPLEMENTAL_HEADERS)
        elif self is CollectionType.goldfish:
            return Headers(map=GOLDFISH_HEADER_MAP, supplemental=GOLDFISH_SUPPLEMENTAL_HEADERS)

    def uses_scryfall(self) -> bool:
        if type is CollectionType.helvault:
            return True
        else:
            return False

class Headers:
    def __init__(self, map: dict, supplemental: list):
        self.name_header = map['name_header']
        self.quantity_header = map['quantity_header']
        self.set_code_header = map['set_code_header']
        self.set_name_header = map['set_name_header']
        self.foil_header = map['foil_header']
        self.language = map.get('language_header', None)
        self.map = map
        self.supplemeßntal_headers = supplemental

    def header_string(self) -> str:
        # combine all headers into a comma separated list
        return ','.join(self.map.values().append(self.supplemental_headers))

class BaseCollection(ABC):
    def __init__(self, type: CollectionType):
        self.type = type
        self.headers = self.type.get_headers()
        self.cards = []
ß        self.dialect = type.get_dialect()

    def transmute(self, type: CollectionType) -> BaseCollection:
        new_collection = type.collection()
        new_collection.cards = self.cards
        return new_collection

    def import(self, in_file: str):
        # open the input file
        with open(in_file) as infile:
            # setup CSV reader
            self.reader = csv.DictReader(infile)

            # convert the rows to Cards
            for row in self.reader:
                self.cards.append(self.to_card(row))


    def export(self, out_file: str):
        # open the input file
        with open(out_file) as outfile:
            # setup CSV reader
            self.writer = csv.DictWriter(outfile, fieldnames=self.output_headers, dialect=self.dialect)
            # write out header row
            self.writer.writeheader()

            # convert the Cards to rows and write
            for card in self.cards:
                row = self.to_row(card)
                self.writer.writerow(row)

    @abstractmethod
    def to_card(self, row: str) -> Card:
        pass

    @abstractmethod
    def to_row(self, card: Card) -> str:
        pass

class HelvaultCollection(BaseCollection):

    def to_card(self, row: str) -> Card:
        details = {}
        details['name'] = row[self.headers.name_header]
        details['set_code'] = row[self.headers.set_code_header]
        details['set_name'] = row[self.headers.set_name_header]
        quantity = row[self.headers.quantity]
        if self.headers.language_header:
            details['language'] = row[self.headers.language_header]
        if self.headers.condition_header:
            details['condition']   = row[self.headers.condition_header]
        details['is_foil'] = row[self.headers.foil_header] == self.is_foil_value

        return Card.from_dict(card_details=details)

    def to_row(self, card: Card) -> str:
        card_details = ScryfallAPI.get_card_details(name=card.name, set_code=card.set_code)


class GoldfishCollection(BaseCollection):

    def to_card(self, row: str) -> Card:
        pass

    def to_row(self, card: Card) -> str:
        pass

class MTGCollection:
    
    def __init__(self, type: CollectionType) -> None:
        self.type = type
        self.name_header = None
        self.set_code_header = None
        self.set_code_header = None
        self.quantity_header = None
        self.foil_header = None
        self.foil_value = None
        self.variation_header = None
        self.requires_scryfall = False
        self.output_headers = None        
        self.scryfall_id_header = None
        self.current_row = None
        self.dialect = None

        self.initialize()

    def initialize(self):
        if self.type is CollectionType.helvault:
            self.name_header = "name"
            self.set_code_header = "set_code"
            self.set_name_header = "set_name"
            self.quantity_header = "quantity"
            self.foil_header = "extras"
            self.foil_value = "foil"
            self.variation_header = None
            self.language_header = "language"
            self.requires_scryfall = True
            self.output_headers = HELVAULT_OUT_HEADERS
            self.scryfall_id_header = "scryfall_id"
            # self.dialect = register_dialect("hel", doublequote=False)
        
        elif self.type is CollectionType.goldfish:
            self.name_header = "Card"
            self.set_code_header = "Set ID"
            self.set_name_header = "Set Name"
            self.quantity_header = "Quantity"
            self.foil_header = "Foil"
            self.foil_value = "True"
            self.variation_header = "Variation"
            self.language_header = None
            self.requires_scryfall = False
            self.output_headers = GOLDFISH_OUT_HEADERS
            self.scryfall_id_header = None
            self.dialect = register_dialect("gld", doublequote=False)

        else:
            raise Exception("unsupported collection type")

