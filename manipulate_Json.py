import json


def make_json():
    data = {
        'access_points': [
            {
                "ssid": "MyAP",
                "snr": 63,
                "channel": 11
            },
            {
                "ssid": "YourAP",
                "snr": 42,
                "channel": 1
            },
            {
                "ssid": "HisAP",
                "snr": 54,
                "channel": 6
            }
        ]
    }
    json_string = json.dumps(data)
    with open('access_points', 'w') as outfile:
        outfile.write(json_string)

def change_json_forward():
    data = {
        'access_points': [
            {
                "ssid": "MyAP",
                "snr": 82,
                "channel": 11
            },
            {
                "ssid": "YourAP",
                "snr": 42,
                "channel": 6
            },
            {
                "ssid": "HerAP",
                "snr": 71,
                "channel": 1
            }
        ]
    }
    json_string = json.dumps(data)
    with open('access_points', 'w') as outfile:
        outfile.write(json_string)

def change_json_backward():
    data = {
        'access_points': [
            {
                "ssid": "MyAP",
                "snr": 63,
                "channel": 11
            },
            {
                "ssid": "YourAP",
                "snr": 42,
                "channel": 1
            },
            {
                "ssid": "HisAP",
                "snr": 54,
                "channel": 6
            }
        ]
    }
    json_string = json.dumps(data)
    with open('access_points', 'w') as outfile:
        outfile.write(json_string)

if __name__ == '__main__':
    # make_json()
    change_json_forward()
    # change_json_backward()