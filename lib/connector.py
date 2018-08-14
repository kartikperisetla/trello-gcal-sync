from auth_mgr import *
from board_manager import *
from gcal_manager import *
from datetime import timezone, datetime, timedelta
from settings import *


class Connector:
    def __init__(self):
        am = AuthManager(key = KEY, token = TOKEN)
        self.board_manager = BoardManager(auth_mgr=am)
        self.gcal_manager = GcalManager()

        self.processed_card_coll = {}
        self.boards_to_process = set(BOARDS.split(","))
        
    def run(self):
        board_coll = self.board_manager.get_boards(self.boards_to_process)
        for board in board_coll:
            if board.get_prop("name") in self.boards_to_process:
                self.process_board(board)

    def process_board(self, board):
        if board is None:
            return
        
        for _, card in board.cards.items():
            if card is not None and card.get_prop("due") is not None:    
                event = self._get_event_for_card(card, board.get_prop("name"))
                self.gcal_manager.add_event(event)
    
    def utc_to_local(self, utc_dt):
        utc_dt = datetime.strptime(utc_dt, '%Y-%m-%dT%H:%M:%S.%fz')
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def _get_event_for_card(self, card, board_name):
        event = {
                    "summary" : card.get_prop("name") + " [" + board_name+"]",
                    "description" : card.get_prop("desc"),
                    'start': {
                            'dateTime': card.get_prop("due"),
                            'timeZone': 'America/Los_Angeles',
                            },
                    'end': {
                            'dateTime': (datetime.strptime(card.get_prop("due"),'%Y-%m-%dT%H:%M:%S.%fz')+ timedelta(minutes = 30)).strftime('%Y-%m-%dT%H:%M:%S.%fz'),
                            'timeZone': 'America/Los_Angeles',
                            }
                }
        return event