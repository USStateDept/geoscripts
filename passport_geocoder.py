import csv
import geocoder


INPUTFILE = "C:\\Users\\nathanhilbert\\workspace\\Passports\\Raw Data\\Acceptance Facilities.csv"
HAS_HEADERS = True

OUTPUT = "C:\\Users\\nathanhilbert\\workspace\\Passports\\CleanedData\\Acceptance Facilities.csv"

DEBUG = True
LIMIT = 10

counter = 0

tempoutput = []

successdict = {"success":0, "fails":0}

with open(INPUTFILE, 'rb') as csvinput:

    isfirst = True
    headers = []
    thereader = csv.reader(csvinput, delimiter=',')

    for row in thereader:

        counter +=1
        if isfirst and HAS_HEADERS:
            tempoutput.append(row + ["lat", "lon"])
            headers = row
            isfirst = False
            continue
        dictedinput = dict(zip(headers, row))
        #OSM was not accurate, switch to google
        g = geocoder.yahoo(dictedinput['Address'] + "," + dictedinput['City'] + "," + dictedinput['State'] + "," + dictedinput['Zip Code'])

        if DEBUG:
            print g
            print "looking at ", dictedinput['Address'] + "," + dictedinput['City'] + "," + dictedinput['State'] + "," + dictedinput['Zip Code']
        if g.lat and g.lng:
            tempoutput.append(row + [g.lat, g.lng])
            successdict['success'] += 1
            if DEBUG:
                print g.lat, g.lng
        else:
            g = geocoder.google(dictedinput['Address'] + "," + dictedinput['City'] + "," + dictedinput['State'] + "," + dictedinput['Zip Code'])
            if g.lat and g.lng:
                tempoutput.append(row + [g.lat, g.lng])
                successdict['success'] += 1
                if DEBUG:
                    print g.lat, g.lng
            else:
                g = geocoder.osm(dictedinput['Address'] + "," + dictedinput['City'] + "," + dictedinput['State'] + "," + dictedinput['Zip Code'])
                if g.lat and g.lng:
                    tempoutput.append(row + [g.lat, g.lng])
                    successdict['success'] += 1
                    if DEBUG:
                        print g.lat, g.lng
                else:
                    successdict['fails'] += 1
                    print "there was an error with", dictedinput['Address'] + "," + dictedinput['City'] + "," + dictedinput['State'] + "," + dictedinput['Zip Code']
                    tempoutput.append(row + ["x", "x"])
        # if DEBUG:
        #     if counter > LIMIT:
        #         break

print "Success:", successdict['success']
print "Fails:", successdict['fails']



with open(OUTPUT, 'wb') as csvoutput:
    thewriter = csv.writer(csvoutput, delimiter=',')
    for temprow in tempoutput:
        thewriter.writerow(temprow)