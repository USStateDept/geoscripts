import urllib
import json
from time import sleep

URL_PART_1 = 'http://maps.googleapis.com/maps/api/geocode/json?address='
URL_PART_2 = '&sensor=false'
INPUT_FILE = 'current730.txt'
OUTPUT_FILE= 'current73_locs2.txt'

def run():

	f=open(INPUT_FILE,'r')
	w=open(OUTPUT_FILE,'w')
	count = 0
	
	line = f.readline()
	while line :
		coord = getCoord(line)
		while coord == 'OVER_QUERY_LIMIT':
			sleep(1)
			coord = getCoord(line)
		print line.strip() + ": " + coord + "\n"		
		w.write(coord + "\n")
		count += 1
		line = f.readline()
		
	f.close()
	w.close()
	print count
	
def run_noDups():
	from linkedList import LinkedList
	f = open(INPUT_FILE,'r')
	w = open(OUTPUT_FILE,'w')
	count = 0
	lst = LinkedList()
	
	nation = f.readline()
	while nation :
		if lst.add(nation):
			coord = getCoord(nation)
			while coord == 'OVER_QUERY_LIMIT':
				sleep(1)
				coord = getCoord(nation)
			print nation.strip() + ": " + coord + "\n"						
			w.write(coord + "\n")
			count += 1
		nation = f.readline()
					
	f.close()
	w.close()
	print count + "unique nations were queried"	
		
def getCoord( nation ):
	
	ret_str = ""
	
	response = urllib.urlopen( URL_PART_1 + nation.replace(' ','+') + URL_PART_2 )
	data = json.loads(response.read())	
	
	if data["status"] == 'OK':
		lat = data["results"][0]["geometry"]["location"]["lat"]
		lon = data["results"][0]["geometry"]["location"]["lng"]		
		return str(lon) + "\t" + str(lat)
	
	elif data["status"] == 'OVER_QUERY_LIMIT':
		return 'OVER_QUERY_LIMIT'

	elif data["status"] == 'ZERO_RESULTS':
		return 'ZERO_RESULTS'
	else:
		return 'ERROR'

def main():
	run_noDups()


if __name__ == "__main__":
	main()


	
