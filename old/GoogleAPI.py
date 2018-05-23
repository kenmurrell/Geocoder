import sys
import requests
import xml.etree.ElementTree as ET

#ie https://maps.googleapis.com/maps/api/geocode/xml?address=K0K1A0&key=AIzaSyBdehriC3bxbHMtaAPB0JJ4xiZWr23jSKA

coding='xml'
server='https://maps.googleapis.com/maps/api/geocode/{0}?address='.format(coding)
proxies = {
  'http': 'http://pchproxy.in.pch.gc.ca/accelerated_pac_base.pac',
  'https': 'http://pchproxy.in.pch.gc.ca/accelerated_pac_base.pac'
}

#This method confirms success of a server request and displays errors in the event of a failure
def _check_status(server_response):
    status = server_response.find('status').text
    #print(status)
    if(status!='OK'):
        raise ConnectionError(status)

def _get_API_key(filename):
    keyfile=ET.parse(filename)
    return keyfile.getroot().text

class ConnectionError(Exception):
    def __init__(self, message):
        self.message = message

#UTF-8 is love, UTF-8 is life
def _encode_to_byte(text):
    return text.encode('ascii', errors="backslashreplace").decode('utf-8')

def getGeocode(address,city,province): #throws ConnectionError
    location_str=address.replace(' ','+')+',+'+city.replace(' ','+') +',+'+ province.replace(' ','')
    key = _get_API_key('key.xml')
    url= server + location_str + "&key=" + key
    server_response=requests.get(url,proxies=proxies)
    server_response = ET.fromstring(_encode_to_byte(server_response.text))
    _check_status(server_response) #throws ConnectionError
    a=server_response.find('result').find('geometry').find('location')
    lat=a.find('lat')
    lng=a.find('lng')
    return lat.text, lng.text

# def getGeocode(postalcode):
#     location=postalcode
#     key = _get_API_key('key.xml')
#     url= server + location + "&key=" + key
#     server_response=requests.get(url, proxies=proxies)
#     server_response = ET.fromstring(_encode_to_byte(server_response.text))
#     _check_status(server_response) #throws ConnectionError
#     a=server_response.find('result').find('geometry').find('location')
#     lat=a.find('lat')
#     lng=a.find('lng')
#     return lat.text, lng.text
