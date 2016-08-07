#this script is authored by Georges BODIONG
import sys
import urllib
import twurl
import json

TWITTER_URL = 'https://api.twitter.com/1.1/search/tweets.json'

while True:
	print '-----------------------------------'
	q = raw_input('Enter your search query: ')
#	if (len(acct) < 1) : break

	url = twurl.augment(TWITTER_URL,
	 {'q' : q})
	print 'Retrieving', url
	connection = urllib.urlopen(url)
	data = connection.read()
	headers = connection.info().dict
	print '-----------------------------------'
	print 'Retrieved', len(data), 'characters'

	js = json.loads(data)

#	print json.dumps(js, indent=4)

	#persist data in the file system
	#in a file named followers.json
	with open('dBootcamp.json', 'w') as f:
    		json.dump(js, f)
    	print 'The operation was successful...'		
	print 'Remaining', headers['x-rate-limit-remaining']