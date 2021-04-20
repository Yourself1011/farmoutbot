from replit import db
from zstats import locations, merch, animals, seeds, tools, softSearch
import discord

async def location(message, client):	
	if str(message.author.id) not in db['members']: return await message.channel.send('make an account')

	args = message.content.split(" ")

	args = [i.lower() for i in args]

	user = db["members"][str(message.author.id)]

	if len(args) == 2:
		return await message.channel.send("Please use a subcommand!\n\n`my` - shows your current locations\n`view` - look at all the locations. Include a location name to look at a specific location\n`buy` - purchase a location\n`transfer` - transfers you to a location. If you want to transfer animals to a different location, do it like this: ```\ni location transfer 5 cow, 1 camel desert\n```")

	netWorth = 0

	for k, v in user["merch"].items():
		netWorth += merch[k]["sellcost"] * v if type(merch[k]["sellcost"]) is int else 0

	for k, v in user["animals"].items():
		netWorth += animals[k]["sellcost"] * v["amount"] if type(animals[k]["sellcost"]) is int else 0

	for k in user["tools"].keys():
		netWorth += tools[k]["sellcost"] if type(tools[k]["sellcost"]) is int else 0

	for k, v in user["seeds"].items():
		netWorth += seeds[k]["sellcost"] * v["amount"] if type(seeds[k]["sellcost"]) is int else 0

	if args[2] == "my":
		embed = discord.Embed(
			title = "Your locations:",
			description = f"**» {locations[user['location']]['name']}**\n\n" + "\n".join([locations[i]["name"] for i in user["locations"].keys()])
		)
		
		return await message.channel.send(embed = embed)

	elif args[2] == "view":
		dictCopy = dict(locations)

		ints = {k: v for k, v in dictCopy.items() if type(v["cost"]) is int}

		strs = {k: v for k, v in dictCopy.items() if type(v["cost"]) is str}

		intsSorted = sorted(ints.keys(), key=lambda x: int(ints[x]["cost"]))

		strsSorted = sorted(strs.keys(), key=lambda x: str(strs[x]["cost"]))

		r = intsSorted + strsSorted


		if len(args) == 4 and args[3].isnumeric():

			page = max(min(int(args[3]), len(r)), 1) - 1

			location = locations[r[page]]

			embed = discord.Embed(
				title = location["name"],
				description = location["desc"]
			)
			embed.add_field(name = "Price", value = f"Regular: {location['cost']}\nBuy and liquidate: {max(location['cost'] - netWorth if type(location['cost']) is int else location['cost'], 0)}")

			embed.set_footer(text = f"Page {page + 1}/{len(r)}")

			return await message.channel.send(embed = embed)

		else:
			embed = discord.Embed(
				title = "locations",
				description = "\n".join([f"`{i + 1}`: {l['name']} - {l['cost']}" for i, l in enumerate(locations.values())])
			)
			return await message.channel.send(embed = embed)

	elif args[2] == "buy":
		liquidate = True if len(args) >= 5 and (args[4] == "liquidate" or args[4] == "l") else False

		if len(args) <= 3:
			return await message.channel.send("What are you buying lol")

		locationKey = softSearch(locations.keys(), args[3])

		if not locationKey: 
			return await message.channel.send("I couldn't find any location with that")

		location = locations[locationKey]

		if type(location["cost"]) is str:
			return await message.channel.send("You can't buy this location")

		if locationKey in user["locations"] or locationKey == user["location"]:
			return await message.channel.send("You already have this location smh")

		if not liquidate and user["money"] < location["cost"]:
			return await message.channel.send("You don't have enough money for that (include `liquidate` at the end of the command if you want to liquidate and buy (meaning you lose everything except for animals in other locations))")

		if liquidate and user["money"] - netWorth < location["cost"]:
			return await message.channel.send("You don't have enough money for that even if you liquidated everything")

		m = db["members"]

		user = m[str(message.author.id)]
		if not liquidate:
			user["locations"][user["location"]] = user["animals"]

		else:
			user["tools"] = {}
			user["seeds"] = {}
			user["merch"] = {}

		user["animals"] = {}

		user["money"] -= location["cost"] if not liquidate else location["cost"] - netWorth

		user["location"] = locationKey

		db["members"] = m
		return await message.channel.send(f"{location['name']} successfully purchased")

	elif args[2] == "transfer":
		locationKey = softSearch(locations.keys(), args[-1])

		if not locationKey:
			return await message.channel.send("I couldn't find that location")

		if locationKey == user["location"]:
			return await message.channel.send("You're already in that location!")

		if locationKey not in user["locations"]:
			return await message.channel.send("buy that location first")

		if len(args) == 4:

			m = db["members"]
			user = m[str(message.author.id)]

			user["locations"][user["location"]] = user["animals"]

			user["animals"] = user["locations"][locationKey]

			del user["locations"][locationKey]

			user["location"] = locationKey

			db["members"] = m

			return await message.channel.send(f"You're now in the {locationKey}")

		else:
			animalsMoved = " ".join(args[3:-1]).split(", ")

			check = [i for i in animalsMoved if len(i) == 2 and i[0].isnumeric() and softSearch(animals.keys(), i[1], ["name"])]

			if not bool(check):
				return await message.channel.send("It looks like your animals were formatted incorrectly. Please use a format like this: `i location transfer 1 cow, 5 chicken, 3 camel desert`")

			animalsFormatted = [[int(i.split(" ")[0]), softSearch(animals.keys(), i.split(" ")[1], ["name"])] for i in animalsMoved]

			m = db["members"]

			user = m[str(message.author.id)]

			for animal in animalsFormatted:
				if animal[1] not in user["animals"] or animal[0] < user["animals"][animal[1]]["amount"]:
					return await message.channel.send(f"You don't have that many {animals[animal[1]]['name']} (s)! No animals were moved.")

				user["animals"][animal[1]]["amount"] -= animal[0]

				if not bool(user["animals"][animal[1]]["amount"]):
					del user["animals"][animal[1]]

				if animal[1] in user["locations"][locationKey]:
					user["locations"][locationKey][animal[1]]["amount"] += animal[0]

				else:
					user["locations"][locationKey][animal[1]] = {
						"lastused": 0,
						"amount": animal[0]
					}
				
			db["members"] = m

			return await message.channel.send("Successfully moved animals")
	else:

		return await message.channel.send("Please use a valid subcommand!\n\n`my` - shows your current locations\n`view` - look at all the locations. Include a location name to look at a specific location\n`buy` - purchase a location\n`transfer` - transfers you to a location. If you want to transfer animals to a different location, do it like this: ```\ni location transfer 5 cow, 1 camel desert\n```")