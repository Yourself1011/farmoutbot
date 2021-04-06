from replit import db

async def lottery(message, client):
	if str(message.author.id) not in db['members']:
		return
	await message.channel.send('no')