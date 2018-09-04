from lib.connector import *
import time
import datetime
import os

def shall_i_stop():
    if os.path.exists("stop.now"):
        return True
    else:
        return False

if __name__ == "__main__":
    flag = 0
    rflag = 0
    while True:
        if shall_i_stop():
            if flag == 0:
                print(datetime.datetime.now(),":stopping connector execution...")
                flag = 1
            rflag = 0
        else:
            if rflag == 0:   
                print(datetime.datetime.now(), ":resumed connector execution...")
                rflag = 1
            c = Connector()
            c.run()
            c = None
            flag = 0