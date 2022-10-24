""" Import required python modules """
from multiprocessing.connection import Client
import time
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
hash_file = read_configs.get_one_option("CHECK_FILE_DETAILS", "hash_value_file")



def check_json():
    # Check the Json file
    # return True if Json is changed
    # return False if Json is not changed

    # Read the hash value
    f = open(hash_file, "r")
    file_hash_prev = (f.read())
    
    # Get the hash of the file
    BLOCK_SIZE = 32768              # The size of each read from the file

    file_hash = hashlib.sha256()    # Create the hash object
    with open(wireless_APS_file, 'rb') as f:        # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE)                     # Read from the file. Take in the amount declared above
        while len(fb) > 0:                          # While there is still data being read from the file
            file_hash.update(fb)                    # Update the hash
            fb = f.read(BLOCK_SIZE)                 # Read the next block from the file

    file_hash_new = file_hash.hexdigest()         # Get the hexadecimal digest of the hash

    # Write hash value to a file
    fo = open(hash_file, "r+")  # Open a file in read/write mode
    line = fo.write( file_hash_new )      # Write a line at the end of the file.
    fo.close()                              # Close opened file

    if (file_hash_prev == file_hash_new):
        return False
    else:
        return True



def MonitorChanges():
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
    MonitorChanges()