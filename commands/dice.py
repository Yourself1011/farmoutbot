from replit import db
import random
import discord
from zstats import convertInt

async def dice(message, client):
	if str(message.author.id) not in db['members']:
		await message.channel.send('::')
		return
	args = message.content.split(' ')
	if len(args) == 2:
		await message.channel.send('you gotta bet something bro')
		return

	if args[2] in ['a', 'all', 'max']:
		amount = db['members'][str(message.author.id)]['money']
		if db['members'][str(message.author.id)]['money'] > 100000:
			amount = 100000
	else:
		amount = convertInt(args[2])
		if not bool(amount):
			await message.channel.send("bet a number")
			return

	if amount > db['members'][str(message.author.id)]['money']:
		await message.channel.send('thats more than u have lol')
		return
	if db['members'][str(message.author.id)]['reputation'] > 1000:
		await message.channel.send('your reputation is too high to gamble,go do something better with your money')
		return
	if db['members'][str(message.author.id)]['money'] == 0:
		await message.channel.send('You have no money. \'-\'')
		return
	if amount <= 0:
		await message.channel.send('can\'t bet less than 0')
		return
	you = random.randint(1,6)
	other = random.randint(1,6)
	a = db['members']
	a[str(message.author.id)]['amounts']['gambled'] += amount
	db['members'] = a
	thing = ''
	if you > other:
		a = db['members']
		a[str(message.author.id)]['money'] += amount
		amount = f'+{int(amount)}'
		thing = 'won'
		db['members'] = a
	if other > you:
		a = db['members']
		a[str(message.author.id)]['money'] -= amount
		amount = f'-{amount}'
		thing = 'lost'
		db['members'] = a
	if other == you:
		thing = 'tied'
		amount = '+0'
		await message.channel.send(f'{message.author.mention} you got `{you}` and they got `{other}`, nothing happened. :/')
		return
	e = discord.Embed(
		title = '',
		description = f'You {thing}, (coins {amount})',
		colour = discord.Colour.red()
	)
	e.set_author(name=f'{message.author.name}\'s dice game', icon_url=message.author.avatar_url)

	e.add_field(name = '- Your Score: ', value = f'{you}', inline = False)
	e.add_field(name = '- Their Score: ', value = f'{other}', inline = False)
	e.set_footer(text = 'please come again!')
	await message.channel.send(embed = e)