#!/usr/bin/python3
import subprocess, datetime

# this function will return a list of lists describing the list of devices in the network
# format: [IP, MAC, NAME/MANUFACTURER]
# find out interface by running ifconfig and determining which interface is being used, like eth0 or wlp3s0
def scan(interface):
    # use subprocess.run to run the command
    cliOutput = subprocess.run(['sudo', 'arp-scan', '--localnet', '--interface=' + interface], stdout=subprocess.PIPE)
    # extract the output from the subprocess
    strOutput = cliOutput.stdout.decode()
    # generate a list of lists in the specified format and return it
    #return strOutput
    return [i.split('\t') for i in strOutput.split('\n')][2:-4]

def scanDict(interfaces):
    ts = datetime.datetime.now().timestamp() #seconds since the epoch (floating point)
    data = {}
    for interface, network in interfaces.items():
        data[network] = scan(interface)
    result = []
    for network, lines in data.items():
        for item in lines:
            if len(item) < 3: continue
            ip = item[0]
            mac = item[1]
            device = item[2]
            dup = False
            for other in result:
                if mac == other['MAC']:
                    dup = True
                    continue
            if dup:
                continue
            result.append({
                "IP": ip,
                "MAC": mac,
                "device": device,
                "network": network,
                "time": ts
            })
    return result

if __name__ == "__main__":
    from sense_hat import SenseHat
    sense = SenseHat()

    s = scan("wlan1")
    print(len(s))
    print(s[0:3])

    sense.clear()
    sense.set_pixel(2, 2, (0, min(len(s), 255), 0))
