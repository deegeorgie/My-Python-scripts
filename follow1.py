import json

my_file = 'followers.json'

with open(my_file, 'r') as f:
	data = json.loads(str(f.read()))

	user_data = data["users"]
	count = 0
	for item in user_data:
		name = item["name"]
		user_name = item["screen_name"]
		creation_date = item["created_at"]
		language = item["lang"]
		friends = item["friends_count"]
		statuses = item["statuses_count"]
		print '--------------------------'
#		print 'Name: ', name
		print 'Username: ', user_name	
		print 'Creation date: ', creation_date
		print 'Number of friends: ', friends
		print 'Statuses: ', statuses
		count +=1
#print  user_name, name, creation_date, language
#print 'Friends: ', friends
#print 'Statuses: ', statuses

#	print json.dumps(data, indent=4)
print '-------------------------'
print 'done printing ', count, 'names'

