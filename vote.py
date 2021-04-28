from replit import db
from time import time

def vote(id, site):
	a = db["members"]
	user = a[id]
	user["cooldowns"][site] = (time + 43200) * 10

	db["members"] = a