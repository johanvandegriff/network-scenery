import json, time
from pymongo import MongoClient
from networkScanner import scan, scanDict
from sense_hat import SenseHat

if __name__ == "__main__":
    ROOT = "/home/pi/Nextcloud/NetworkVisualizer/network-scenery/"
    INTERFACES = {
        "wlan0": "eduroam",
        "wlan1": "HOYAHacks"
    }

    sense = SenseHat()
    sense.set_pixel(7, 7, (255, 0, 0))

    with open(ROOT + '/secret.json') as f:
        key = json.load(f)['mongodb']

    client = MongoClient(key)
    db = client.networkviz

    s = scanDict(INTERFACES)

    sense.set_pixel(7, 7, (255, 255, 0))

    #for l in s: print(l)
    print(len(s), "items")

    if len(s) > 0:
        mostRecentTime = s[0]['time']
        #with open("/home/pi/lastTime.json", 'w') as f:
        #    json.dump(mostRecenTime, f)

        print(db.arp_scan_times.insert_one({'time': mostRecentTime, 'len': len(s)}))
        print(db.arp_scans.insert_many(s))
    sense.set_pixel(7, 7, (0, 255, 0))
