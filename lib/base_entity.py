
class BaseEntity:
    def __init__(self, **kwargs):
        self.prop = {}
        self.cards = {}
        self.type = "BASE_ENTITY"

        if "auth_mgr" in kwargs:
            self.auth_mgr = kwargs["auth_mgr"]
    
    def add_prop(self, pname, pval):
        self.prop[pname] = pval
    
    def get_prop(self, pname):
        return self.prop[pname]