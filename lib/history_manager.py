import os
import pickle

class HistoryManager:
    def __init__(self):
        self.collection = dict()
        self.dump_loc = "cards.history"
    
    def load_state(self):
        if not os.path.exists(self.dump_loc):
            print(self.__class__.__name__+":prev history not present. creating fresh history")
            return
    
        self.collection = pickle.load(open(self.dump_loc,"rb"))
        # print(self.__class__.__name__+": prev history loaded.")

    def add(self, key, val):
        if key in self.collection:
            return -1
        
        self.collection[key] = val
        return 1

    def get(self, key):
        if key in self.collection:
            return self.collection[key]
        else:
            None

    def save_state(self):
            fop = open(self.dump_loc, "wb")

            #save state
            pickle.dump(self.collection, fop)
            fop.close()