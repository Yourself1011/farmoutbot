from replit import db
from zstats import animals, tools, deaths, births
import time
import random
import asyncio

async def useanimal(message, animal, client, thing):
	if str(message.author.id) not in db['members']:
		await message.channel.send(' Make an account first, then worry about animals**')
		return
	if animal not in db['members'][str(message.author.id)]['animals']:
		await message.channel.send(' You don\'t have that :angry:')
		return
	tool = None
	for i in tools:
		if i != 'name':
			if tools[i]['animal'] == animal and tools[i]['name'] in db['members'][str(message.author.id)]['tools']:
				tool = tools[i]['name']
	if tool == None:
		r = animals[animal]['tool']
		await message.channel.send(f' buy a(n) `{r}` first')
		return

	now2 = int(round(time.time() * 1000))
	f = db['members'][str(message.author.id)]['animals'][animal]['lastused'] - now2
	f = str(f)
	newvar = animals[animal]['cooldown']+db['members'][str(message.author.id)]['animals'][animal]['lastused']
	e = round((newvar-now2)/1000)
	f = animals[animal]['cooldown']/1000
	if f-e <= 10:
		paid = random.randint(1,3)
		if db['members'][str(message.author.id)]['money'] < paid:
			paid = db['members'][str(message.author.id)]['money']
		await message.channel.send(f' You used your {animal} too early and hurt it. You paid `{paid}` coins for the medical bills')
		a = db['members']
		a[str(message.author.id)]['money'] -= paid
		db['members'] = a

	now = int(round(time.time()*1000))
	if db['members'][str(message.author.id)]['animals'][animal]['lastused'] + animals[animal]['cooldown'] > now:
		now2 = int(round(time.time() * 1000))
		f = db['members'][str(message.author.id)]['animals'][animal]['lastused'] - now2
		f = str(f)
		newvar = animals[animal]['cooldown']+db['members'][str(message.author.id)]['animals'][animal]['lastused']
		e = round((newvar-now2)/1000)
		await message.reply(f' Your {animal}(s) are not ready, wait `'+str(e)+'` seconds.')
		return

	a = db['members']
	amount = a[str(message.author.id)]['animals'][animal]['amount']
	for i in tools:
		if i != 'name':
			if (tools[i]['animal'] == animal or animal in tools[i]["animal"]) and tools[i]['name'] in db['members'][str(message.author.id)]['tools']:
				tool = tools[i]['name']
	if amount > db['members'][str(message.author.id)]['tools'][tool]:
		f = db['members'][str(message.author.id)]['tools'][tool]
		amount = f
		a = db['members']
		del a[str(message.author.id)]['tools'][tool]
		db['members'] = a
		things = ['LOL', 'u dum dum', 'ur fat', 'go donate to yogogiddap', 'idiot']
		thing = random.choice(things)
		await message.channel.send(f'your `{tool}` broke {thing}')
	else:
		a = db['members']
		a[str(message.author.id)]['tools'][tool] -= amount
		if a[str(message.author.id)]['tools'][tool] <= 0:
			del a[str(message.author.id)]['tools'][tool]
		db['members'] = a
	
	now = int(round(time.time()*1000))
	a = db['members']
	a[str(message.author.id)]['animals'][animal]['lastused'] = now
	merch = animals[animal]['result']
	if merch not in a[str(message.author.id)]['merch']:
		a[str(message.author.id)]['merch'][merch] = amount
	else:
		a[str(message.author.id)]['merch'][merch] += amount
	a[str(message.author.id)]['amounts']['used'] += amount
	thing = animals[animal]['thing']
	db['members'] = a
	cooldown = animals[animal]['cooldown']/1000
	await message.reply(f'You {thing}ed `{amount}` `{animal}(s)`, gaining `{amount}` `{merch}`. Wait `{cooldown}` seconds before {thing}ing your {animal} again')

	echance = random.randint(1,10)
	if echance >= 6:
		whatthingchance = random.randint(1, 10)
		if whatthingchance in [1, 2]:
			if amount > 11:
				death = random.choice(list(deaths.keys()))
				deadamount = random.randint(1,round(amount/5))
				thingtotype = deaths[death]
				await message.channel.send(f'Oh no! {message.author.mention}, {deadamount} of your {animal}s are trying to die {death}! quick, type `{thingtotype}` in the chat now!')

				channel = message.channel

				reply = None

				def check(m):
					return m.content.lower() == thingtotype.lower() and m.author.id == message.author.id

				try:	
					reply = await client.wait_for('message', timeout=10.0, check=check)
				except asyncio.TimeoutError:
					await channel.send('idiot your animals died')
					a = db['members']
					a[str(message.author.id)]['animals'][animal]['amount']-= deadamount
					if a[str(message.author.id)]['animals'][animal]['amount'] == 0:
						del a[str(message.author.id)]['animals'][animal]
					db['members'] = a
					return
				else:
					await channel.send('phew you saved ur animals in time')
					return

		elif whatthingchance in [3, 4, 5, 6]:
			if amount > 8:
				thingtotype = random.choice(births)
				await message.channel.send(f'{message.author.mention} ar ur animals are trying to breed, better type `{thingtotype}` or else they won\'t')

				channel = message.channel

				reply = None

				def check(m):
					return m.content.lower() == thingtotype.lower() and m.author.id == message.author.id

				try:	
					reply = await client.wait_for('message', timeout=10.0, check=check)
				except asyncio.TimeoutError:
					await channel.send('idiot your animals didn\'t breed')
					return
				else:
					bornedamount = random.randint(1, round(amount/5))
					await channel.send(f'oop {bornedamount} {animal}(s) were born')
					a = db['members']
					a[str(message.author.id)]['animals'][animal]['amount'] += bornedamount
					db['members'] = a
					return