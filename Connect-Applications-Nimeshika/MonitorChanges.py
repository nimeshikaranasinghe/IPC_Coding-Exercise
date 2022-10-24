""" Import required python modules """
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


# Get the has of the file
BLOCK_SIZE = 32768              # The size of each read from the file

file_hash = hashlib.sha256()    # Create the hash object
with open(wireless_APS_file, 'rb') as f:        # Open the file to read it's bytes
    fb = f.read(BLOCK_SIZE)                     # Read from the file. Take in the amount declared above
    while len(fb) > 0:                          # While there is still data being read from the file
        file_hash.update(fb)                    # Update the hash
        fb = f.read(BLOCK_SIZE)                 # Read the next block from the file

file_hash_value = file_hash.hexdigest()         # Get the hexadecimal digest of the hash
print (file_hash_value)


# Write hash value to a file
fo = open("file_hash_value.txt", "r+")  # Open a file in read/write mode
line = fo.write( file_hash_value )      # Write a line at the end of the file.
fo.close()                              # Close opened file