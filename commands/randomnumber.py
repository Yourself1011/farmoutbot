import random
from replit import db

async def randomnumber(message, client):
	args = message.content.split(' ')
	if str(message.author.id) not in db['members']:
		await message.channel.send('M A K E A N A C C O U N T')
		return
	if len(args) == 2:
		await message.channel.send('what number do you think it is lol')
		return
	if db['members'][str(message.author.id)]['reputation'] > 1000:
		await message.channel.send('your reputation is too high to gamble,go do something better with your money')
		return
	number = int(args[2])
	num2 = random.randint(1, 20)
	if number == num2:
		a = db['members']
		a[str(message.author.id)]['money'] += 50
		await message.channel.send('thats right, 50 coins for you')
		a[str(message.author.id)]['amounts']['gambled'] += 50
		db['members'] = a
		return
	if number != num2:
		a = db['members']
		lost = random.randint(1,3)
		if a[str(message.author.id)]['money'] < lost:
			a[str(message.author.id)]['money'] = 0
		else:
			a[str(message.author.id)]['money'] -= lost
			a[str(message.author.id)]['amounts']['gambled'] -= lost 
		db['members'] = a
		await message.channel.send(f'you guessed `{number}` and the number was `{num2}`, you lost `{lost}` coins.')
