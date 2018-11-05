#!/usr/bin/python

#
# wifiGeoLocate:  Uses google geolocation services to determine computer location
#

import requests
import socket
import re
import json
import sys, getopt
import os

__version__ = "1.9.5"
__author__ = "Forrest Beck"

googleAPIURL = "https://www.googleapis.com/geolocation/v1/geolocate?key="


def execute_command(cmd):
    return os.popen(cmd).read()


def collect_serial():
    serial_number = execute_command('/usr/sbin/system_profiler SPHardwareDataType | '
                                    'grep -i "Serial Number" | cut -d ":" -f 2 | tr -d " " ')
    return serial_number


def collect_hostname():
    host = socket.gethostname()
    return host


def collect_networks():
    nearbyNetworks = execute_command(
        "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan "
        "| grep -v BSSID | sed 's/^ *//' | sed 's/[ \t]*$//' | tr -s ' ' | rev | cut -d' ' -f5,6 | rev")
    return nearbyNetworks


def usage():
    print(sys.argv[0] + " -k apiKey -n(doNotify) -u(notifyURL) -K(notifyKey) | -d(display)")


def printVer():
    print(__version__)
    exit(0)


def googleGeolocate(networks, apiKey):
    apiURL = googleAPIURL + apiKey
    if networks:
        networksFormatted = re.compile("(.*) (.*)", re.MULTILINE).findall(networks)
        request = {"consider_ip": "false",
                   "wifiAccessPoints": [{"macAddress": str(x[0]), "signalStrength": str(x[1]), "signalToNoiseRatio": 0}
                                        for x in
                                        networksFormatted]
                   }
        print("Wireless Access Points Discovered: " + str(request))
        try:
            data = json.dumps(request)
            response = requests.post(apiURL, verify=False, json=data)
            if response:
                return response
        except:
            print("Cannot contact Google")
            exit(0)


def notify(jsonLocation, notifyURL, notifyKey):
    location = jsonLocation.json()
    print("Google Location Data " + str(location))
    notifyText = "Serial Number: " + collect_serial() + \
                 "\nHostname: " + collect_hostname() + \
                 "\nAccuracy: " + str(location['accuracy']) + " meter radius" \
                                                              "\nLocation: http://maps.google.com/maps?z=12&t=k&q=loc:" + \
                 str(location['location']['lat']) + "+" + \
                 str(location['location']['lng'])
    postData = {'key': notifyKey,
                'notifyText': notifyText}

    try:
        req = requests.post(notifyURL, postData)
    except:
        exit(0)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'k:p:u:vhnd')
    except:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-k'):
            apiKey = arg
        if opt in ('-p'):
            notifyKey = arg
        if opt in ('-u'):
            notifyURL = arg
        if opt in ('-v'):
            printVer()
            exit(0)
        if opt in ('-h'):
            usage()
            exit(0)

        if not apiKey:
            usage()
            exit(0)

        if opt in ('-n') and apiKey:
            # Display output and notify.
            googleResponse = googleGeolocate(collect_networks(), apiKey)
            if googleResponse:
                notify(googleResponse, notifyURL, notifyKey)
        elif opt in ('-d'):
            # Display output without notifying.
            print(json.loads(googleGeolocate(collect_networks(), apiKey).read()))


if __name__ == "__main__":
    main(sys.argv[1:])
