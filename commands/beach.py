from replit import db
from time import time
from math import floor
from random import randint
import random
from zstats import gatheringCmd, merch, tools, seeds, animals

async def beach(message, client):
	user = str(message.author.id)
	if user not in db['members']: await message.channel.send('make an account to search the beach'); return
	user = db["members"][str(message.author.id)]
	if "gather" in user["cooldowns"] and user["cooldowns"]["gather"] > time():
		await message.channel.send(f"you already gathered stuff, wait {floor(user['cooldowns']['gather'] - time())}s")
		return
	
	if 'sandals' not in user['tools']:
		await message.channel.send('buy sandals')
		return

	thing = random.randint(1,35)
	if thing == 1:
		things = ['bug', 'fish', 'tree', 'plant', 'elephant', 'neighbour']
		thing2 = random.choice(things)
		await message.channel.send(f'On the way over to the beach, you accidentally smelled a really smelly {thing2} and died. you paid 100 coins to be reborn.')
		a = db['members']
		if a[str(message.author.id)]['money']<100: a[str(message.author.id)]['money'] = 0
		else:
			a[str(message.author.id)]['money'] -= 100
		db['members'] = a
		return

	item = gatheringCmd(
		message,
		{
			'death': [20, 1, 1, 1],
			'voldysnose': [10, 2, 1, 3],
			'umbrella': [20, 5, 1, 1],
			"gineseng": [3, 2, 1, 10],	
			"nothing": [50, 1, 1, 1],
		}
	)
	
	m = db["members"]
	user = m[str(message.author.id)]
	if item[0] != 'death':
		if item[0] in merch:
			if item[0] in user["merch"]:
				user["merch"][item[0]] += item[1]

			else:
				user["merch"][item[0]] = item[1]
			itemName = merch[item[0]]["name"]

		elif item[0] in seeds:
			if item[0] in user["seeds"]:
				user["seeds"][item[0]]["amount"] += item[1]

			else:
				user["seeds"][item[0]]["amount"] = item[1]
			itemName = seeds[item[0]]["name"]

	breakAmt = randint(3, 6)

	user["tools"]["hikingboots"] -= breakAmt
	
	if user["tools"]["sandals"] <= 0:
		del user["tools"]["sandals"]
		durabilityMsg = "Your sandals broke!"
	else:
		durabilityMsg = f"Your sandals lost {breakAmt} durability! They are now at {user['tools']['hikingboots']} durability."

	reserveMsg = ""
	if not bool(randint(0, 7)):
		fine = randint(floor(user["money"] / 10), floor(user["money"] / 4))

		user["money"] -= fine
		reserveMsg = f"You accidentally sneezed at a shark and died. You paid {fine} to be reborn."

	user["cooldowns"]["gather"] = time() + 60

	db["members"] = m

	if item[0] == "dragonegg":
		await message.channel.send(f"You looked at the beach, and there, in a pile of sand, you saw it. A small piece of ginseng.\n{durabilityMsg}\n{reserveMsg}")

	elif item[0] == "nothing":
		await message.channel.send(f"You found nothing on the beach\n{durabilityMsg}\n{reserveMsg}")

	elif item[0] == 'death':
		await message.channel.send('You were searching the beach when, all of a sudden, a huge horde of seagulls swooped down on you and pecked you to death. you paid 100 coins to be reborn.')
		m = db['members']
		m[str(message.author.id)]['money'] -= 100
		db['members'] = m

	else:
		responses = ["looked on the beach and found", "walked around a little and picked up", "discovered", "found", "looked in a sand castle and found"]
		await message.channel.send(f"You {responses[randint(0, len(responses)-1)]} {item[1]}x {itemName}\n{durabilityMsg}\n{reserveMsg}")	