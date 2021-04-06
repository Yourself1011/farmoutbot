async def report(message, client):
	args = message.content.split(' ')
	if len(args) == 2:
		await message.reply('When reporting bugs, have a detailed description or send an image link.')
		return
	args.pop(0)
	args.pop(0)
	args = ' '.join(args)
	channel = client.get_channel(806178919409254450)
	name = await client.fetch_user(message.author.id)
	await channel.send(f'{name} has reported a bug: \n**[Farmout]** {args}')
	await message.add_reaction('✅')