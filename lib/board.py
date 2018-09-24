import requests           
import json
from lib.base_entity import *
from lib.card import *

class Board(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "BOARD"
        self.cards = {}
        self.cards_url = None

    def _get_board_url_for_cards(self):
        if self.cards_url is None:
            self.cards_url =  "https://api.trello.com/1/boards/"+ self.get_prop("id")+"/?cards=all"
        return self.cards_url

    def add_card(self, card_instance):
        if card_instance is None:
            print(self.__class__.__name__+" None passed as card_instance")
            return

        card_id = card_instance.get_prop("id")
        if card_id in self.cards:
            print(self.__class__.__name__+":card '" + card_id + "' already exists in this board")
            return
        self.cards[card_id] = card_instance
    
    def fetch_cards(self):
        response = requests.get(self._get_board_url_for_cards(), params=self.auth_mgr.get_key_token())
        self._parse_json_for_cards(response.json())

    def _parse_json_for_cards(self, json=None):
        if json is None:
            return
        
        for card in json["cards"]:
            new_c = Card(auth_mgr=self.auth_mgr)
            for key, val in card.items():
                new_c.add_prop(key, val)
            self.add_card(new_c)