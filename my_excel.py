import json

from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

#This is the json file containing our source data
#we parse it as a python dictionary(using json.loads method)
my_file = 'followers.json'
with open(my_file, 'r') as f:
	data = json.loads(str(f.read()))

#we initialize our workbook
#where the data will be saved in excel format
wb = Workbook()
dest_filename = 'followers.xlsx'
ws1 = wb.active
ws1.title = 'followers_info'

#naming the columns....
for col in range(1,6):
	ws1['A1'] = 'Name'
	ws1['B1'] = 'screen Name'
	ws1['C1'] = 'Creation date'
	ws1['D1'] = 'Language'
	ws1['E1'] = 'Number of friends'
	ws1['F1'] = 'Number of followers'
	ws1['G1'] = 'Number of statuses'

#subsetting our source file to retain the users'
#info only
user_data = data["users"]
count = 0
for item in user_data:
	name = item["name"]
	user_name = item["screen_name"]
	creation_date = item["created_at"]
	language = item["lang"]
	friends = item["friends_count"]
	followers = item["followers_count"]
	statuses = item["statuses_count"]

#	specify row values and populate workbook
	row = name, user_name, creation_date, language, friends, followers, statuses
	ws1.append(row)

	print '--------------------------'
	print 'Username: ', user_name	
	print 'Creation date: ', creation_date
	print 'Number of friends: ', friends
	print 'followers: ', followers
	print 'Statuses: ', statuses
	count +=1
#print  user_name, name, creation_date, language
#print 'Friends: ', friends
#print 'Statuses: ', statuses

#	print json.dumps(data, indent=4)
print '-------------------------'
print 'done printing ', count, 'names'


wb.save(filename = dest_filename)

print 'The whole operation was successful'