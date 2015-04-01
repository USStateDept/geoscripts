import urllib
import urllib2
import json
from time import sleep

SERVER = 'maps.google.com'
URL_PART_1 = 'http://' + SERVER + '/maps/api/geocode/json?address='
URL_PART_2 = '&sensor=false'
INPUT_FILE = 'locations-ge.txt'
OUTPUT_FILE = str(INPUT_FILE.replace('.txt','-goog.csv'))

def run():
	f=open(INPUT_FILE,'r')
	w=open(OUTPUT_FILE,'w')
	count = 0
	
	line = f.readline()
	while line :
		coord = getCoord(line)
		while coord == 'OVER_QUERY_LIMIT':
			sleep(10)
			coord = getCoord(line)
		print line.strip() + ": " + coord + "\n"		
		w.write(coord + "\n")
		count += 1
		line = f.readline()
		
	f.close()
	w.close()
	print count
	
# Dedupping is not currently working
def run_noDups():
	from linkedList import LinkedList
	f = open(INPUT_FILE,'r')
	w = open(OUTPUT_FILE,'w')
	count = 0
	lst = LinkedList()
	
	w.write('sourceStreetAddress' + "\t" + 'sourceLocality' + "\t" + 'sourceAdministrativeArea' + "\t" + 'sourceCountry' + "\t" + 'resultStatus' + "\t" + 'resultGeomType' + "\t" + 'resultLat' + "\t" + 'resultLon' + "\t" + 'resultFormatted' + "\t" + 'URL' + "\t" + 'note' + "\n")
	street_address = f.readline()
	print street_address
	while street_address :
		if lst.add(street_address):
			sleep(1)
			address = getCoord(street_address)
			while address == 'OVER_QUERY_LIMIT':
				sleep(10)
				address = getCoord(street_address)
			if address is None:
				print str(street_address.strip()) + ": " + str(getReducedCoord(street_address)) + "\n"
				w.write(str(getReducedCoord(street_address)) + "\n".encode('utf-8'))
			else:
				print str(street_address.strip()) + ": " + str(address) + "\n"
				w.write(str(address) + "\n".encode('utf-8'))
			count += 1
		street_address = f.readline()
	return street_address
	
	f.close()
	w.close()
	# Count not working
	print count + "unique coordinates were queried"	
	
def getCoord( street_address ):
	url = ""
	locality = ""
	locality1 = ""
	locality2 = ""
	administrative_area = ""
	country = ""
		
	clean_street_address = street_address.replace(' ','%20').replace(',','').replace('\n','')
	
	# Checks for address specificity using commas, tailors API call
	if street_address.count(',') == 1:
		locality, country = (street_address.split(','))
		components = '&components=locality:' + locality.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		
	elif street_address.count(',') == 2:
		locality, administrative_area, country = (street_address.split(','))
		components = '&components=locality:' + locality.strip().replace(' ','%20').replace(',','') + "|administrative_area:" + administrative_area.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		
	elif street_address.count(',') == 3:
		locality1, locality2, administrative_area, country = (street_address.split(','))
		components = '&components=locality:' + locality1.strip().replace(' ','%20').replace(',','') + locality2.strip().replace(' ','%20').replace(',','') + "|administrative_area:" + administrative_area.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		
	url = ( URL_PART_1 + clean_street_address + components + URL_PART_2 )
	
	# Makes the API call and returns data
	try:
		urllib2.urlopen(url)
		response = urllib.urlopen( url )
		data = json.loads(response.read())
		note = ""
		
		if data["status"] == 'OK':
			resultLat = data["results"][0]["geometry"]["location"]["lat"]
			resultLon = data["results"][0]["geometry"]["location"]["lng"]
			resultGeomType = data["results"][0]["geometry"]["location_type"]
				
			resultFormatted = data["results"][0]["formatted_address"].encode('utf-8')
				
			return street_address.replace('\n','') + "\t" + str(locality.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()).replace('\n','') + "\t" + str(data["status"]) + "\t" + str(resultGeomType) + "\t" + str(resultLat) + "\t" + str(resultLon) + "\t" + str(resultFormatted) + "\t" + url + "\t" + note
		
		else:
			url = ( URL_PART_1 + clean_street_address + URL_PART_2 )
			
			# Makes the API call and returns data
			try:
				urllib2.urlopen(url)
				response = urllib.urlopen( url )
				data = json.loads(response.read())
				note = ""
				
				if data["status"] == 'OK':
					resultLat = data["results"][0]["geometry"]["location"]["lat"]
					resultLon = data["results"][0]["geometry"]["location"]["lng"]
					resultGeomType = data["results"][0]["geometry"]["location_type"]
						
					resultFormatted = data["results"][0]["formatted_address"].encode('utf-8')
						
					return street_address.replace('\n','') + "\t" + str(locality.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()).replace('\n','') + "\t" + str(data["status"]) + "\t" + str(resultGeomType) + "\t" + str(resultLat) + "\t" + str(resultLon) + "\t" + str(resultFormatted) + "\t" + url + "\t" + note
				
				else:
					return street_address.replace('\n','') + "\t" + str(locality.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()).replace('\n','') + "\t" + str(data["status"]) + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + url + "\t" + note

			# Catches server errors
			except urllib2.HTTPError, e:
				reduced_address = getReducedCoord(street_address)
			except urllib2.URLError, e:
				reduced_address = getReducedCoord(street_address)

	# Catches server errors
	except urllib2.HTTPError, e:
		reduced_address = getReducedCoord(street_address)
	except urllib2.URLError, e:
		reduced_address = getReducedCoord(street_address)

def getReducedCoord( street_address ):
	url = ""
	locality = ""
	locality1 = ""
	locality2 = ""
	administrative_area = ""
	country = ""
		
	reduce_street_address = street_address.replace('\n','')
	
	# Checks for address specificity using commas, tailors API call
	if reduce_street_address.count(',') == 1:
		locality, country = (reduce_street_address.split(','))
		components = '&components=country:' + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		url = ( URL_PART_1 + country.strip().replace(' ','%20') + components + URL_PART_2 )
			
	elif reduce_street_address.count(',') == 2:
		locality, administrative_area, country = (reduce_street_address.split(','))
		components = '&components=administrative_area:' + administrative_area.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		url = ( URL_PART_1 + administrative_area.strip().replace(' ','%20') + '%20' + country.strip().replace(' ','%20') + components + URL_PART_2 )
			
	elif reduce_street_address.count(',') == 3:
		locality1, locality2, administrative_area, country = (reduce_street_address.split(','))
		components = '&components=locality:' + locality2.strip().replace(' ','%20').replace(',','') + '|administrative_area:' + administrative_area.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		url = ( URL_PART_1 + locality2.strip().replace(' ','%20') + '%20' + administrative_area.strip().replace(' ','%20') + '%20' + country.strip().replace(' ','%20') + components + URL_PART_2 )
	
	# Makes the API call and returns data
	try:
		urllib2.urlopen(url)
		response = urllib.urlopen( url )
		data = json.loads(response.read())
		note = 'Reduced precision'
		
		if data["status"] == 'OK':
			resultLat = data["results"][0]["geometry"]["location"]["lat"]
			resultLon = data["results"][0]["geometry"]["location"]["lng"]
			resultGeomType = data["results"][0]["geometry"]["location_type"]
				
			resultFormatted = data["results"][0]["formatted_address"].encode('utf-8')
			
			return street_address.replace('\n','') + "\t" + str(locality.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()).replace('\n','') + "\t" + str(data["status"]) + "\t" + str(resultGeomType) + "\t" + str(resultLat) + "\t" + str(resultLon) + "\t" + str(resultFormatted) + "\t" + url + "\t" + note
		
		else:
			return street_address.replace('\n','') + "\t" + str(locality.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()).replace('\n','') + "\t" + str(data["status"]) + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + url + "\t" + note

	# Catches server errors
	except urllib2.HTTPError, e:
		return street_address.replace('\n','') + "\t" + str(locality.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()).replace('\n','') + "\t" + 'HTTP ERROR' + "\t" + "" + "\t" + "0" + "\t" + '0' + "\t" + "" + "\t" + url + "\t" + ""
	except urllib2.URLError, e:
		return street_address.replace('\n','') + "\t" + str(locality.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()).replace('\n','') + "\t" + 'URL ERROR' + "\t" + "" + "\t" + "0" + "\t" + '0' + "\t" + "" + "\t" + url + "\t" + ""
	
def main():
	run_noDups()

if __name__ == "__main__":
	main()