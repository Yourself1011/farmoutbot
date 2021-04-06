from replit import db
import discord
import time
from zstats import seeds, merch

async def crops(message, client):
	if str(message.author.id) not in db['members']:
		await message.channel.send('make an account first strumfum')
		return
	if db['members'][str(message.author.id)]['plantcooldowns'] == {} or 'plantcooldowns' not in db['members'][str(message.author.id)]:
		await message.channel.send('no plants here')
		return
	name = message.author.name
	e = discord.Embed(
		title = f'',
		colour = discord.Colour.green()
	)
	for i in db['members'][str(message.author.id)]['plantcooldowns']:
		name = merch[i]['name']
		amount = db['members'][str(message.author.id)]['plantcooldowns'][i]['amount']
		now = int(round(time.time()*1000))
		seed =  seeds[db['members'][str(message.author.id)]['plantcooldowns'][i]['name']]
		growTime = seed["stages"][db['members'][str(message.author.id)]['plantcooldowns'][i]["stage"]] if "stages" in seed else seed['growtime']

		if db['members'][str(message.author.id)]['plantcooldowns'][i]['cooldown'] + growTime > now:

			now2 = int(round(time.time() * 1000))
			f = db['members'][str(message.author.id)]['plantcooldowns'][i]['cooldown'] - now2
			f = str(f)
			
			newvar = growTime+db['members'][str(message.author.id)]['plantcooldowns'][i]['cooldown']
			cooldown = round((newvar-now2)/1000)
			r = f'Wait `{cooldown}` seconds.'
		else:
			r = '**Ready!**'
		e.add_field(name = f'- {name}: ',value = f'Amount: **{amount}** | Status: {r}', inline = False)
	prefix = db['server'][str(message.guild.id)]['prefix']
	e.set_author(name=f'{message.author.name}\'s farm', icon_url=message.author.avatar_url)
	e.set_footer(text = f'Use <{prefix} collect (plant)> to collect your plants when they are ready.')
	await message.channel.send(embed = e)