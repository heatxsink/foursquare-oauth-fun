#!/usr/bin/python
import math
import time
import oauth
import foursquare
import os.path

VENUE_FILE_CACHE = 'path_to_venue_cache_file'
oauth_key = "oauth-key-here";
oauth_secret = "oauth-secret-here";
access_token_key = "oauth-access-token-key-here"
access_token_secret = "oauth-access-token-secret-here"

def load_venue_cache(four_square):	
	if not venue_cache_exists():
		vids =[266773, 513144, 1025595, 95005]
		for vid in vids:
			venue = four_square.venue(vid)
			print venue['venue']['id']
			print venue['venue']['name']
			print venue['venue']['geolat']
			print venue['venue']['geolong']
			print '------'
			venue_line = []
			venue_line.append(str(venue['venue']['id']))
			venue_line.append(str(venue['venue']['name']))
			venue_line.append(str(venue['venue']['geolat']))
			venue_line.append(str(venue['venue']['geolong']))
			fs = open(VENUE_FILE_CACHE, 'a')
			line = ','.join(venue_line)
			fs.write(line)
			fs.write('\n')
			fs.close()
	venue_list = {}
	fs = open(VENUE_FILE_CACHE, 'r')
	for line in fs:
		line = line.strip('\n')
		venue_data = line.split(',')
		id = venue_data[0]
		name = venue_data[1]
		lat = venue_data[2]
		long = venue_data[3]
		venue_list[name] = dict(id=id, name=name, lat=lat, long=long)
	return venue_list

def venue_cache_exists():
	if os.path.exists(VENUE_FILE_CACHE):
		return True
	else:
		return False

def is_in_bounding_box(lat, long):
	ul_lat = 34.0765508
	ul_long = -118.394656
	lr_lat = 34.075810
	lr_long = -118.393634

def move_lat_long(latitude, longitude, distance, bearing):
	bearing = convert_to_radians(bearing)
	latitude = convert_to_radians(latitude)
	longitude = convert_to_radians(longitude)
	# earths radius in kilometers
	earth_radius = 6371
	d = float(distance) / float(earth_radius)
	latitude2 = math.asin(math.sin(latitude) * math.cos(d) + math.cos(latitude) * math.sin(d) * math.cos(bearing))
	longitude2 = longitude + math.atan2(math.sin(bearing) * math.sin(d) * math.cos(latitude), math.cos(d) - math.sin(latitude) * math.sin(latitude2))
	return convert_to_degrees(latitude2), convert_to_degrees(longitude2)

def convert_to_degrees(number):
	return (float(number) * (180/math.pi))

def convert_to_radians(number):
	return (float(number) * (math.pi/180))

def expand_geo_coordinate(coordinate):
	geo_coordinate = float(coordinate)
	geo_degrees = int(geo_coordinate)
	geo_minutes = (abs(geo_coordinate) % abs(geo_degrees)) * 60
	geo_seconds = (geo_minutes % int(geo_minutes)) * 60
	random_format = "[%s]  %d degrees   %d minutes   %d seconds"
	return random_format % (coordinate, geo_degrees, geo_minutes, geo_seconds)

def check_in(fs, id, lat=None, long=None):
	checkin = fs.checkin(vid=id)
	#checkin = fs.checkin(vid=venue['id'], geolat=venue['lat'], geolong=venue['long'])
	print checkin['checkin']['message']
	print checkin['checkin']['mayor']['message']

def main():
	fs = foursquare.Foursquare(foursquare.OAuthCredentials(oauth_key, oauth_secret))
	fs.credentials.set_access_token(oauth.OAuthToken(access_token_key, access_token_secret))
	venues = load_venue_cache(fs)
	for v in venues.keys():
		venue = venues[v]
		print venue['name']
		#print move_lat_long(venue['lat'], venue['long'], 0.0009, 108.63)
		check_in(fs=fs, id=venue['id'])
		seconds = 300
		print "sleeping for %s" % (seconds)
		time.sleep(seconds)
	print 'done'

main()
