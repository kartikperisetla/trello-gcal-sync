from lib.base_entity import *
from datetime import timezone
from datetime import datetime

class Card(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "CARD"
    
    # method that returns hash representing card name and due date
    # <card_name:due_date>
    def get_card_hash(self):
        hash_val = self.get_prop("name") + ":" + self.get_prop("due")
        return hash_val

    def is_card_due_in_future(self):
        due_date = self.get_prop("due")
        due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S.%fz')
        local_date = due_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        # print("local_date=",local_date," for utc_date=", self.get_prop("due"))
        
        # remove timezone info
        local_date = local_date.replace(tzinfo=None)
        if local_date > datetime.now():
            return True
        else:
            return False