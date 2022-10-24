from multiprocessing.connection import Client
import  time

def check_json():
    # Check the Json file
    # return True if Json is changed
    # return False if Json is not changed
    return False

def nim_checker():
    address = ('localhost', 6000)
    conn = Client(address, authkey=b'secret password')
    while True:
        changed_bool = check_json()
        if(changed_bool == True):
            conn.send('different')
        else:
            conn.send('same')
        time.sleep(1)               # sleep for 1 second
    # conn.close()

if __name__ == '__main__':
    nim_checker()