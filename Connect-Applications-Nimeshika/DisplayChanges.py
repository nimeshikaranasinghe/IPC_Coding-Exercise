""" Import required python modules """
from multiprocessing.connection import Listener
import json

import components.log_writer as log_py
import components.read_config_file as read_config


# Define globla variables
read_configs = read_config.ReadConfig()                                                     # Create read config object ot read the ini file
wireless_APS_file = read_configs.get_one_option("CHECK_FILE_DETAILS", "file_name")          # Get the file name
conn_hostname = read_configs.get_one_option("CONNECTION_DETIALS", "hostname")               # Get the hostname for the connection 
conn_port = int(read_configs.get_one_option("CONNECTION_DETIALS", "port"))                  # Get the port number  for the connection 



def identify_changes(curr_json, prev_json):
    """ Identify changes fields """
    
    # Get only the APs list under 'access_points'
    curr_json_list = curr_json['access_points']
    prev_json_list = prev_json['access_points']
    curr_aps, prev_aps = {}, {}

    # List APs as - ssid : [snr, channel]
    for i in range(len(curr_json_list)):
        curr_aps[curr_json_list[i]['ssid']] = [curr_json_list[i]['snr'], curr_json_list[i]['channel']]
    for i in range(len(prev_json_list)):
        prev_aps[prev_json_list[i]['ssid']] = [prev_json_list[i]['snr'], prev_json_list[i]['channel']]

    # Identify the removed/added/static APs
    removed = [x for x in prev_aps.keys() if x not in curr_aps.keys()]
    added = [x for x in curr_aps.keys() if x not in prev_aps.keys()]
    static = [x for x in curr_aps.keys() if x in prev_aps.keys()]

    # Get the list of changes to a python list
    changes = []
    # Catch parameter changes
    for key in static:
        for idx, parameter in enumerate(['snr', 'channel']):
            if(curr_aps[key][idx] != prev_aps[key][idx]):
                changes.append(f"{key}'s {parameter} has changed from {prev_aps[key][idx]} to {curr_aps[key][idx]}")

    # Catch Removed APs
    for key in removed:
        changes.append(f'{key} is removed from the list')

    # Catch Added APs
    for key in added:
        changes.append(f'{key} is added to the list with SNR {curr_aps[key][0]} and channel {curr_aps[key][1]}')

    return changes



def print_changes(start = 0):
    """ Print any file changes """

    global prev_json_object

    if(start == 1):
        with open(wireless_APS_file, 'r') as fid:
            prev_json_object  = json.load(fid)
    else:
        with open(wireless_APS_file, 'r') as fid:
            json_object = json.load(fid)
        
        changes = identify_changes(json_object, prev_json_object)
        print('\n')
        log_py.info ("Printing file changes.")
        
        for line in changes:
            print(line)
            log_py.info ("{}".format(line))
        
        prev_json_object = json_object



def DisplayChanges():
    """ Listen to file changes """

    address = (conn_hostname, conn_port)
    listner = Listener(address, authkey=b'secret password')
    conn = listner.accept() 

    #print('connection accepted from', listner.last_accepted)
    log_py.info ("Connection accepted from {}".format(listner.last_accepted))

    # Initial read of the Json file
    print_changes(start=1)
    while True:
        # Read message if available
        try:
            msg = conn.recv()
        except EOFError:
            #print('connection terminated!')
            log_py.error ("Connection terminated!")
            break

        # Check if Json is changed and display changes
        if(msg == 'different'):
            print_changes()

    listner.close()



if __name__ == '__main__':
    DisplayChanges()