import discord

async def credits(message, client):
	e = discord.Embed(
		title = 'Farmout Credits: ',
		description = 'You can find and meet these people in our support server, at  discord.gg/tvCmtkBAkc',
		colour = discord.Colour.blue()
	)
	e.add_field(name = 'Lead Developer', value = 'Larg Ank#4701', inline = False)
	e.add_field(name = 'Debugged, helped, and tested', value = 'Yourself, Cookie\'s Owner, yogogiddap', inline = False)
	await message.channel.send(embed =e)