#!/usr/bin/python

#
# wifiGeoLocate:  Uses google geolocation services to determine computer location
#

import urllib
import urllib2
import socket
import re
import json
import sys, getopt
from commands import getoutput

__version__ = "1.9.4"
__author__ = "Forrest Beck"

googleAPIURL = "https://www.googleapis.com/geolocation/v1/geolocate?key="

def collectSerial():
    serialNumber = getoutput(
        '/usr/sbin/system_profiler SPHardwareDataType | grep -i "Serial Number" | cut -d ":" -f 2 | tr -d " " ')
    return serialNumber

def collectHostName():
    host = socket.gethostname()
    return host

def collectNetworks():
    nearbyNetworks = getoutput(
        "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan "
        "| grep -v BSSID | sed 's/^ *//' | sed 's/[ \t]*$//' | tr -s ' ' | rev | cut -d' ' -f5,6 | rev")
    return nearbyNetworks

def usage():
    print sys.argv[0] + " -k apiKey -n(doNotify) -u(notifyURL) -K(notifyKey) | -d(display)"

def printVer():
    print __version__
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
        print "Wireless Access Points Discovered: " + str(request)
        try:
            req = urllib2.Request(apiURL)
            req.add_header('Content-Type', 'application/json')
            data = json.dumps(request)
            response = urllib2.urlopen(req, data)

            if response:
                return response
        except:
            exit(0)

def notify(jsonLocation, notifyURL, notifyKey):
    location = json.loads(jsonLocation.read())
    print "Google Location Data " + str(location)
    notifyText = "Serial Number: " + collectSerial() + \
                 "\nHostname: " + collectHostName() + \
                 "\nAccuracy: " + str(location['accuracy']) + " meter radius" \
                                                              "\nLocation: http://maps.google.com/maps?z=12&t=k&q=loc:" + \
                 str(location['location']['lat']) + "+" + \
                 str(location['location']['lng'])
    postData = urllib.urlencode({'key': notifyKey,
                'notifyText': notifyText})

    try:
        req = urllib2.Request(notifyURL, postData)
        notify = urllib2.urlopen(req)
    except:
        exit(0)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'k:vuhnKd')
    except:
        usage()
        sys.exit(2)

    for opt, arg in opts:

        if opt in ('-k'):
            apiKey = arg
        elif opt in ('-K'):
            notifyKey = arg
        elif opt in ('-u'):
            notifyURL = arg
        elif opt in ('-v'):
            printVer()
            exit(0)
        elif opt in ('-h'):
            usage()
            exit(0)

        if not apiKey:
            usage()
            exit(0)

        if opt in ('-n') and apiKey:
            # Display output and notify.
            googleResponse = googleGeolocate(collectNetworks(), apiKey)
            if googleResponse:
                notify(googleResponse, notifyURL, notifyKey)
        elif opt in ('-d'):
            # Display output without notifying.
            print json.loads(googleGeolocate(collectNetworks(), apiKey).read())

if __name__ == "__main__":
    main(sys.argv[1:])
