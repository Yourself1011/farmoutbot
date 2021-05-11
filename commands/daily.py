from replit import db
import time
import datetime
import random
from zstats import dailys

async def daily(message, client):
	if str(message.author.id) not in db['members']:
		await message.channel.send('market: make an account first dumum')
		return
	now = int(round(time.time()*1000))
	if db['members'][str(message.author.id)]['dailytimer'] + 86400000 > now:		
		now2 = int(round(time.time() * 1000))
		f = db['members'][str(message.author.id)]['dailytimer'] - now2
		f = str(f)
		newvar = 86400000+db['members'][str(message.author.id)]['dailytimer']
		e = round((newvar-now2)/1000)
		e = str(datetime.timedelta(seconds=e))

		await message.channel.send(f'market: it\'s called daily for a reason, wait `{e}` (hours:minutes:seconds) before coming back')
		return
	thing = random.randint(1,35)
	if db['members'][str(message.author.id)]['reputation'] < 250:
		await message.channel.send('market: nah, your reputation is too low so i\'m not giving you anything')
		chance = random.randint(1,5)
		if chance > 3:
			a = db['members']
			a[str(message.author.id)]['reputation']+=chance
			db['members'] = a
		return
	
	one = round(db['members'][str(message.author.id)]['reputation']/50)
	two = round(db['members'][str(message.author.id)]['reputation']/10)
	moneygained = random.randint(one, two)
	a = db['members']
	a[str(message.author.id)]['money']+=moneygained
	a[str(message.author.id)]['dailytimer'] = now
	db['members'] = a

	dail = random.choice(dailys)
	await message.channel.send(f'you gained `{moneygained}` coins {dail}')
	return