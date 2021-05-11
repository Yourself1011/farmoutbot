from random import randint
from replit import db
from zstats import tools, updateDict, getMember
from datetime import date
import collections.abc
from json import loads
from os import environ

async def devmode(message, client):
	args = message.content.lower().split(" ")
	if message.author.id not in [690577156006477875, 690575294674894879,697094970842021969, 764900173431832576, 697089328668737566] and not environ.get("ENV") == "dev": 
		responses = ["Thank you for using Farmout. All of our agents are currently unavailable. Our next available agent will be with you shortly. *elevator music plays*", "uhm no", "Be a dev smh", "Wait five more minutes. If I still don't work, read this message again.", "Shh... I'm sleeping. Don't disturb me", "bruh", "Maybe I shouldn't be focusing on adding more of these responses and start finishing the bot", "Nearly 40% of small breed dogs live longer than 10 years, but only 13% of giant breed dogs live that long. The average 50-pound dog will live 10 to 12 years. But giant breeds such as great Danes or deerhounds are elderly at 6 to 8 years.", "Bones, stop growing after puberty and muscle and fat cells also stop dividing. But cartilage - that's the plastic-like stuff in ears and noses - cartilage continues to grow until the day you die. Not only does cartilage grow, but the earlobes elongate from gravity. And that makes ears look even larger.", "you missed your chance to be a beta tester 2bad4u", 'You\'re fat. Did you know that?', 'You\'re dumb. Like a babbon bum?', 'why are we spending so much time on this we\'ll just remove it eventually anyway', "Cow's teeth are different from ours. On the top front, cows have a tough pad of skin instead of teeth. They have 8 incisors on the bottom front and 6 strong molars on the top and bottom of each side to grind their food. Cows have a total of 32 teeth.", "Is this thing on?", '*jeopardy music plays*', 'Sheep are quadrupedal, ruminant mammals typically kept as livestock. Like all ruminants, sheep are members of the order Artiodactyla, the even-toed ungulates. Although the name sheep applies to many species in the genus Ovis, in everyday usage it almost always refers to Ovis aries.'] 
		await message.channel.send(responses[randint(0, len(responses) - 1)])
		return

	if len(args) == 2:
		await message.channel.send("Do a subcommand. Toggle or update")
		return

	if args[2] == "toggle":
		members = db["members"]

		if f"{str(message.author.id)} real" in members:
			members[str(message.author.id)] = members[f"{str(message.author.id)} real"]

			del members[f"{str(message.author.id)} real"]

			await message.channel.send("Devmode is now OFF")

		else:
			members[f"{str(message.author.id)} real"] = members[str(message.author.id)]


			today = date.today()
			datemade = today.strftime("%B %d, %Y")
			
			members[str(message.author.id)] = {
				'animals': {},
				'tools': {
					'wateringcan': tools['wateringcan']['durability']
				},
				'merch': {},
				'seeds': {
					'grassseeds': {
						'amount': 5
					}
				},
				'plantcooldowns': {},
				'plants': {},
				'dailytimer': 0,
				'hourlytimer': 0,
				'money': 100,
				'reputation': 500,
				'amounts': {
					'shared': 0,
					'gambled': 0,
					'bought': 0,
					'sold': 0,
					'used': 0,
				},
				'prestige': 0,
				'multi': 1.0,
				'commandsused': 0,
				'datemade': datemade,
				'donecontracts': [{
					'1': [],
					'2': [],
					'3': [],
					'4': []
				}],
				'currentcontract': [],
				"trades": {
					"lastTradeId": 0,
					"tradeAmts": [0, 0, 0],
					"stock": [0, 0, 0]
				},
				"cooldowns": {},
				"location": "default",
				"locations": {} }
			await message.channel.send("Devmode is now ON")
		db["members"] = members

	elif args[2] == "off":
		members = db["members"]

		if f"{str(message.author.id)} real" in members:
			members[str(message.author.id)] = members[f"{str(message.author.id)} real"]

			del members[f"{str(message.author.id)} real"]

			await message.channel.send("Devmode is now OFF")

		else:
			await message.channel.send("Devmode is already OFF idiot")

		db["members"] = members

	elif args[2] == "on":
		members = db["members"]

		if f"{str(message.author.id)} real" in members:
			await message.channel.send("Devmode is already ON idiot")

		else:
			members[f"{str(message.author.id)} real"] = members[str(message.author.id)]


			today = date.today()
			datemade = today.strftime("%B %d, %Y")
			
			members[str(message.author.id)] = {
				'animals': {},
				'tools': {
					'wateringcan': tools['wateringcan']['durability']
				},
				'merch': {},
				'seeds': {
					'grassseeds': {
						'amount': 5
					}
				},
				'plantcooldowns': {},
				'plants': {},
				'dailytimer': 0,
				'hourlytimer': 0,
				'money': 100,
				'reputation': 500,
				'amounts': {
					'shared': 0,
					'gambled': 0,
					'bought': 0,
					'sold': 0,
					'used': 0,
				},
				'prestige': 0,
				'multi': 1.0,
				'commandsused': 0,
				'datemade': datemade,
				"trades": {
					"lastTradeId": 0,
					"tradeAmts": [0, 0, 0],
					"stock": [0, 0, 0]
				},
				"cooldowns": {},
				"location": "default",
				"locations": {}
			} 
			await message.channel.send("Devmode is now ON")
		db["members"] = members

	elif args[2] == "check":
		if f"{str(message.author.id)} real" in db["members"]:
			await message.channel.send("Devmode is ON")

		else:
			await message.channel.send("Devmode is OFF")

	elif args[2] == "update":
		if f"{str(message.author.id)} real" not in db["members"]:
			await message.channel.send("Be in dev mode smh")
			return
		members = db["members"]

		members[str(message.author.id)] = updateDict(db["members"][str(message.author.id)], loads("".join(args[3:len(args)]).replace("'", "\"")))

		db["members"] = members
		await message.channel.send(":white_check_mark: yessir")

	elif args[2] == "other":
		if message.author.id not in [690577156006477875, 690575294674894879]:
			return await message.channel.send(responses[randint(0, len(responses) - 1)])

		user = getMember(args[3], message.guild.id, client)

		if not user:
			return await message.channel.send("nobody found")

		members = db["members"]

		members[str(user.id)] = updateDict(db["members"][str(user.id)], loads("".join(args[4:len(args)]).replace("'", "\"")))

		db["members"] = members
		await message.channel.send(":white_check_mark: yessir")

	else:
		await message.channel.send("That's not a subcommand, \"dev\"")