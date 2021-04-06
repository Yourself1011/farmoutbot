from replit import db

async def prefix(message, client):
	prefix = db['server'][str(message.guild.id)]['prefix']
	name = message.guild.name
	await message.channel.send(f'The prefix for `{name}` is `{prefix}`. use `{prefix} changeprefix` to change the prefix.')