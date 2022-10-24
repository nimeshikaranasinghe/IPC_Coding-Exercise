""" Import required python modules """
from multiprocessing.connection import Client
import time
import hashlib

import components.log_writer as log_py
import components.read_config_file as read_config


""" Create relevant objects to call the functions """
read_configs = read_config.ReadConfig()

# Get the file name
wireless_APS_file = read_configs.get_one_option("CHECK_FILE_DETAILS", "file_name")

# Get the sleep seconds
wait_time = int(read_configs.get_one_option("CHECK_FILE_DETAILS", "read_wait_time"))



def get_file_hash():
    """ Get the hash of the file """

    BLOCK_SIZE = 32768              # The size of each read from the file

    file_hash = hashlib.sha256()    # Create the hash object
    with open(wireless_APS_file, 'rb') as file_content:         # Open the file to read it's bytes
        fb = file_content.read(BLOCK_SIZE)                      # Read from the file. Take in the amount declared above
        while len(fb) > 0:                                      # While there is still data being read from the file
            file_hash.update(fb)                                # Update the hash
            fb = file_content.read(BLOCK_SIZE)                  # Read the next block from the file
    file_hash = file_hash.hexdigest()         # Get the hexadecimal digest of the hash
    file_content.close()

    return file_hash



def check_json(start):
    """ Check the Json file. Return True if Json is changed. Return False if Json is not changed """

    global prev_file_hash
    if(start == 1):
        prev_file_hash  = get_file_hash()
    else:
        file_hash = get_file_hash()
        if(file_hash == prev_file_hash):
            return False
        else:
            log_py.info("'{}' file has changed.".format(wireless_APS_file))
            prev_file_hash = file_hash
            return True



def MonitorChanges():
    """ Monitor if file has changed """

    address = ('localhost', 6000)
    conn = Client(address, authkey=b'secret password')
    start = 1
    while True:
        changed_bool = check_json(start)
        start = 0
        if(changed_bool == True):
            conn.send('different')
        else:
            conn.send('same')
        time.sleep(wait_time)               # sleep for 1 second
    # conn.close()



if __name__ == '__main__':
    MonitorChanges()