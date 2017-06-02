import json
import csv

my_file = 'followers.json'

with open(my_file, 'r') as f:
	data = json.loads(str(f.read()))

	user_data = data["users"]

	followers_data = open('followers.csv', 'w')
	csvwriter = csv.writer(followers_data)

	count = 0

	for item in user_data:
		if count == 0:
			header = item.keys()
			csvwriter.writerow(header)
			count += 1
		csvwriter.writerow(item.values())
	followers_data.close()