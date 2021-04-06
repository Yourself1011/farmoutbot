import discord
from replit import db

async def contract(message, client):
	args = message.content.split(' ')
	if len(args) == 2:
		await message.channel.send('do a subcommand: `show`, `sign`, or `get`')
		return
	if str(message.author.id) not in db['members']:
		await message.channel.send('')