from replit import db
from time import time
from zstats import animals, tools, merch, seeds
from math import floor

def vote(id, site):
	a = db["members"]
	user = a[id]
	user["cooldowns"][site] = (floor(time()) + 43200) * 10

	rewards = [["epicbox", 2]]

	for i in rewards:
		if i[0] in merch:
			if i[0] in user["merch"]:
				user["merch"][i[0]] += i[1]

			else:
				user["merch"][i[0]] = i[1]

	db["members"] = a