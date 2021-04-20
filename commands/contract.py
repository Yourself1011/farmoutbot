from replit import db
from contracts import contracts
import discord

async def contract(message, client):
	prefix = db['server'][str(message.guild.id)]['prefix']
	args = message.content.split(' ')
	if len(args) == 2:
		await message.channel.send('do a subcommand: `show`, `sign`, `complete`, or `current`')
		return
	if str(message.author.id) not in db['members']:
		await message.channel.send('make a farm first')
		return
	if args[2].lower() not in ['show', 'sign', 'complete', 'current']:
		await message.channel.send('uhh wrong')
		return
	command = args[2].lower()
	currentpart = False

	for i in db['members'][str(message.author.id)]['donecontracts'][0]:
		if len(i) < 3:
			currentpart = i
			break
	if not currentpart: await message.channel.send('you\'ve already done all the contracts lol'); return
	currentpart = str(currentpart)

	if command == 'show':
		e = discord.Embed(
			title = '',
			colour = discord.Colour.red()
		)
		e.set_author(name='Contracts: ', icon_url=message.author.avatar_url)
		for i in contracts[currentpart]:
			desc = contracts[currentpart][i]['description']
			need = contracts[currentpart][i]['need'][0]
			reward = contracts[currentpart][i]['reward'][0]
			title = contracts[currentpart][i]['title']
			if i in db['members'][str(message.author.id)]['donecontracts'][0][str(currentpart)]:
				e.add_field(name = f'- ~~{title}~~ COMPLETED', value = f'~~**Description:** {desc}~~\n\n~~**Need:** {need}~~\n~~**Reward:** {reward}~~')
			else:
				e.add_field(name = f'- {title}', value = f'**Description:** {desc}\n\n**Need:** {need}\n**Reward:** {reward}')
		prefix = db['server'][str(message.guild.id)]['prefix']
		e.set_footer(text = f'Part {currentpart} of 4')
		await message.channel.send(embed = e)
		return
	
	if command == 'sign':
		currentpart = str(currentpart)
		if len(args) == 3: await message.channel.send('which one are you signing lol'); return
		if not args[3].isnumeric(): await message.channel.send('gotta say a number corresponding to the contract id'); return
		signed = int(args[3])
		if signed not in [1, 2, 3]: await message.channel.send('what'); return
		if signed in db['members'][str(message.author.id)]['donecontracts'][0][currentpart]: await message.channel.send('oy you\'ve already done that contract'); return
		if not db['members'][str(message.author.id)]['currentcontract'] == [] and signed == db['members'][str(message.author.id)]['currentcontract'][1] and currentpart == db['members'][str(message.author.id)]['currentcontract'][0]: await message.channel.send('you\'re doing that contract right now idot'); return
		a = db['members']
		a[str(message.author.id)]['currentcontract'] = [currentpart, signed]
		db['members'] = a
		await message.reply(f'You signed contract {signed} of part {currentpart}. Do `{prefix} contract current` to see your currently signed contract.')
		return

	if command == 'current':
		if db['members'][str(message.author.id)]['currentcontract'] == []:
			await message.channel.send('you havent signed a contract yet')
			return
		e = discord.Embed(
			title = '',
			colour = discord.Colour.orange()
		)
		i = db['members'][str(message.author.id)]['currentcontract'][1]
		e.set_author(name='Current contract: ', icon_url=message.author.avatar_url)
		i = str(i)	
		desc = contracts[currentpart][i]['description']
		need = contracts[currentpart][i]['need'][0]
		reward = contracts[currentpart][i]['reward'][0]
		title = contracts[currentpart][i]['title']
		e.add_field(name = f'- {title}', value = f'**Description:** {desc}\n\n**Need:** {need}\n**Reward:** {reward}')
		e.set_footer(text = f'Do <{prefix} contract complete> to complete the contract once you have all the required items.')
		await message.reply(embed = e)

	if command == 'complete':
		if db['members'][str(message.author.id)]['currentcontract'] == []:
			await message.channel.send('you havent signed a contract yet bruh')
			return
		completed = str(db['members'][str(message.author.id)]['currentcontract'][1])
		currentpart = db['members'][str(message.author.id)]['currentcontract'][0]
		print(completed, currentpart)
		if contracts[currentpart][completed]['need'][2] not in db['members'][str(message.author.id)]['merch'] or contracts[currentpart][completed]['need'][1] > db['members'][str(message.author.id)]['merch'][contracts[currentpart][completed]['need'][2]]:
			await message.channel.send('you dont have what you need to complete the contract'); return
		a = db['members']
		a[str(message.author.id)]['currentcontract'] = []
		try:
			a[str(message.author.id)]['donecontracts'][0][int(currentpart)].append(completed)
		except:
			a[str(message.author.id)]['donecontracts'][0][int(currentpart)] = [completed]
		if contracts[currentpart][completed]['reward'][2] not in db['members'][str(message.author.id)]['merch']:
			a[str(message.author.id)]['merch'][contracts[currentpart][completed]['reward'][2]] = contracts[currentpart][completed]['reward'][1]
		else:
			a[str(message.author.id)]['merch'][contracts[currentpart][completed]['reward'][2]] += contracts[currentpart][completed]['reward'][1]
		if len(contracts[currentpart][completed]['reward']) == 4:
			a[str(message.author.id)]['money'] += contracts[currentpart][completed]['reward'][3]
		a[str(message.author.id)]['merch'][contracts[currentpart][completed]['need'][2]] -= contracts[currentpart][completed]['need'][1]
		if a[str(message.author.id)]['merch'][contracts[currentpart][completed]['need'][2]] == 0:
			del a[str(message.author.id)]['merch'][contracts[currentpart][completed]['need'][2]]
		db['members'] = a
		if currentpart == 4 and completed == 3:
			await message.channel.send('woah you did all the contracts already? i better add more soon lol')
			return
		else:
			await message.reply(f'yay you completed contract #{completed} of part {currentpart}.')