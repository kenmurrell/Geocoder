import sys
import csv
import requests
import xml.etree.ElementTree as ET
import os

coding='xml'
server='https://maps.googleapis.com/maps/api/geocode/{0}?address='.format(coding)


#UTF-8 is love, UTF-8 is life
def _encode_to_byte(text):
    return text.encode('ascii', errors="backslashreplace").decode('utf-8')

class Geocode(object):

    def __init__(self,key_file):
        b= ET.parse(key_file)
        self.key = b.getroot().text

    def generate(self, csv_in, csv_out):
        with open(csv_in,'r') as csvinput, open(csv_out, 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)
            db = []
            header=['Address','City','Province','Latitude','Longitude']
            writer.writerow(header)
            for row in reader:
                try:
                    loc_str= row[0].replace(' ','+')+',+'+row[1].replace(' ','+') +',+'+ row[2].replace(' ','')
                    url= server + loc_str + "&key=" + self.key
                    server_response=requests.get(url)
                    server_response = ET.fromstring(_encode_to_byte(server_response.text))
                    #_check_status(server_response) #throws ConnectionError
                    struct=server_response.find('result').find('geometry').find('location')
                    lat=struct.find('lat').text
                    lng=struct.find('lng').text
                    row.append(lat)
                    row.append(lng)
                except Exception:
                    pass
                finally:
                    writer.writerow(row)
            writer.writerows(db)

    def csv_count(self, csvfile):
        with open(csvfile,'r') as csv_obj:
            obj = csv.reader(csv_obj)
            ctr = sum(1 for row in obj)
        return ctr

    class ConnectionError(Exception):
        def __init__(self, message):
            self.message = message
