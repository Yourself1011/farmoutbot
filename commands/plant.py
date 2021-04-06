from replit import db
from zstats import seeds, tools, softSearch, convertInt
import asyncio
import random
import time 

async def plant(message, client):
	args = message.content.split(' ')
	if str(message.author.id) not in db['members']:
		await message.channel.send(' n o ')
		return
	if db['members'][str(message.author.id)]['seeds'] == {}:
		await message.channel.send(' n o ')
		return
	if len(args) == 2:
		await message.channel.send(' what are you planting lol')
		return
	seed = softSearch(seeds, args[2], ["name"])
	if not bool(seed):
		await message.channel.send('don\'t try to fool me, that\'s not a seed')
		return
	if seed not in db['members'][str(message.author.id)]['seeds']:
		await message.channel.send(' you dont have that')
		return
		
	tool = None
	for i in tools:
		if tools[i] != 'tools':
			if tools[i]['animal'] == 'seed':
				if tools[i]['name'] in db['members'][str(message.author.id)]['tools']:
					tool = tools[i]['name']
	if tool == None:
		await message.channel.send(' buy a watering can first')
		return
	
	if len(args) == 3:
		amount = 1
	if len(args) == 4 and args[3] in ['a', 'all', 'max']:
		amount = db['members'][str(message.author.id)]['seeds'][seed]['amount']
	elif len(args) == 4:
		amount = convertInt(args[3])
		if not bool(amount):
			amount = 1
	if amount <= 0:
		await message.channel.send(' cant be less than 0 bro')
		return
	
	if amount > db['members'][str(message.author.id)]['seeds'][seed]['amount']:
		await message.channel.send(' thats more than you have nerd')
		return
	if seeds[seed]['result'] in db['members'][str(message.author.id)]['plantcooldowns']:
		await message.channel.send(' you already planted that, go collect it first')
		return
	if amount >= db['members'][str(message.author.id)]['tools'][tool]:
		amount = db['members'][str(message.author.id)]['tools'][tool]
		a = db['members']
		del a[str(message.author.id)]['tools'][tool]
		db['members']  =a
		await message.channel.send(f'your {tool} broke LOL')
	else:
		a = db['members']
		a[str(message.author.id)]['tools'][tool] -= amount
		db['members']  =a

	things = ['water', 'watering', 'undie', 'hydrate', 'sea', 'ocean', 'water', 'drink', 'plant', 'water', 'slurp', 'ice', 'snow', 'pool', 'lake']
	thingtotype = random.choice(things)
	await message.channel.send(f'{message.author.name} you\'re planting `{amount} {seed}(s)`, but plants need water, type `{thingtotype}` in the chat now')
	
	channel = message.channel

	reply = None

	def check(m):
		return m.content.lower() == thingtotype and m.author.id == message.author.id

	try:	
		reply = await client.wait_for('message', timeout=10.0, check=check)
	except asyncio.TimeoutError:
		await channel.send('idiot your plants died')
		a = db['members']
		a[str(message.author.id)]['seeds'][seed]['amount'] -= amount
		if a[str(message.author.id)]['seeds'][seed]['amount'] == 0:
			del a[str(message.author.id)]['seeds'][seed]
		db['members'] = a
		return
	else:
		amountwait = seeds[seed]["stages"][0] if "stages" in seeds[seed] else seeds[seed]['growtime']
		prefix = db['server'][str(message.guild.id)]['prefix']
		plantr = seeds[seed]['result']
		tts = [f' You watered your plants. Wait `{amountwait/1000}` seconds before collecting them, and use `{prefix} collect {plantr}` to collect them.', f'yessir, plants are watered and are now growing, see them using `{prefix} crops`', f'plants are successfully watered. they will be ready to collect in `{amountwait/1000}`s.', f'plants watered. be sure to collect them in `{amountwait/1000}s` using `{prefix} collect {plantr}`.']
		tt = random.choice(tts)
		await message.reply(tt)
		a = db['members']
		now = int(round(time.time()*1000))
		a[str(message.author.id)]['plantcooldowns'][seeds[seed]['result']] = {
			'name': seeds[seed]['name'],
			'cooldown': now,
			'amount': amount
		}
		if "stages" in seeds[seed]: 
			a[str(message.author.id)]['plantcooldowns'][seeds[seed]['result']]["start"] = now
			a[str(message.author.id)]['plantcooldowns'][seeds[seed]['result']]["stage"] = 0

			
		a[str(message.author.id)]['seeds'][seed]['amount'] -=amount
		if a[str(message.author.id)]['seeds'][seed]['amount'] == 0:
			del a[str(message.author.id)]['seeds'][seed]
		db['members'] = a