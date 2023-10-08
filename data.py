import csv
import random
from datetime import datetime, timedelta

class Eclipse:
	def __init__(self, date, t, begins, ends, magnitude, obscuration, a_t_duration):
		self.date = date
		self.t = t
		self.begins = begins
		self.ends = ends
		self.magnitude = magnitude
		self.obscuration = obscuration
		self.a_t_duration = a_t_duration

	def get_type(self):
		if self.t == "P":
			self.t = "Partial"
		elif self.t == "A":
			self.t = "Annular"
		elif self.t == "T":
			self.t = "Total"
		return self.t
	
	def get_duration(self):
		b = self.begins.replace("(r)", ":00")
		e = self.ends.replace("(s)", ":00")
		time1 = datetime.strptime(b, "%H:%M:%S")
		time2 = datetime.strptime(e, "%H:%M:%S")

		# Calculate the difference between the two times
		time_difference = time2 - time1
		return time_difference

eclipses = []

with open('buffalo.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter='	', quotechar='|')
	for row in reader:
		e = Eclipse(row[0], row[1], row[2], row[9], row[11], row[12], row[13])
		eclipses.append(e)

def get_eclipse():
	eclipse = random.choice(eclipses)
	return eclipse

# print(eclipse.date)