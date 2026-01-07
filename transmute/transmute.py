import json
import os.path
from time import sleep

import requests

from transmute.collection import CollectionType


class Transmute:

    def __init__(self, in_file: str, out_file: str) -> None:
        self.infile = in_file
        self.outfile = out_file

        self.validate_or_create_files()

    def validate_or_create_files(self):
        # check input and output files
        if not os.path.isfile(self.infile):
            raise Exception("input file does not exist")
        if not os.path.isfile(self.outfile):
            # output file doesn't exist, create it
            open(self.outfile, 'a').close()
        

    def convert_collection(self, input_type: CollectionType, output_type: CollectionType):
        # create collections
        in_collection = input_type.collection()

        total_cards = sum(1 for _ in open(self.infile)) - 1
        print(f"processing {total_cards} cards\n")

        # read in all the rows as cards
        in_collection.import(self.infile)

        # convert to a different collecction type
        out_collection = in_collection.transmute(output_type)

        # write out the collection to a file
        out_collection.export(self.outfile)
        
        # TODO: REMOVE
        # open files and begin processing
        with open(self.infile) as input_file, open(self.outfile, 'w') as output_file:
            # setup CSV objects
            self.reader = csv.DictReader(input_file)
            self.writer = csv.DictWriter(output_file, fieldnames=out_collection.output_headers, dialect=out_dialect)
            self.writer.writeheader()


            for row in self.reader:
                in_collection.current_row = row
                details = None
                
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
            out_dict[out_col.variation_header] = in_col.current_row.get(in_col.variation_header, '""')
        
        out_dict[out_col.quantity_header] = in_col.current_row[in_col.quantity_header]
        if in_col.foil_value in in_col.current_row[in_col.foil_header]:
            out_dict[out_col.foil_header] = out_col.foil_value    

        return out_dict    