""" Import required python modules """
from multiprocessing.connection import Client
import time
import hashlib

import components.log_writer as log_py
import components.read_config_file as read_config


# Define globla variables
read_configs = read_config.ReadConfig()                                                     # Create read config object ot read the ini file
wireless_APS_file = read_configs.get_one_option("CHECK_FILE_DETAILS", "file_name")          # Get the file name
wait_time = int(read_configs.get_one_option("CHECK_FILE_DETAILS", "read_wait_time"))        # Get the sleep seconds
conn_hostname = read_configs.get_one_option("CONNECTION_DETIALS", "hostname")               # Get the hostname for the connection 
conn_port = int(read_configs.get_one_option("CONNECTION_DETIALS", "port"))                  # Get the port number  for the connection 


def get_file_hash():
    """ Get the hash of the file """

    BLOCK_SIZE = 32768              # The size of each read from the file

    file_hash = hashlib.sha256()                                # Create the hash object
    with open(wireless_APS_file, 'rb') as file_content:         # Open the file to read it's bytes
        fb = file_content.read(BLOCK_SIZE)                      # Read from the file. Take in the amount declared above
        while len(fb) > 0:                                      # While there is still data being read from the file
            file_hash.update(fb)                                # Update the hash
            fb = file_content.read(BLOCK_SIZE)                  # Read the next block from the file
    file_hash = file_hash.hexdigest()                           # Get the hexadecimal digest of the hash
    file_content.close()                                        # Close the opened file

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
            prev_file_hash = file_hash                                      # Save new hash for the next run
            return True



def MonitorChanges():
    """ Monitor if file has changed """

    address = (conn_hostname, conn_port)
    conn = Client(address, authkey=b'secret password')

    start = 1
    while True:
        file_is_changed = check_json(start)
        start = 0
        if(file_is_changed == True):
            conn.send('different')
        else:
            conn.send('same')
        time.sleep(wait_time)               # Sleep monitor for few seconds
    # conn.close()



if __name__ == '__main__':
    MonitorChanges()