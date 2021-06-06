from replit import db
import discord
from zstats import animals, tools, merch, seeds, getMember

async def inventory(message, client):
	args = message.content.split(' ')
	if len(args) == 2 and str(message.author.id) not in db['members']:
		await message.channel.send('Gotta make an account first dummy')
		return

	if len(args) >= 3 and args[2].lower() == 'stats':
		userObj = getMember(args[3:], message.guild.id, client)
		user = str(userObj.id) if userObj else False

		if len(args) == 3 or not user:
			user = str(message.author.id)

		if user not in db['members']:
			await message.channel.send(f'Ask {userObj.name}#{userObj.discriminator} to make an account first stupid')
			return
		name = await client.fetch_user(user)
		e = discord.Embed(
			title = f'',
			colour = discord.Colour.red()
		)
		e.set_author(name=f'{name	}\'s inventory stats:', icon_url=name.avatar_url)
		animaltotalunique = len(list(db['members'][user]['animals'].values()))
		animaltotal = 0
		for i in db['members'][user]['animals']:
			animaltotal += db['members'][user]['animals'][i]['amount']
		tooltotalunique = len(list(db['members'][user]['tools'].values()))
		merchtotalunique = len(list(db['members'][user]['merch'].values()))
		merchtotal = 0
		for i in db['members'][user]['merch']:
			merchtotal += db['members'][user]['merch'][i]
		e.add_field(name = '- :sheep: Animals ', value = f'Total: {animaltotal}\nUnique Total: {animaltotalunique}', inline = False)
		e.add_field(name = '- :hammer: Tools ', value = f'Total: {tooltotalunique}', inline = False)
		e.add_field(name = '- :moneybag: Merch ', value = f'Total: {merchtotal}\nUnique Total: {merchtotalunique}')
		prefix = db['server'][str(message.guild.id)]['prefix']
		e.set_footer(text = f'<{prefix} inv> for more info')
		await message.channel.send(embed=  e)
		return

	userObj = getMember(args[2:], message.guild.id, client)
	user = str(userObj.id) if userObj else False

	if len(args) == 2 or not user:
		user = str(message.author.id)

	if user not in db['members']:
		await message.channel.send(f'Ask {userObj.name}#{userObj.discriminator} to make an account first stupid')
		return

	name = await client.fetch_user(user)
	e = discord.Embed(
		title = f'',
		colour = discord.Colour.gold()
	)
	e.set_author(name=f'{name}\'s inventory:', icon_url=name.avatar_url)
	
	aout = []
	tout = []
	mout = []
	sout = []

	if db['members'][user]['animals'] == {}:	
		aout = None
	else:
		for i in db['members'][user]['animals']:
			c = db['members'][user]['animals'][i]['amount']
			kare=animals[i]['name']
			aout.append(f'{kare}: {c}')

		aout = "".join(  # Join an array together
			[
				# If the index is a multiple of, add a newline
				f"{val}\n" if (index + 1) % 5 == 0 else f"{val}, "
				for index, val in enumerate(aout)  # For every element in arr
			],
		)

	if db['members'][user]['tools'] == {}:
		tout = None
	else:
		for i in db['members'][user]['tools']:
			c = db['members'][user]['tools'][tools[i]['name']]
			name = tools[i]['name']
			tout.append(f'{name}: {c} durability')

		tout = "".join(  # Join an array together
			[
				# If the index is a multiple of, add a newline
				f"{val}\n" if (index + 1) % 3 == 0 else f"{val}, "
				for index, val in enumerate(tout)  # For every element in arr
			],
		)

	mercha = db['members'][user]['merch']
	if mercha == {}:
		mout = None
	else:
		for m in mercha:
			mout.append(f"{merch[m]['name']}: {str(mercha[m])}")

		mout = "".join(  # Join an array together
			[
				# If the index is a multiple of, add a newline
				f"{val}\n" if (index + 1) % 4 == 0 else f"{val}, "
				for index, val in enumerate(mout)  # For every element in arr
			],
		)

	seed = db['members'][user]['seeds']
	if seed == {}:
		sout = None
	else:
		for m in db['members'][user]['seeds']:
			amount = str(db['members'][user]['seeds'][m]['amount'])
			sout.append(f"{seeds[m]['name']}: {amount}")

		sout = "".join(  # Join an array together
			[
				# If the index is a multiple of, add a newline
				f"{val}\n" if (index + 1) % 5 == 0 else f"{val}, "
				for index, val in enumerate(sout)  # For every element in arr
			],
		)

	e.add_field(name = '- :sheep: Animals: ', value = aout, inline = False)

	e.add_field(name = '- :hammer: Tools: ', value = tout, inline = False)

	e.add_field(name = '- :seedling: Seeds: ', value = sout, inline = False)

	e.add_field(name = '- :moneybag: Merchandise: ', value = mout, inline = False)

	await message.channel.send(embed = e)

