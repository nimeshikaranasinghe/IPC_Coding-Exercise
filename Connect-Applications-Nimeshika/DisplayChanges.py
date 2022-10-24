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

print ("File changed")