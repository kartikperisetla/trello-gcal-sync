import copy

class AuthManager:
    def __init__(self, key=None, token=None):
        self._d = {}
        self._d["key"] = key
        self._d["token"] = token
    
    def get_key(self):
        return self._d["key"]
    
    def get_token(self):
        return self._d["token"]
    
    def get_key_token(self):
        return copy.deepcopy(self._d)