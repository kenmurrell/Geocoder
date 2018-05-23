import sys
import GoogleAPI as api
import csv

file1 = sys.argv[1]
file2 = file1.replace(".csv","-out.csv")

with open(file1,'r') as csvinput, open(file2, 'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    reader = csv.reader(csvinput)
    a = []
    header=['PostalCode','Latitude','Longitude']
    a.append(header)
    for row in reader:
        postalcode=row[0].replace(' ','+')
        try:
            lat, lng = api.getGeocode(postalcode)
            row.append(lat)
            row.append(lng)
        except Exception:
            print(postalcode)
        a.append(row)
    writer.writerows(a)
    print("Wrote "+str(len(a))+" to file")
    print("DONE")
