from replit import db

async def setchannel(message, client):
	if not message.author.guild_permissions.manage_guild:
		await message.channel.send(f'gotta have `Manage Server` perms for that')
		print(f'{message.author.name} tried to set channel with no perms')
	else:
		args = message.content.split(' ')
		if len(args) == 2:
			await message.channel.send('gotta specify a channel dummy')
			return
		if not args[2].startswith('<#') and args[2].endswith('>'):
			await message.channel.send('mention a channel for this to work')
			return
		channel = args[2].strip('<#')
		channel = channel.strip('>')
		a = db['server']
		a[str(message.guild.id)]['channel'] = int(channel)
		db['server'] = a
		server = message.guild.name
		channel = db['server'][str(message.guild.id)]['channel']
		await message.channel.send(f'The system messages channel for `{server}` is now <#{channel}>.')