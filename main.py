# Jeff's not here. I can do whatever I want. heheheheheheh also i wonder when he will see this i saw it already stupid no you didn't you didn't see anything whoosh you never saw this yes i did mf nope yap

import os
from os.path import join, dirname
from importlib import import_module

import discord
from dotenv import load_dotenv
from replit import db
import sys
import random
import pprint
import asyncio

from acommands import commands
from zuseanimal import useanimal
from zstats import tips
from zstats import animals
from keep_alive import keep_alive
import traceback
from trade_update import startLoop, trade_update
from thinghappen import thinghappen
from drawlottery import drawlottery

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path) 
BOT_TOKEN = os.environ.get('BOT_TOKEN')

client = discord.Client(intents = discord.Intents.all())

for file in os.scandir('./commands/'):
	filename = file.name[:-3]
	if file.name.endswith('.py') and filename not in ['main', 'acommands', 'zstats', 'zuseanimal', 'keep_alive', 'trade_update']:
		commands[filename]['execute'] = getattr(import_module(f"commands.{filename}"), filename)

@client.event
async def on_ready():
	kljkalsdhfasjdkf = ['stupid', 'dumb', 'fat', 'annoying', 'crybaby', 'weirdo', 'nerd', 'moron', 'stinky', 'idiot', 'diaperbutt']
	slkfjhasldkjfkan = random.choice(kljkalsdhfasjdkf)
	await client.change_presence(status=discord.Status.idle, activity=discord.Game(name = slkfjhasldkjfkan))

	print('babbon babbon bot babbon burp')

	await startLoop(client)

@client.event
async def on_guild_join(guild):
	a = db['server']
	a[str(guild.id)] = {
		'prefix': 'eye',
		'channel': None
	}
	db['server'] = a
	print(f'woah woah woah new serverrrrr: {guild.name}')

@client.event
async def on_message(message):
	if message.author.bot:
		return
	if client.user == message.author:
		return
		
	mention = f'<@!{client.user.id}>'
	if mention in message.content:
		prefix = db['server'][str(message.guild.id)]['prefix']
		await message.reply('hi my prefix for this server is `'+prefix+'`. use `'+prefix+' help` to see all commands.')
		return

	prefix = db['server'][str(message.guild.id)]['prefix']
	if not message.content.lower().startswith(f"{prefix} "):
		return

	msg = message.content
	msg = msg.split(' ')
	msg.pop(0)
	msg = ' '.join(msg)

	if msg.lower() in animals and msg.lower() != 'name':
		thing = animals[msg.lower()]['thing']
		await useanimal(message, msg.lower(), client, thing)
		return

	command = None
	for i in commands:
		if msg.lower().startswith(commands[i]['name']):
			command = commands[i]
			break
		for j in commands[i]['aliases']:
			if msg.lower().startswith(j):
				command = commands[i]
				break

	if command == None:
		return
	if command:
		try:
			await commands[command['name']]['execute'](message, client)
			name = commands[command['name']]['name']
			print(f'{message.author.name} did {name} command in {message.guild.name}')
			if str(message.author.id) in db['members']:
				a = db['members']
				a[str(message.author.id)]['commandsused'] += 1
				db['members'] = a
			
			tipchance = random.randint(1,50)
			if tipchance == 1:
				tip = random.choice(tips)
				await message.channel.send(tip)
				return
			thingchance = random.randint(1,80)
			if thingchance == 1 and str(message.author.id) in db['members']:
				await thinghappen(message, client)

		except:
			traceback.print_exc()
			permsNeeded = ["read_messages", "send_messages", "embed_links"]
			if "perms" in command:
				permsNeeded.extend(command["perms"])

			permsNotGiven = [i.replace("_", " ") for i in permsNeeded if not dict(iter(message.guild.get_member(client.user.id).permissions_in(message.channel)))[i]]
			try:
				await message.channel.send(f'```{sys.exc_info()}```')
			except:
				if bool(permsNotGiven):
					await message.author.send(f'I\'m missing some permissions! I need to be able to {", ".join(permsNotGiven)}\n ```{sys.exc_info()}```')
	
keep_alive()
try:
	client.run(BOT_TOKEN)	
except discord.errors.HTTPException as err:
	print(err)	