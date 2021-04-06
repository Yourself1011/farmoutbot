from replit import db
import discord
from zstats import emojis, convertInt
import random

async def slots(message, client):
	if str(message.author.id) not in db['members']:
		await message.reply('make an account to play slots!')
		return
	args = message.content.split(' ')
	if len(args) == 2:
		await message.channel.send('gotta bet something for slots to work')
		return

	amount = convertInt(args[2])

	if args[2] in ['a', 'all', 'max']:
		amount = db['members'][str(message.author.id)]['money']
		
	if not bool(amount):
		await message.channel.send('put a number?')
		return
	if amount > db['members'][str(message.author.id)]['money']:
		await message.channel.send('you can only bet as much as you have, no more')
		return
	if amount <= 0:
		await message.channel.send(f'how u gonna bet `{amount}` coins dumbo')
		return
	
	g = random.choice(emojis)
	h = random.choice(emojis)
	i = random.choice(emojis)
	if g == h == i:
		a = db['members']
		a[str(message.author.id)]['money'] += amount*5
		db['members'] = a
		fat = f'oh wow you won {amount*5} coins'
	else:
		fat = f'lmao you lost {amount} coins'
		a= db['members']
		a[str(message.author.id)]['money'] -= amount
		db['members'] = a
	
	thingr = f'{g}, {h}, {i}'
	e = discord.Embed(
		title = f'{message.author.name}\'s slots game',
		description = thingr,
		colour = discord.Colour.red()
	)
	e.set_footer(text = fat)
	await message.channel.send(embed = e)