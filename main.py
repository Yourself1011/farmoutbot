# Jeff's not here. I can do whatever I want. heheheheheheh also i wonder when he will see this i saw it already stupid no you didn't you didn't see anything whoosh you never saw this yes i did mf nope yap nap sapnap

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
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

from acommands import commands
from zstats import tips
from zstats import animals
from zuseanimal import useanimal
from keep_alive import keep_alive
import traceback
from trade_update import startLoop, trade_update
from thinghappen import thinghappen
from drawlottery import drawlottery
from time import time
from vote import vote	

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
	DiscordComponents(client)
	kljkalsdhfasjdkf = ['stupid', 'dumb', 'fat', 'annoying', 'crybaby', 'weirdo', 'nerd', 'moron', 'stinky', 'idiot', 'diaperbutt']
	slkfjhasldkjfkan = random.choice(kljkalsdhfasjdkf)
	await client.change_presence(status=discord.Status.idle, activity=discord.Game(name = slkfjhasldkjfkan))

	things = ["bong bong bong this is my song the bot is on", "babbon babbon bot babbon burp", "unga unga bunga boo, the bot is on, now time for poo"]

	print(things[random.randint(0, len(things) - 1)])

	await startLoop(client)

@client.event
async def on_guild_join(guild):
	a = db['server']
	a[str(guild.id)] = {
		'prefix': 'i',
		'channel': None
	}
	db['server'] = a
	print(f'woah woah woah new serverrrrr: {guild.name}')

@client.event
async def on_message(message):
	if message.author.id == 835153690155024454:
		args = message.content.replace("|", "").split(" ")
		user = await client.fetch_user(args[2])
		print(f"{user.name} has voted for {args[0]} on {args[1]}")
		await vote(args[2], args[1], client)
	if message.author.bot:
		return
	if client.user == message.author:
		return

	if str(message.guild.id) not in db["server"]:
		a = db['server']
		a[str(message.guild.id)] = {
			'prefix': 'i',
			'channel': None
		}
		db['server'] = a
		print(f'woah woah woah new serverrrrr: {message.guild.name}')
		
	mention = f'<@!{client.user.id}>'
	if message.content == mention or f'<@{client.user.id}>' == message.content:
		prefix = db['server'][str(message.guild.id)]['prefix']
		await message.reply('hi my prefix for this server is `'+prefix+'`. use `'+prefix+' help` to see all commands.')
		return

	prefix = db['server'][str(message.guild.id)]['prefix']
	args = message.content.split(' ')
	if not message.content.lower().startswith(f"{prefix} ") and str(args[0]) != (mention):
		return

	msg = message.content
	msg = msg.split(' ')
	msg = msg[1]

	if msg.lower() in animals and msg.lower() != 'name':
		thing = animals[msg.lower()]['thing']
		await useanimal(message, msg.lower(), client, thing)
		return

	command = None
	for i in commands:
		if msg.lower() == commands[i]['name']:
			command = commands[i]
			break
		for j in commands[i]['aliases']:
			if msg.lower() == j:
				command = commands[i]
				break

	if command == None:
		return
	if command:

		try:
			if str(message.author.id) in db["members"]:
				user = db["members"][str(message.author.id)]
				sites = []
				links = []
				a = db["members"]

				if "discordbotlist.com" in user["cooldowns"] and user["cooldowns"]["discordbotlist.com"]/10 <= time() and not bool(int(str(user["cooldowns"]["discordbotlist.com"])[-1])):
					sites.append("discordbotlist.com")
					links.append("https://discordbotlist.com/bots/farmout/upvote")
					a[str(message.author.id)]["cooldowns"]["discordbotlist.com"] += 1

				db["members"] = a

				if bool(sites) and bool(links) and user["settings"]["votedm"]:
					embed = discord.Embed(
						title = "You can vote again at",
						description = "\n".join([f"[{site}]({link})" for site, link in zip(sites, links)])
					)
					await message.author.send(embed = embed)
			outRaw = await commands[command['name']]['execute'](message, client)
			name = commands[command['name']]['name']
			print(f'{message.author.name} did {name} command in {message.guild.name}')
			if str(message.author.id) in db['members']:
				a = db['members']
				a[str(message.author.id)]['commandsused'] += 1
				db['members'] = a

			reply = outRaw[1] if (type(outRaw) == list or type(outRaw) == tuple) and len(outRaw) == 2 else False

			out = outRaw[0] if type(outRaw) == list or type(outRaw) == tuple else ""

			embed = outRaw if type(outRaw) == discord.Embed else None
			
			tipchance = random.randint(1, 50)
			if tipchance == 1 and db["members"][str(message.author.id)]["settings"]["tips"]:
				tip = random.choice(tips)
				out += f"\n\ntip: {tip}"
				return
			thingchance = random.randint(1, 250)
			if thingchance == 1 and str(message.author.id) in db['members']:
				thing = thinghappen(message, client)
				thingg = await thing.__anext__()

				out += f"\n\n{thingg}" if type(thingg) == str else ""

			if type(out) == str and not reply and (out != "" or bool(embed)):
				await message.channel.send(out, embed = embed)

			elif type(out) == str and reply and (out != "" or bool(embed)):
				await message.reply(out, mention_author = db["members"][str(message.author.id)]["settings"]["replypings"], embed = embed)

			if thingchance == 1 and str(message.author.id) in db['members']:
				await thing.__anext__()

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

"""
Super important, do not	remove  			 
	
     		  	 	
	
     			 		 
	
     		  	 	
	
      			  	 
	
      	     
	
     		  			
	
     		 				
	
     		 			 
	
     		 			 
	
     		    	
	
      	     
	
     		  			
	
     		 	  	
	
     			 		 
	
     		  	 	
	
      	     
	
     				  	
	
     		 				
	
     			 	 	
	
      	     
	
     			 	 	
	
     			    
	
  """