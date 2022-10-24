from multiprocessing.connection import Listener

def display_changes():
    print('my pawan')

def nim_listener():
    address = ('localhost', 6000)
    listner = Listener(address, authkey=b'secret password')
    conn = listner.accept()
    print('connection accepted from', listner.last_accepted)
    while True:
        try:
            msg = conn.recv()
        except EOFError:
            print('connection terminated!')
            break

        if(msg == 'different'):
            display_changes()
        elif (msg == 'close'):
            conn.close()
            break
    listner.close()

if __name__ == '__main__':
    nim_listener()