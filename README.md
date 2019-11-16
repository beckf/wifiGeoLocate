# wifiGeoLocate

## Initial Setup
1)  Change the Makefile to correct reverse-domain.
2)  For notifications, create a script on a webhost to handle notifications.

## Running wifiGeoLocate
Run with Google API key as argument:

  -h : Print Help

  -v : Print Version

  -k : (Required) Google API Key

  -u : Notify URL

  -K : Key to Notify Web URL (Required with -n and -u)

  -d : Display location in STDOUT
  
  -a : Play Find My Device alert sound at full volume.

  -n : Display location and Notify using -u URL.

To notify of location:
./main.py -k "GoogleAPIKey" -a -n -u "https://server.domain.tld/path/to/notify.php" -K "RandomKeyLocatedinNotify.phpPage"

To report location back to terminal without notifying:
./main.py -k "GoogleAPIKey" -d


## Building with PyInstaller

pyinstaller main.py --onefile

cp -rfv dist/main ./wifiLocate

sudo make pkg
