import discord

async def vote(message, client):
	e = discord.Embed(
		title = 'vote for farmout',
		description = 'vote rn or else',
		colour = discord.Colour.gold()
	)
	e.add_field(name = 'vote link', value = 'https://discordbotlist.com/bots/farmout/upvote')
	e.set_footer(text = 'vote rn or babn')
	await message.channel.send(embed = e)