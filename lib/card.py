from base_entity import *

class Card(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "CARD"