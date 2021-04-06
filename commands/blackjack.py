from replit import db
from random import randint
import discord
from asyncio import TimeoutError
from time import time
from math import floor
from zstats import convertInt

cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
amounts = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
suits = ["♠️", "♥️", "♣️", "️♦️"]

def cardFormat(x):
	return f"`{x[0]} {x[1]}`"

def getCard():
	return [cards[randint(0, 12)], suits[randint(0, 3)]]

def getTotal(cardes):
	numbers = [i[0] for i in cardes]
	total = 0
	aUsed = 0
	for i in numbers:
		total += amounts[cards.index(i)]
	while total > 21 and len([i for i in numbers if i == "A"]) > aUsed:
		total -= 10
		aUsed += 1
	return total

async def blackjack(message, client):
	if str(message.author.id) not in db['members']:
		await message.channel.send('make an account to blackjack')
		return
	dbuser = db["members"][str(message.author.id)]

	if "bjcd" in dbuser:
		if dbuser["bjcd"] < time():

			cdFormatted = floor(time() - dbuser["bjcd"]) + "s"
			

			await message.channel.send(f"Woah there, chill. Wait {cdFormatted} before gambling again")
			return

	if len(message.content.split(" ")) < 3:
		await message.channel.send("bet smth smh")
		return

	amt = message.content.split(" ")[2]
	if amt in ["a", "all", "max"]:
		amt = dbuser["money"]
	else:
		amt = convertInt(amt)

		if not bool(amt):
			await message.channel.send("bet a number")
			return


	if dbuser["money"] < amt:
		await message.channel.send("Sorry, you can't go into debt here at farmout")
		return
	elif amt < 50:
		await message.channel.send("Bet an amount over 50.")
		return

	m = db["members"]
	db["members"][str(message.author.id)]["bjcd"] = time() + 10
	db["members"] = m

	bot = [getCard()]
	user = [[getCard(), getCard()]]

	botTotal = getTotal(bot)
	userTotal = [getTotal(user[0])]

	userSplit = 0

	insurance = 0
	
	end = True
	while end:
		if userSplit > len(user) - 1:
			end = False
			userSplit -= 1
			break
		if userTotal[userSplit] >= 21:
			if userSplit < len(user) - 1:
				userSplit += 1
			else:
				break
		options = ["H", "S"]

		if user[userSplit][0][0] == user[userSplit][1][0] and len(user[userSplit]) == 2:
			options.append("SP")
		if botTotal == 11 and amt * 1.5 <= dbuser["money"] and insurance == 0 and len(user[0]) == 2:
			options.append("I")
		if amt * 2 <= dbuser["money"]:
			options.append("D")

		e = discord.Embed(
			title = f"{message.author.name}'s blackjack game",
			description = f"**Bot, total: {botTotal}**\n{', '.join(list(map(cardFormat, bot)))}, `?`",
			colour = 15721648,
		)

		footer = f"Type {'SP to split, ' if 'SP' in options else ''}{'I for insurance, ' if 'I' in options else ''}{'D to double down, ' if 'D' in options else ''}H to hit, or S to stand"

		e.set_footer(text = footer)

		for i in range(len(user)):
			e.add_field(name = f"{'» ' if i == userSplit else ''}Hand {i + 1}, total: {userTotal[i]}",
			value = ", ".join(list(map(cardFormat, user[i]))), inline=False)
		
		await message.channel.send(embed = e)

		try:
			msg = await client.wait_for("message", check=lambda x: x.author.id == message.author.id and x.content.lower() in [i.lower() for i in options], timeout=60.0)
		except TimeoutError:
			await message.channel.send("SMH my head 60 seconds is more than enough time to make up your mind")
			return
		else:
			if msg.content.lower() == "h":
				user[userSplit].append(getCard())

				userTotal[userSplit] = getTotal(user[userSplit])

			elif msg.content.lower() == "s":
				userSplit += 1

			elif msg.content.lower() == "d":
				user[userSplit].append(getCard())

				userTotal[userSplit] = getTotal(user[userSplit])

				amt *= 2

				userSplit += 1

			elif msg.content.lower() == "i":
				insurance = amt*0.5

			elif msg.content.lower() == "sp":
				userCopy = user[userSplit]
				user[userSplit] = [userCopy[0], getCard()]
				user.append([userCopy[1], getCard()])

				userTotal[userSplit] = getTotal(user[userSplit])
				userTotal.append(getTotal(user[userSplit + 1]))
	
	while botTotal < 17:
		bot.append(getCard())
		botTotal = getTotal(bot)

	insuranced = False
	if bot[0][0] == "A" and amounts[cards.index(bot[1][0])] == 10:
		insuranced = True

	largestSplit = max([i for i in userTotal if i <= 21]) if bool([i for i in userTotal if i <= 21]) else 0

	if largestSplit > botTotal or (botTotal > 21 and bool(largestSplit)) or (bool([a for a, b in zip(userTotal, user) if len(b) == 2 and a == 21])):
		reason = "Nice you found a bug\n"
		if largestSplit > botTotal:
			reason = "You went higher than the bot!\n"
		elif botTotal > 21:
			reason = "The bot busted!\n"
		elif bool([a for a, b in zip(userTotal, user) if len(b) == 2 and a == 21]):
			reason = "You got blackjack\n"
		
		if bool(insurance):
			amt -= insurance
		e = discord.Embed(
			title = f"{message.author.name}'s blackjack game. You win!",
			description = f"{reason}{'Also your insurance did not work' if bool(insurance) else ''}\nYou won {amt}\n**Bot, total: {botTotal}**\n{', '.join(list(map(cardFormat, bot)))}",
			colour = 1950746,
		)

		e.set_footer(text = "winner winner chicken dinner")

		for i in range(len(user)):
			e.add_field(name = f"Hand {i + 1}, total {userTotal[i]}", value = ", ".join(list(map(cardFormat, user[i]))), inline=False)
		
		await message.channel.send(embed = e)
		m = db["members"]
		m[str(message.author.id)]["money"] += amt
		m[str(message.author.id)]["amounts"]["gambled"] += amt
		db["members"] = m

	elif largestSplit == botTotal and bool(largestSplit) and not (len(bot) == 2 and botTotal == 21):
		reason = "You and the bot tied\n"
		
		if bool(insurance):
			amt -= insurance
		e = discord.Embed(
			title = f"{message.author.name}'s blackjack game. You tied!",
			description = f"{reason}{'Also your insurance did not work' if bool(insurance) else ''}\nYour balance did not change\n**Bot, total: {botTotal}**\n{', '.join(list(map(cardFormat, bot)))}",
			colour = 16442624,
		)

		e.set_footer(text = "👔")

		for i in range(len(user)):
			e.add_field(name = f"Hand {i + 1}, total {userTotal[i]}", value = ", ".join(list(map(cardFormat, user[i]))), inline=False)
		
		await message.channel.send(embed = e)

	else:
		insuranceMsg = ""
		if bool(insurance) and insuranced:
			insuranceMsg = " But hey, at least you bought insurance and it worked\n"
			amt -= insurance
		elif bool(insurance) and not insuranced:
			insuranceMsg = " oh also your insurance didn't work\n"
			amt += insurance
		
		reason = "Nice you found a bug\n"

		if botTotal > largestSplit:
			reason = "The bot got higher than you.\n"
		elif not bool(largestSplit) and botTotal > 21:
			reason = "You and the bot busted! House wins.\n"
		elif not bool(largestSplit):
			reason = "You busted!\n"
		elif botTotal == 21:
			reason = "The bot got blackjack\n"

		e = discord.Embed(
			title = f"{message.author.name}'s blackjack game. You lose!",
			description = f"{reason}{insuranceMsg}You lost {amt}\n**Bot, total: {botTotal}**\n{', '.join(list(map(cardFormat, bot)))}",
			colour = 12851738,
		)

		e.set_footer(text = 'too bad so sad')

		for i in range(len(user)):
			e.add_field(name = f"Hand {i + 1}, total {userTotal[i]}", value = ", ".join(list(map(cardFormat, user[i]))), inline=False)
		
		await message.channel.send(embed = e) #is it working now no
		m = db["members"]
		m[str(message.author.id)]["money"] -= amt
		m[str(message.author.id)]["amounts"]["gambled"] -= amt
		db["members"] = m