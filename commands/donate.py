from replit import db
from zstats import convertInt

async def donate(message, client):
	print('hi')
	args = message.content.split(' ')
	if str(message.author.id) not in db['members']:
		await message.channel.send('you don\'t exist LOL')
		return
	if len(args) == 2:
		await message.channel.send('how much are you donating lol')
		return
	if db['members'][str(message.author.id)]['money'] == 0:
		await message.channel.send('you have no money, dummy')
		return

	gave = convertInt(args[2])
	if not bool(gave) and args[2] not in ['a', 'all', 'max']:
		await message.channel.send('gotta say a number')
		return
	if gave > db['members'][str(message.author.id)]['money']:
		await message.channel.send('you don\'t have that much')
		return
	if gave == 0:
		await message.channel.send('how you gonna give 0 coins u dumdum')
		return
	
	if args[2] in ['all', 'a', 'max']:
		gave = db['members'][str(message.author.id)]['money']
	if gave <= 0:
		await message.channel.send('cant donate less than 1')
		return

	if db['members'][str(message.author.id)]['reputation'] >= 750:
		await message.channel.send('your reputation is too high, thanks for the free money nerd')
		a = db['members']
		a[str(message.author.id)]['money'] -= gave
		db['members'] = a
		return

	a = db['members']
	a[str(message.author.id)]['money'] -= gave
	repgained = int(round(gave/3))
	a[str(message.author.id)]['reputation'] += repgained
	if a[str(message.author.id)]['reputation'] > 1000:
		repgained = 1000
		a[str(message.author.id)]['reputation'] = 1000
	nowmoney = a[str(message.author.id)]['money']
	nowrep = a[str(message.author.id)]['reputation']
	db['members'] = a
	await message.reply(f'You gave `{gave}` coins to the marketplace. Your reputation increased by `{repgained}`. \nYou now have `{nowmoney}` coins and `{nowrep}` reputation.')