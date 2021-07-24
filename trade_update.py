import discord
from replit import db
import random
from zstats import animals, tools, merch, builtintrades
import math  # just use mental math kekw
from time import time
import asyncio
from threading import Timer
from drawlottery import drawlottery
from requests import post, exceptions


async def startLoop(client):
    while True:
        if math.floor(((db["lastTradeDate"] + 1) * 21600) - time()) <= 0:
            db["lastTradeDate"] = math.floor(time() / 21600)
            await trade_update(client)

        print(
            f"{math.floor(((db['lastTradeDate'] + 1)  * 21600) - time())}s to trade update"
        )

        await asyncio.sleep(math.ceil(((db["lastTradeDate"] + 1) * 21600) - time()))


diff = [3, 10, 20, 50, 100]
limits = [2, 3, 5, 7, 9]
getTv = [5, 10, 50, 100, 300]


def mapFunc(x):
    return f"`{x[1]}x` **{x[0]['name']}**"


async def trade_update(client):
	
	print("updated trades")
	for j in range(0, 5):
			if j == 0:
					tradeval = random.randint(10, 50)
			if j == 1:
					tradeval = random.randint(50, 150)
			if j == 2:
					tradeval = random.randint(200, 500)
			if j == 3:
					tradeval = random.randint(1000, 2000)
			if j == 4:
					tradeval = random.randint(5000, 8500)

			objList = [animals, merch, tools]

			sideOneVal = 0
			sideOne = []

			while True:

					obj = objList[random.randint(0, 1)]

					thingInt = random.randint(1, len(obj) - 1)
					thing = obj[list(obj)[thingInt]]
					while "give" in thing:
							if not thing["give"]:
									break
							thingInt = random.randint(1, len(obj) - 1)
							thing = obj[list(obj)[thingInt]]

					maxAmount = math.floor((tradeval - sideOneVal) / thing["tradevalue"])
					fourCheck = math.ceil(tradeval / limits[j] / thing["tradevalue"])

					if maxAmount == 0:
							continue

					if fourCheck > maxAmount:
							fourCheck = maxAmount

					amount = random.randint(fourCheck, maxAmount)

					repeat = [i for i in sideOne if i[0] in [thing]]

					if bool(repeat):
							sideOne[sideOne.index(repeat[0])][1] += amount

							sideOneVal += thing["tradevalue"] * amount

					else:

							sideOne.append([thing, amount, list(obj.keys())[thingInt]])

							sideOneVal += thing["tradevalue"] * amount

					if sideOneVal < tradeval + diff[j] and sideOneVal > tradeval - diff[j]:
							break

			sideTwoVal = 0
			sideTwo = []
			while True:

					obj = objList[random.randint(0, 2)]

					thingInt = random.randint(1, len(obj) - 1)
					thing = obj[list(obj)[thingInt]]
					while "get" in thing:
							if not thing["get"]:
									break
							thingInt = random.randint(1, len(obj) - 1)
							thing = obj[list(obj)[thingInt]]

					maxAmount = math.floor(
							(tradeval + getTv[j] - sideTwoVal) / thing["tradevalue"]
					)
					fourCheck = math.ceil(
							tradeval + getTv[j] / (limits[j] + j) / thing["tradevalue"]
					)

					if maxAmount == 0:
							continue

					if fourCheck > maxAmount:
							fourCheck = maxAmount

					amount = random.randint(fourCheck, maxAmount)

					if obj["name"] == "tools":
							amount = 1

					repeat = [i for i in sideTwo if i[0] in [thing]]

					if bool(repeat) and obj["name"] == "tools":
							continue
					if bool(repeat):
							sideTwo[sideTwo.index(repeat[0])][1] += amount

							sideTwoVal += thing["tradevalue"] * amount

					else:

							sideTwo.append([thing, amount, list(obj.keys())[thingInt]])

							sideTwoVal += thing["tradevalue"] * amount

					if (
							sideTwoVal < tradeval + getTv[j] + diff[j]
							and sideTwoVal > tradeval + getTv[j] - diff[j]
					):
							break

	trades = db["trades"]
	trades[j]["give"] = sideOne
	trades[j]["get"] = sideTwo
	db["trades"] = trades

	e = {
			"title": "Trade Offers: ",
			"description": f"Trades update every 6 hours. Next trade update <t:{(db['lastTradeDate'] + 1) * 21600}:R>",
			"color": 16711680,
			"fields": [],
	}
	db["tradeId"] += 1

	for i in range(len(db["trades"])):
			give = db["trades"][i]["give"]
			get = db["trades"][i]["get"]

			e["fields"].append(
					{
							"name": f"{i}: ",
							"value": f'Give: {", ".join(list(map(mapFunc, give)))}\nGet: {", ".join(list(map(mapFunc, get)))}',
							"inline": False,
					}
			)

	e["footer"] = {
			"text": "Use <trade (tradenumber)> to request a trade. If your reputation is too low, they may not let you."
	}

	data = {"username": "New trades!", "embeds": [e]}

	for i in db["server"]:
			if db["server"][i]["channel"] != None and "webhookUrl" in db["server"][i]:
					result = post(db["server"][i]["webhookUrl"], json=data)
					try:
							result.raise_for_status()
					except exceptions.HTTPError as err:
							print(err)

	if len(db["lottery"]) < 1:
			return
	else:
			await drawlottery(client)
