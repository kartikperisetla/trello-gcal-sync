from base_entity import *

class Board(BaseEntity):
    def __init__(self):
        super().__init__()
        self.type = "BOARD"