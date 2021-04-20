from replit import db

async def lottery(message, client):
	if str(message.author.id) not in db['members']:
		return
	if message.author.id in db['lottery']:
		await message.channel.send('you\'re already in the lottery drumbo')
		return
	args = message.content.split(' ')
	if len(args) == 2:
		if db['members'][str(message.author.id)]['reputation'] < 250:
			await message.channel.send('your reputation is too low to participate in the lottery')
			return
		if db['members'][str(message.author.id)]['money'] < 100:
			await message.channel.send('get 100 coins to do the lottery')
			return
		a = db['members']
		await message.channel.send('alr you spent 100 coins to participate in the lottery, draws every 6 hours gl')
		a[str(message.author.id)]['money'] -= 100
		db['members'] = a
		a = db['lottery']
		a.append(message.author.id)
		db['lottery'] = a
	if len(args) == 3:
		if args[2].lower() == 'view':
			thing = len(db['lottery'])
			await message.channel.send(f'there are currently {thing} people in the lottery')
			return