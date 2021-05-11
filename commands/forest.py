from zstats import gatheringCmd, merch, tools, seeds, animals
from replit import db
from time import time
from math import floor
from random import randint
import random

async def forest(message, client):
	user = str(message.author.id)
	if user not in db['members']: await message.channel.send('make an account to search the forest'); return
	user = db["members"][str(message.author.id)]
	if "gather" in user["cooldowns"] and user["cooldowns"]["gather"] > time():
		await message.channel.send(f"you already gathered stuff, wait {floor(user['cooldowns']['gather'] - time())}s")
		return

	if "hikingboots" not in user["tools"]:
		await message.channel.send("buy hiking boots")
		return
	 
	thing = random.randint(1,35)
	if thing == 1:
		if 'undeadwool' in db['members'][str(message.author.id)]['merch']: return
		things = ['bug', 'fish', 'tree', 'plant', 'elephant', 'neighbour']
		thing2 = random.choice(things)
		await message.channel.send(f'On the way over to the forest, you accidentally saw a weird {thing2} and died. you paid 100 coins to be reborn.')
		a = db['members']
		if a[str(message.author.id)]['money']<100: a[str(message.author.id)]['money'] = 0
		else:
			a[str(message.author.id)]['money'] -= 100
		db['members'] = a
		return

	item = gatheringCmd(
		message,
		{
			"mushroom": [50, 10, 1, 2],
			"grass": [75, 10, 1, 3],
			"strawberry": [50, 10, 1, 2],
			"dragonegg": [5, 2, 1, 10],	
			"rarecoin": [10, 3, 1, 5],
			"pebble": [75, 15, 3, 2],
			"nothing": [50, 1, 1, 1],
		}
	)

	m = db["members"]
	user = m[str(message.author.id)]
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
	
	if user["tools"]["hikingboots"] <= 0:
		del user["tools"]["hikingboots"]
		durabilityMsg = "Your hikingboots broke!"
	else:
		durabilityMsg = f"Your hikingboots lost {breakAmt} durability! They are now at {user['tools']['hikingboots']} durability."

	reserveMsg = ""

	if not bool(randint(0, 7)):
		fine = randint(floor(user["money"] / 10), floor(user["money"] / 4))
		repLoss = randint(floor(user["reputation"] / 50), floor(user["reputation"] / 10))

		user["money"] -= fine
		user["reputation"] -= repLoss

		reserveMsg = f"You accidentally walked into an environmental reserve! You were fined {fine} and you lost {repLoss} reputation."

	user["cooldowns"]["gather"] = time() + 60

	db["members"] = m

	if item[0] == "dragonegg":
		await message.channel.send(f"You looked in the forest, and there, in a clearing, you saw it. {'A' if item[1] == 1 else 'Two'} dragon egg{'s' if item[1] == 2 else ''}\n{durabilityMsg}\n{reserveMsg}")

	elif item[0] == "nothing":
		await message.channel.send(f"You found nothing in the forest\n{durabilityMsg}\n{reserveMsg}")

	else:
		responses = ["looked in the forest and found", "walked around a little and picked up", "discovered", "picked", "looked in the stump of a dead tree and found"]
		await message.channel.send(f"You {responses[randint(0, len(responses)-1)]} {item[1]}x {itemName}\n{durabilityMsg}\n{reserveMsg}")	