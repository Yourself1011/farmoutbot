from replit import db

async def channel(message, client):
	name = message.guild.name
	channel = db['server'][str(message.guild.id)]['channel']
	if channel == None:
		await message.channel.send(f'`{name}` has not set a system messages channel.')
		return
	await message.channel.send(f'The system messages channel for `{name}` is <#{channel}>.')