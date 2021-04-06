import random

async def fart(message, client):
	args = message.content.split(' ')
	thing = random.randint(1,50)
	if thing == 1:
		await message.channel.send('no fart came out. everyone evacuated anyway')
		return
	else:
		if len(args) == 2:
			await message.channel.send(f'ahh {message.author.mention} farteddd everyone evacuate')
		if len(args) > 2:
			args.pop(0)
			args.pop(0)
			args = ' '.join(args)
			await message.channel.send(f'lmao {message.author.mention} farted on {args}')