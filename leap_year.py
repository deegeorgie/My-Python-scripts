# Conditionals example
def is_leap_year(year):
	if (year % 400) == 0:
		return True
	elif (year % 100) == 0:
		return False
	elif (year % 4) == 0:
		return True
	else:
		return False

try:
	inp = raw_input("Enter a year please...")
	date = float(inp)
	leap_year = is_leap_year(year)
except:
	print "Please enter a valid date..."
	quit()
if leap_year:
	print year, "is leap year"
else:
	print year, "is not a leap year"
	
