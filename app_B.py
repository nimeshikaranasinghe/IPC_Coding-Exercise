from multiprocessing.connection import Client
import  time
import json

def check_json(start):
    global prev_json_object
    if(start == 1):
        with open('wireless.json', 'r') as fid:
            prev_json_object  = json.load(fid)
    else:
        with open('wireless.json', 'r') as fid:
            json_object = json.load(fid)
        if(json_object == prev_json_object):
            return 0
        else:
            prev_json_object = json_object
            return 1

def nim_checker():
    address = ('localhost', 6000)
    conn = Client(address, authkey=b'secret password')
    start = 1
    while True:
        changed_bool = check_json(start)
        start = 0
        if(changed_bool == True):
            conn.send('different')
        time.sleep(1)               # sleep for 1 second
    # conn.close()

if __name__ == '__main__':
    nim_checker()
