from replit import db
import time
import datetime
import random
from zstats import dailys

async def daily(message, client):
	if str(message.author.id) not in db['members']:
		await message.channel.send('market: make an account first dumum')
		return
	args = message.content.split(' ')
	if len(args) != 2 and args[2] == 'show':
		lastdaily = db['members'][str(message.author.id)]['cooldowns']['lastdaily']
		await message.channel.send(f'your last daily was {lastdaily}')
		return
	now = int(round(time.time()*1000))
	if db['members'][str(message.author.id)]['cooldowns']['daily'] + 86400000 > now:		
		now2 = int(round(time.time() * 1000))
		f = db['members'][str(message.author.id)]['cooldowns']['daily'] - now2
		f = str(f)
		newvar = 86400000+db['members'][str(message.author.id)]['cooldowns']['daily']
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
	currentday = datetime.date.today().strftime('%Y-%m-%d')
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	yesterday.strftime('%m%d%y')
	print(currentday, yesterday)
	a = db['members']
	if db['members'][str(message.author.id)]['cooldowns']['lastdaily'] == yesterday: a[str(message.author.id)]['cooldowns']['streak'] += 1
	else: a[str(message.author.id)]['cooldowns']['streak'] = 0
	a[str(message.author.id)]['cooldowns']['lastdaily'] = currentday
	streak = a[str(message.author.id)]['cooldowns']['streak']
	if streak % 5 == 0:
		streak /= 5
	if streak == 1: streak = 1.25
	if not streak == 0:	moneygained = round(moneygained * streak)
	a[str(message.author.id)]['money']+=moneygained
	a[str(message.author.id)]['cooldowns']['daily'] = now
	db['members'] = a

	dail = random.choice(dailys)
	await message.channel.send(f'you gained `{moneygained}` coins {dail}\nyour current streak is `{streak} days in a row`')
	return