import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


async def vote(message, client):
	await message.channel.send(
		'vote for farmout by clicking the "vote" button\nfrom voting, you can support our bot and get 2 epicboxes which you can eat\nyou can vote every 12 hours',
		components=[
		Button(style=ButtonStyle.URL, label="Vote", url="https://discordbotlist.com/bots/farmout/upvote"),],
	)