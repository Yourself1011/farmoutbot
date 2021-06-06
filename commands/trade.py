#TEMPERARY THING IGNORE FOR NOW	TEMPORARY*

from replit import db
import pprint
from zstats import animals, seeds, merch, tools
import time
from math import floor
from random import randint

async def trade(message, client):
	if str(message.author.id) not in db['members']:
		await message.channel.send('market: make an account first u dumum')
		return

	user = db["members"][str(message.author.id)]
	if user["trades"]["lastTradeId"] != db["tradeId"]:

		m = db["members"]

		m[str(message.author.id)]["trades"] = {"lastTradeId": db["tradeId"], "tradeAmts": [0, 0, 0, 0, 0], "stock": [floor((user["reputation"]/randint(200, 300))*10), floor((user["reputation"]/randint(200, 300))*4), floor(user["reputation"]/randint(200, 300)), floor(user["reputation"]/randint(300, 400)), floor(user["reputation"]/randint(400, 500))]}

		db["members"] = m
	user = db["members"][str(message.author.id)]

	args = message.content.split(' ')
	if len(args) == 2:
		await message.channel.send('what trade are you doing lol')
		return
	
	if db['members'][str(message.author.id)]['reputation'] < 350:
		await message.channel.send('gotta have at least `350` rep to do trades')
		return
	if not args[2].isnumeric() or int(args[2]) not in [0, 1, 2, 3, 4]:
		await message.channel.send(f'say a number from 0 to 4 not {args[2]} dumbo')
		return
	trade = int(args[2])
	if user["trades"]["tradeAmts"][trade] >= user["trades"]["stock"][trade]:
		await message.channel.send("Sorry, Mr. Trader dude here has run out of that trade for you. Come back tommorow though.")
		return
	for i in db['trades'][trade]['give']:
		for j in [animals, seeds, merch]:
			if i[2] in j:
				thing = j
		if i[2] not in db['members'][str(message.author.id)][thing['name']]:
			await message.channel.send(f'you dont have any {i[2]}, get that first dumum')
			return
		if thing in [animals, seeds]:
			if i[1] > db['members'][str(message.author.id)][thing['name']][i[2]]['amount']:
				await message.reply(f'you do not have enough {i[2]}(s), get more first')
				return
		if thing == merch:
			if i[1] > db['members'][str(message.author.id)][thing['name']][i[2]]:
				await message.reply(f'You do not have enough {i[2]}(s), get more first')
				return

	a = db['members']
	a[str(message.author.id)]["trades"]["tradeAmts"][trade] += 1
	for i in db['trades'][trade]['give']:
		for j in [animals, seeds, merch]:
			if i[2] in j:
				thing = j
		if thing in [animals, seeds]:
			a[str(message.author.id)][thing['name']][i[2]]['amount'] -= i[1]
			if a[str(message.author.id)][thing['name']][i[2]]['amount'] == 0:
				del a[str(message.author.id)][thing['name']][i[2]]
		if thing == merch:
			a[str(message.author.id)][thing['name']][i[2]] -= i[1]
			if a[str(message.author.id)][thing['name']][i[2]] == 0:
				del a[str(message.author.id)][thing['name']][i[2]]
	db['members'] = a
	a = db['members']
	for i in db['trades'][trade]['get']:
		for j in [animals, tools, seeds, merch]:
			if i[2] in j:
				thing = j
		if thing in [animals, seeds]:
			if i[2] in db['members'][str(message.author.id)][thing['name']]:
				a[str(message.author.id)][thing['name']][i[2]]['amount'] += i[1]
			else:
				if thing == animals:
					now = int(round(time.time()*1000))
					a[str(message.author.id)][thing['name']][i[2]] = {
						'amount': i[1],
						'lastused': now
					}
				if thing == seeds:
					a[str(message.author.id)][thing['name']][i[2]] = {'amount':i[1]}
		if thing == tools:
			a[str(message.author.id)]['tools'][i[2]] = tools[i[2]]['durability']
		if thing == merch:
			if i[2] in db['members'][str(message.author.id)][thing['name']]:

				a[str(message.author.id)]['merch'][i[2]] += i[1]
			else:
				a[str(message.author.id)]['merch'][i[2]] = i[1]
	
	reps = {0: [0, 5], 1: [7, 15], 2: [20, 35], 3: [35, 45], 4: [50, 60]}
	repGain = round(randint(reps[trade][0], reps[trade][1])/3)
	a[str(message.author.id)]['reputation'] += repGain

	db['members'] = a
	await message.channel.send(f'{message.author.mention} did trade `{trade}`.\n**market:**\nTank yoo fer trading wees us, heers {repGain} rep')