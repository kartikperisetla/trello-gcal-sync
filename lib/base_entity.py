
class BaseEntity:
    def __init__(self):
        self.prop = {}
        self.cards = {}
        self.type = "BASE_ENTITY"
    
    def add_prop(self, pname, pval):
        self.prop[pname] = pval
    
    def get_prop(self, pname):
        return self.prop[pname]