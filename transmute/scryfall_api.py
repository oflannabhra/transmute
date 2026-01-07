import json

import requests

from transmute.constants import *

class CardNotFoundException(Exception):
    pass

class ScryfallAPI:

    @staticmethod
    def get_card_details(card_name: str, set_code: str=None):
        try:
            url = None
            if set_code:
                url = f"{SCRYFALL_API}{card_name}&set={set_code}"
            else:
                url = f"{SCRYFALL_API}{card_name}"
            details = ScryfallAPI.query(url=url)
        except CardNotFoundException as e:
            # try again without set code
            print(f"card not found: {card_name}")
            if set_code:
                print("retrying without set name")
                details = ScryfallAPI.get_card_details(card_name=card_name)
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