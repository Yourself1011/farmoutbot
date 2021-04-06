import discord

async def invite(message, client):
	e = discord.Embed(
		title = '',
		colour = discord.Colour.gold()
	)
	e.set_author(name='Links:', icon_url=message.author.avatar_url)
	e.add_field(name = 'Bot invite link: ', value = 'https://discord.com/api/oauth2/authorize?client_id=795319933314662452&permissions=67628225&scope=bot', inline = False)
	e.add_field(name = 'Admin link: ', value = 'https://discord.com/api/oauth2/authorize?client_id=795319933314662452&permissions=8&scope=bot', inline = False)
	e.add_field(name = 'Support server: ', value = 'https://discord.gg/tvCmtkBAkc', inline = False)
	e.set_footer(text = 'If the bot is not responding, its probably missing permissions.')
	await message.channel.send(embed = e)