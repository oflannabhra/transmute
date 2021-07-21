import csv
import json
import os.path
from time import sleep

import requests

from transmute.collection import CollectionType, MTGCollection

SCRYFALL_API = "https://api.scryfall.com/cards/named?exact="
SCRYFALL_ID_KEY = "id"
SCRYFALL_LANGUAGE_KEY = "lang"
SCRYFALL_SETCODE_KEY = "set"

class CardNotFoundException(Exception):
    pass

class Transmute:

    def __init__(self, in_file: str, out_file: str) -> None:
        self.infile = in_file
        self.outfile = out_file

        self.validate_or_create_files()

        self.reader = None
        self.write = None


    @staticmethod
    def get_card_details(card_name: str, set_code: str=None):
        try:
            url = None
            if set_code:
                url = f"{SCRYFALL_API}{card_name}&set={set_code}"
            else:
                url = f"{SCRYFALL_API}{card_name}"
            details = Transmute.query(url=url)
        except CardNotFoundException as e:
            # try again without set code
            print(f"card not found: {card_name}")
            if set_code:
                print("retrying without set name")
                details = Transmute.get_card_details(card_name=card_name)
            else:
                raise Exception("Unable to retrieve card details") from e
        return details  


    @staticmethod
    def query(url: str) -> dict:
        print(f"querying: {url}")
        response = requests.get(url)
        details = response.json()

        if set(['code', 'status']).issubset(set(details.keys())):
            if details['code'] == 'not_found':
                print("query failed")
                raise CardNotFoundException()
            if details['status'] in range(400, 499, 1):
                print(f"query failed: {url}")
                raise Exception(f"{details.status} response from Scryfall: {details.details}")

        return details


    def validate_or_create_files(self):
        # check input and output files
        if not os.path.isfile(self.infile):
            raise Exception("input file does not exist")
        if not os.path.isfile(self.outfile):
            # output file doesn't exist, create it
            open(self.outfile, 'a').close()
        

    def convert_collection(self, input_type: CollectionType, output_type: CollectionType):
        # create collections
        in_collection = MTGCollection(input_type)
        out_collection = MTGCollection(output_type)

        total_cards = sum(1 for _ in open(self.infile)) - 1
        print(f"processing {total_cards} cards\n")
        
        # open files and begin processing
        with open(self.infile) as input_file, open(self.outfile, 'w') as output_file:
            # setup CSV objects
            self.reader = csv.DictReader(input_file)
            self.writer = csv.DictWriter(output_file, fieldnames=out_collection.output_headers)
            self.writer.writeheader()


            for row in self.reader:
                in_collection.current_row = row
                details = None
                
                # print(".", end="", flush=True)

                if out_collection.requires_scryfall:
                    details = None
                    try:
                        details = Transmute.get_card_details(card_name=row[in_collection.name_header], set_code=row[in_collection.set_code_header])
                        sleep(0.075)
                    except Exception as e:
                        print(f"failed: {e}")
                        continue
                
                
                output_dict = self.convert_headers(
                    in_col=in_collection, 
                    out_col=out_collection, 
                    supplementary_dict=details
                )

                self.writer.writerow(output_dict)


    def convert_headers(self, in_col: dict, out_col: dict, supplementary_dict: dict=None) -> dict:
        out_dict = {}
        if out_col.requires_scryfall:
            # prefer values returned by scryfall
            skipped_keys = [out_col.scryfall_id_header, out_col.foil_header, out_col.language_header, out_col.quantity_header, out_col.set_code_header]
            for key in out_col.output_headers:
                if key in skipped_keys:
                    continue
                out_dict[key] = supplementary_dict[key]
            out_dict[out_col.scryfall_id_header] = supplementary_dict[SCRYFALL_ID_KEY]
            out_dict[out_col.language_header] = supplementary_dict[SCRYFALL_LANGUAGE_KEY]
            out_dict[out_col.set_code_header] = supplementary_dict[SCRYFALL_SETCODE_KEY]
            
        else:
            out_dict[out_col.name_header] = in_col.current_row[in_col.name_header]
            out_dict[out_col.set_code_header] = in_col.current_row[in_col.set_code_header]
            out_dict[out_col.quantity_header] = in_col.current_row[in_col.quantity_header]
            out_dict[out_col.set_name_header] = in_col.current_row[in_col.set_name_header]
        
        out_dict[out_col.quantity_header] = in_col.current_row[in_col.quantity_header]
        if in_col.foil_value in in_col.current_row[in_col.foil_header]:
            out_dict[out_col.foil_header] = out_col.foil_value    

        return out_dict    