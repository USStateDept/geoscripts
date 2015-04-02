import urllib
import urllib2
import json
from time import sleep

SERVER = '54.221.31.151'
URL_PART_1 = 'http://' + SERVER + '/maps/api/geocode/json?address='
URL_PART_2 = '&sensor=false'
INPUT_FILE = 'locations-ge.txt'
OUTPUT_FILE = str(INPUT_FILE.replace('.txt','-dstk.csv'))

# global variables that may not be useful
url = ""
url1 = ""
url2 = ""
url3 = ""
url4 = ""
locality1 = ""
locality2 = ""
locality3 = ""
locality1 = ""
administrative_area = ""
country = ""
address1 = ""
address2 = ""
address3 = ""
address4 = ""
address0 = ""
note = ""
resultLat = ""
resultLon = ""
resultLocality = ""
resultAdminiArea1 = ""
resultCountry = ""
address_components = ""

# not running
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
	# writes field headers to file
	w.write('sourceStreetAddress' + "\t" + 'sourceLocality' + "\t" + 'sourceAdministrativeArea' + "\t" + 'sourceCountry' + "\t" + 'resultStatus' + "\t" + 'resultGeomType' + "\t" + 'resultLat' + "\t" + 'resultLon' + "\t" + 'resultFormatted' + "\t" + 'URL' + "\t" + 'note' + "\n")
	#reads lines from source file
	street_address = f.readline()
	print street_address
	while street_address :
		if lst.add(street_address):
			# sends address to function
			address = getCoord(street_address)
			# delay for API constraints
			while address == 'OVER_QUERY_LIMIT':
				sleep(10)
				address = getCoord(street_address)
			# checks for None in geocode result and converts - NOT WORKING
			if address is None:
				print str(street_address.strip()) + ": " + str(address) + "\n"
				w.write(str(address) + "\n".encode('utf-8'))
			# returns geocode result - NOT WORKING
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
	# Checks for address specificity using commas, tailors API call
	if street_address.count(',') == 4:
		# splits the source address into parts
		locality1, locality2, locality3, administrative_area, country = (street_address.split(','))
		# builds component restrictions
		components = '&components=locality:' + locality1.strip().replace(' ','%20').replace(',','') + '%20' + locality3.strip().replace(' ','%20').replace(',','') + "%20County" + "|administrative_area_level_2:" + locality3.strip().replace(' ','%20').replace(',','') + "|administrative_area_level_1:" + administrative_area.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		# builds address for tiered search (if most granular geocode result does not match source parts, try less granular until matched)
		address1 = locality1.replace(' ','%20').strip() + ", " + country.replace(' ','%20').strip()
		address2 = locality1.replace(' ','%20').strip() + ",+" + administrative_area.replace(' ','%20').strip() + ",+" + country.replace(' ','%20').strip()
		address3 = locality1.replace(' ','%20').strip() + ",+" + locality3.replace(' ','%20').strip() + ",+" + administrative_area.replace(' ','%20').strip() + ",+" + country.replace(' ','%20').strip()
		address4 = locality1.replace(' ','%20').strip() + ",+" + locality2.replace(' ','%20').strip() +",+" + locality3.replace(' ','%20').strip() + ",+" + administrative_area.replace(' ','%20').strip() + ",+" + country.replace(' ','%20').strip()
		url1 = ( URL_PART_1 + address1 + components + URL_PART_2 )
		url2 = ( URL_PART_1 + address2 + components + URL_PART_2 )
		url3 = ( URL_PART_1 + address3 + components + URL_PART_2 )
		url4 = ( URL_PART_1 + address4 + components + URL_PART_2 )
		
		# tries first geocode (locality 1-3, admin area, country)
		check4(address4, url4, administrative_area, locality1, country)
	
	elif street_address.count(',') == 3:
		# splits the source address into parts
		locality1, locality2, administrative_area, country = (street_address.split(','))
		locality3 = "null"
		# builds component restrictions
		components = '&components=locality:' + locality1.strip().replace(' ','%20').replace(',','') + "|administrative_area_level_2:" + locality2.strip().replace(' ','%20').replace(',','') + "%20County" + "|administrative_area_level_1:" + administrative_area.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		# builds address for tiered search (if most granular geocode result does not match source parts, try less granular until matched)
		address1 = locality1.replace(' ','%20').strip() + ",+" + country.replace(' ','%20').strip()
		address2 = locality1.replace(' ','%20').strip() + ",+" + administrative_area.replace(' ','%20').strip() + ",+" + country.replace(' ','%20').strip()
		address3 = locality1.replace(' ','%20').strip() + ",+" + locality3.replace(' ','%20').strip() + ",+" + administrative_area.replace(' ','%20').strip() + ",+" + country.replace(' ','%20').strip()
		address4 = "null"
		url1 = ( URL_PART_1 + address1 + components + URL_PART_2 )
		url2 = ( URL_PART_1 + address2 + components + URL_PART_2 )
		url3 = ( URL_PART_1 + address3 + components + URL_PART_2 )
		url4 = ( URL_PART_1 + address4 + components + URL_PART_2 )
		
		# tries first geocode (locality 1-2, admin area, country)
		check3(address3, url3, administrative_area, locality1, country)
		
	elif street_address.count(',') == 2:
		# splits the source address into parts
		locality1, administrative_area, country = (street_address.split(','))
		locality2 = "null"
		locality3 = "null"
		# builds component restrictions
		components = '&components=locality:' + locality1.strip().replace(' ','%20').replace(',','') + "|administrative_area_level_1:" + administrative_area.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		# builds address for tiered search (if most granular geocode result does not match source parts, try less granular until matched)
		address1 = locality1.replace(' ','%20').strip() + ",+" + country.replace(' ','%20').strip()
		address2 = locality1.replace(' ','%20').strip() + ",+" + administrative_area.replace(' ','%20')+ ",+" + country.replace(' ','%20').strip()
		address3 = "null"
		address4 = "null"
		url1 = ( URL_PART_1 + address1 + components + URL_PART_2 )
		url2 = ( URL_PART_1 + address2 + components + URL_PART_2 )
		url3 = ( URL_PART_1 + address3 + components + URL_PART_2 )
		url4 = ( URL_PART_1 + address4 + components + URL_PART_2 )
		
		# tries first geocode (locality 1, admin area, country)
		check2(address2, url2, administrative_area, locality1, country)
		
	elif street_address.count(',') == 1:
		# splits the source address into parts
		locality1, country = (street_address.split(','))
		locality2 = ""
		locality3 = ""
		administrative_area = ""
		# builds component restrictions
		components = '&components=locality:' + locality1.strip().replace(' ','%20').replace(',','') + "|country:" + country.strip().replace(' ','%20').replace(',','').replace('\n','')
		# builds address for tiered search (if most granular geocode result does not match source parts, try less granular until matched)
		address1 = locality1.replace(' ','%20').strip() + ",+" + country.replace(' ','%20').strip()
		address2 = ""
		address3 = ""
		address4 = ""
		url1 = ( URL_PART_1 + address1 + components + URL_PART_2 )
		url2 = ( URL_PART_1 + address2 + components + URL_PART_2 )
		url3 = ( URL_PART_1 + address3 + components + URL_PART_2 )
		url4 = ( URL_PART_1 + address4 + components + URL_PART_2 )
		
		# tries first geocode (locality 1-3, country)
		check1(address1, url1, administrative_area, locality1, country)
		
	# Checks if geocode locality result equals source locality for most granular address
	def check4(address4, url4, administrative_area, locality1, country):
		# if address4 was built, check for locality match
		if len(address4) > 0:	
			# Makes the API call and returns data
			try:
				urllib2.urlopen(url4)
				response = urllib.urlopen( url4 )
				data = json.loads(response.read())
				note = ""
					
				if data["status"] == 'OK':
					if address_components == 3:
						resultLocality = data["results"][0]["address_components"][0]["short_name"].encode('utf-8')
					
					# If not OK, check next address
					else:
						check3(address3, url3, administrative_area, locality1, country)
						
					# returns result for locality match
					if resultLocality == locality1:
						url = url4
						returnResults(data, url4, locality1, administrative_area, country)
					# if no match, go to less detailed geocode attempt
					else:
						check3(address3, url3, administrative_area, locality1, country)
					
			# Catches server errors, tries less detailed geocode attempt
			except urllib2.HTTPError, e:
				check3(address3, url3, administrative_area, locality1, country)
			except urllib2.URLError, e:
				check3(address3, url3, administrative_area, locality1, country)

	# Checks if geocode locality result equals source locality for most granular address
	def check3(address3, url3, administrative_area, locality1, country):
		if len(address3) > 0:	
			# Makes the API call and returns data
			try:
				urllib2.urlopen(url3)
				response = urllib.urlopen( url3 )
				data = json.loads(response.read())
				note = ""
					
				if data["status"] == 'OK':
					if address_components == 3:
						resultLocality = data["results"][0]["address_components"][0]["short_name"].encode('utf-8')
						
					# If not OK, check next address
					else:
						check2(address2, url2, administrative_area, locality1, country)
						
					# returns result for locality match
					if resultLocality == locality1:
						url = url3
						returnResults(data, url3, locality1, administrative_area, country)
					# if no match, go to less detailed geocode attempt
					else:
						check2(address2, url2, administrative_area, locality1, country)
						
			# Catches server errors, tries less detailed geocode attempt
			except urllib2.HTTPError, e:
				check2(address2, url2, administrative_area, locality1, country)
			except urllib2.URLError, e:
				check2(address2, url2, administrative_area, locality1, country)
						
	# Checks if geocode locality result equals source locality for most granular address
	def check2(address2, url2, administrative_area, locality1, country):
		if len(address2) > 0:	
			# Makes the API call and returns data
			try:
				urllib2.urlopen(url2)
				response = urllib.urlopen( url2 )
				data = json.loads(response.read())
				note = ""
					
				if data["status"] == 'OK':
					if address_components == 3:
						resultLocality = data["results"][0]["address_components"][0]["short_name"].encode('utf-8')
						
					# If not OK, check next address
					else:
						check1(address1, url1, administrative_area, locality1, country)
						
					# returns result for locality match
					if resultLocality == locality1:
						url2 = url
						returnResults(data, url, locality1, administrative_area, country)
					# if no match, go to less detailed geocode attempt
					else:
						check1(address1, url1, administrative_area, locality1, country)
						
			# Catches server errors, tries less detailed geocode attempt
			except urllib2.HTTPError, e:
				check1(address1, url1, administrative_area, locality1, country)
			except urllib2.URLError, e:
				check1(address1, url1, administrative_area, locality1, country)

	# Checks if geocode locality result equals source locality for most granular address
	def check1(address1, url1, administrative_area, locality1, country):
		if len(address1) > 0:	
			# Makes the API call and returns data
			try:
				urllib2.urlopen(url1)
				response = urllib.urlopen( url1 )
				data = json.loads(response.read())
				note = ""
					
				if data["status"] == 'OK':
					if address_components == 3:
						resultLocality = data["results"][0]["address_components"][0]["short_name"].encode('utf-8')
						
					# If not OK, check next address
					else:
						check0(locality1, administrative_area, country)
						
					# returns result for locality match
					if resultLocality == locality1:
						url = url1
						returnResults(data, url, locality1, administrative_area, country)
					# if no match, go to less detailed geocode attempt
					else:
						check0(locality1, administrative_area, country)
						
			# Catches server errors, tries less detailed geocode attempt
			except urllib2.HTTPError, e:
				check0(locality1, administrative_area, country)
			except urllib2.URLError, e:
				check0(locality, administrative_area, country)

	# Returns failed geocodes
	def check0(locality,administrative_area, country):
		#return street_address.replace('\n','') + "\t" + str(locality1.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()).replace('\n','') + "\t" + "Fail" + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + note				
		return "" + "\t" + str(locality1.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()) + "\t" + "Fail" + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + "" + "\t" + note				
				
	# Process successful geocode match
	def returnResults(data, url, locality1, administrative_area, country):
		if data["status"] == 'OK':
			resultGeomType = data["results"][0]["geometry"]["location_type"]
			resultLat = data["results"][0]["geometry"]["location"]["lat"]
			resultLon = data["results"][0]["geometry"]["location"]["lng"]
			address_components = len(data["results"][0]["address_components"])
					
			# checks what components were returned
			if address_components == 3:
				resultLocality = data["results"][0]["address_components"][0]["short_name"].encode('utf-8')
				resultAdminArea1 = data["results"][0]["address_components"][1]["long_name"].encode('utf-8')
				resultCountry = data["results"][0]["address_components"][2]["long_name"].encode('utf-8')
						
			else:
				resultLocality = data["results"][0]["address_components"][0]["short_name"].encode('utf-8')
				resultAdminArea1 = ""
				resultCountry = data["results"][0]["address_components"][1]["long_name"].encode('utf-8')
		
		if str(resultGeomType) == 'APPROXIMATE':
			resultFormatted = data["results"][0]["address_components"][0]["long_name"].encode('utf-8')
		else:
			resultFormatted = data["results"][0]["formatted_address"].encode('utf-8')
		
		# returns successful  geocode result to be written to file
		return "" + "\t" + str(locality1.strip()) + "\t" + str(administrative_area.strip()) + "\t" + str(country.strip()) + "\t" + str(data["status"]) + "\t" + str(resultGeomType) + "\t" + str(resultLat) + "\t" + str(resultLon) + "\t" + str(resultFormatted) + "\t" + url + "\t" + note
		
def main():
	run_noDups()

if __name__ == "__main__":
	main()