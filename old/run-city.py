import sys
import GoogleAPI as api
import csv

file1 = sys.argv[1]
file2 = file1.replace(".csv","-out.csv")

with open(file1,'r') as csvinput, open(file2, 'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    reader = csv.reader(csvinput)
    a = []
    header=['Address','City','Province','Latitude','Longitude']
    a.append(header)
    for row in reader:
        result_str = row[1]
        try:
            lat, lng = api.getGeocode(row[0],row[1],row[2])
            row.append(lat)
            row.append(lng)
            result_str += '->OK'
        except Exception:
            result_str +='->FAIL'
        finally:
            a.append(row)
            print(result_str)
    writer.writerows(a)
    print("Wrote "+str(len(a))+" to file")
    print("DONE")
