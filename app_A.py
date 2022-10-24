from multiprocessing.connection import Listener
import json

def identify_changes(curr_json, prev_json):
    curr_json_list = curr_json['access_points']
    prev_json_list = prev_json['access_points']
    curr_aps, prev_aps = {}, {}
    for i in range(len(curr_json_list)):
        curr_aps[curr_json_list[i]['ssid']] = [curr_json_list[i]['snr'], curr_json_list[i]['channel']]
    for i in range(len(prev_json_list)):
        prev_aps[prev_json_list[i]['ssid']] = [prev_json_list[i]['snr'], prev_json_list[i]['channel']]
    removed = [x for x in prev_aps.keys() if x not in curr_aps.keys()]
    added = [x for x in curr_aps.keys() if x not in prev_aps.keys()]
    static = [x for x in curr_aps.keys() if x in prev_aps.keys()]
    changes = []
    # Only the parameter changes
    for key in static:
        for idx, parameter in enumerate(['snr', 'channel']):
            if(curr_aps[key][idx] != prev_aps[key][idx]):
                changes.append(f"{key}'s {parameter} has changed from {prev_aps[key][idx]} to {curr_aps[key][idx]}")
    # Removed APs
    for key in removed:
        changes.append(f'{key} is removed from the list')
    # Added APs
    for key in added:
        changes.append(f'{key} is added to the list with SNR {curr_aps[key][0]} and channel {curr_aps[key][1]}')

    return changes

def check_json(start = 0):
    global prev_json_object
    if(start == 1):
        with open('wireless.json', 'r') as fid:
            prev_json_object  = json.load(fid)
    else:
        with open('wireless.json', 'r') as fid:
            json_object = json.load(fid)
        changes = identify_changes(json_object, prev_json_object)
        print('\nChanges:')
        for line in changes:
            print(line)
        prev_json_object = json_object

def nim_listener():
    address = ('localhost', 6000)
    listner = Listener(address, authkey=b'secret password')
    conn = listner.accept()
    print('connection accepted from', listner.last_accepted)
    # Initial read of the Json file
    check_json(start=1)
    while True:
        # Read message if available
        try:
            msg = conn.recv()
        except EOFError:
            print('connection terminated!')
            break
        # Check if Json is changed and display changes
        if(msg == 'different'):
            check_json()

    listner.close()

if __name__ == '__main__':
    nim_listener()