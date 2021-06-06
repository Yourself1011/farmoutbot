import discord
import random
from replit import db

async def onthefence(message, client):
	return
	if str(message.author.id) not in db['members']:
		await message.channel.send('mm mm mm make an account first')
		return
	args = message.content.split(' ')
	if len(args) == 2:
		await message.channel.send('what are you betting lol')
		return
	if not args[2].isnumeric():
		await message.channel.send('bruh bet a number stupid')
		return
	if int(args[2]) < 0:
		await message.channel.send('https://media.tenor.co/videos/e0b51ead5f9fd990f06a5582cdc996bf/mp4')
		return
	betted = int(args[2])
	if 'otfscore' not in db['members'][str(message.author.id)]:
		db['members'][str(message.author.id)]['otfscore'] = 0
	score = db['members'][str(message.author.id)]['otfscore']
	thing = random.randint(-50,50)
	if thing < score:
		await message.channel.send(f'you won `{betted*2} coins')
		a = db['members']
		a[str(message.author.id)]['money'] += betted
		thing = random.randint(-50,50)
		if thing < score:
			a[str(message.author.id)]['otfscore'] -= 2
		if thing > score: a[str(message.author.id)]['otfscore'] += 2
		if a[str(message.author.id)]['otfscore'] > 50: a[str(message.author.id)]['otfscore'] = 50
		if a[str(message.author.id)]['otfscore'] < -50: a[str(message.author.id)]['otfscore'] = -50
		db['members'] = a
	if thing > score:
		await message.channel.send(f'oof you lost `{betted}` coins')
		a = db['members']
		a[str(message.author.id)]['money'] += betted
		thing = random.randint(-50,50)
		if thing < score:
			a[str(message.author.id)]['otfscore'] -= 2
		if thing > score: a[str(message.author.id)]['otfscore'] += 2
		db['members'] = a
		if a[str(message.author.id)]['otfscore'] > 50: a[str(message.author.id)]['otfscore'] = 50
		if a[str(message.author.id)]['otfscore'] < -50: a[str(message.author.id)]['otfscore'] = -50