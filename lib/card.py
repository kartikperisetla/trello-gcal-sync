from base_entity import *

class Card(BaseEntity):
    def __init__(self):
        super().__init__()
        self.type = "CARD"