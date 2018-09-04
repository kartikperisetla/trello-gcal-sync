from lib.auth_mgr import *
from lib.board_manager import *
from lib.gcal_manager import *
from lib.history_manager import *
from datetime import timezone, datetime, timedelta
from lib.settings import *


class Connector:
    def __init__(self):
        am = AuthManager(key = KEY, token = TOKEN)
        self.board_manager = BoardManager(auth_mgr=am)
        self.gcal_manager = GcalManager()
        self.hist_manager = HistoryManager()
        
        self.processed_card_coll = {}
        self.boards_to_process = set(BOARDS.split(","))
        
    def run(self):
        # load any previous state if any exists
        self.hist_manager.load_state()

        board_coll = self.board_manager.get_boards(self.boards_to_process)
        for board in board_coll:
            if board.get_prop("name") in self.boards_to_process:
                self.process_board(board)
        
        # save history manager state
        self.hist_manager.save_state()

    def process_board(self, board):
        if board is None:
            return
        
        event_cnt = 0
        for _, card in board.cards.items():
            if card is not None and card.get_prop("due") is not None:
                card_hash = card.get_card_hash()
                
                # check if due date on card is in future - then only proceed to create cal event
                if not card.is_card_due_in_future():
                    continue
                
                # check if card_hash already present in history manager - i.e. card already processed earlier
                if self.hist_manager.get(card_hash):
                    continue

                event = self._get_event_for_card(card, board.get_prop("name"))
                self.gcal_manager.add_event(event)
                print("\n","*"*40)
                event_cnt += 1

                # add card hash to history manager
                self.hist_manager.add(card_hash, 1)
        if event_cnt>0:
            print(self.__class__.__name__, " ", event_cnt," new events created.")
    
    def utc_to_local(self, utc_dt):
        utc_dt = datetime.strptime(utc_dt, '%Y-%m-%dT%H:%M:%S.%fz')
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def _get_event_for_card(self, card, board_name):
        print("\n","*"*40)
        print("Event: ", card.get_prop("name") + " [" + board_name+"]")
        
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