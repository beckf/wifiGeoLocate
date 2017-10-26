include /usr/local/share/luggage/luggage.make

TITLE=wifiLocate
REVERSE_DOMAIN=tld.domain
PAYLOAD=\
		pack-script-preinstall\
		pack-usr-local-sbin-wifiLocate\
		
PACKAGE_VERSION=$(shell awk -F \" '/__version__/{ print $$2 }' main.py)
