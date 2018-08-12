import requests           
import json
from auth_mgr import *
from board import *
from settings import *

class BoardManager:
    def __init__(self, auth_mgr=None):
        self._url = "https://trello.com/1/members/me/boards"
        self.args = {'fields': 'name', 'lists': 'open'}
        self.auth_mgr = auth_mgr

    def _check_valid_auth_mgr(self):
        if self.auth_mgr is None:
            print(self.__class__.__name__+":Invalid Auth manager- try passing valid auth manager.")
            exit()

    def get_boards(self, board_names_set=None):
        self._check_valid_auth_mgr()

        response = requests.get(self._url, params=self.auth_mgr.get_key_token(), data=self.args)

        if response.status_code == 200:
            board_coll = self._parse_json_for_boards(response.json())
            self._populate_boards_with_cards(board_coll, board_names_set)
            return board_coll

    def _parse_json_for_boards(self, json=None):
        if json is None:
            return
        resp = []

        for board in json:
            new_b = Board(auth_mgr=self.auth_mgr)
            for key, val in board.items():
                new_b.add_prop(key, val)
            resp.append(new_b)        
        return resp

    def _populate_boards_with_cards(self, board_coll, board_names_set=None):
        for _board in board_coll:
            if board_names_set is not None:
                if _board.get_prop("name") not in board_names_set:
                    continue
            print("about to fetch cards for board '"+ _board.get_prop("name") +"'")
            _board.fetch_cards()

        

if __name__ == "__main__":
    am = AuthManager(key = KEY, token = TOKEN)

    bm = BoardManager(auth_mgr=am)
    board_coll = bm.get_boards()