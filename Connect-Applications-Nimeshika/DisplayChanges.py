""" Import required python modules """
from multiprocessing.connection import Listener
import os
import datetime
import sys
import hashlib

import components.log_writer as log_py
import components.read_config_file as read_config


""" Create relevant objects to call the functions """
read_configs = read_config.ReadConfig()


# Get the file name
wireless_APS_file = read_configs.get_one_option("CHECK_FILE_DETAILS", "file_name")




def display_changes():
    print ("File changed")

def DisplayChanges():
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
    DisplayChanges()