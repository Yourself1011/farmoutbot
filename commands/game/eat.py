from replit import db
import random
from zstats import animals, tools, merch, seeds, eatable, softSearch, gatheringCmd
from random import uniform, randint
from math import floor


async def eat(message, client):
    args = message.content.split(" ")
    if len(args) == 2:
        await message.channel.send("what u gonna eat lol")
        return
    if str(message.author.id) not in db["members"]:
        await message.channel.send("cant eat if you dont exist")
        return
    eated = softSearch(eatable, args[2])
    if not bool(eated):
        await message.channel.send("cant eat that")
        return
    if eated not in db["members"][str(message.author.id)]["merch"]:
        await message.channel.send("you dont have that")
        return
    if eated == "ginseng":
        thing = random.choice([animals, tools, merch, seeds])
        values = thing.values()
        things = list(values)
        thingr = random.choice(things)
        name = thingr["name"].split(" ")[0]
        if not str(thing[name]["cost"]).isnumeric():
            while not str(thing[name]["cost"].isnumeric()):
                thing = random.choice([animals, tools, merch, seeds])
                if str(thing[name]["cost"].isnumeric()):
                    break
        if thing == animals:
            amount = random.randint(1, 3)
        if thing == tools:
            amount = 1
        if thing == merch:
            amount = random.randint(5, 10)
        if thing == seeds:
            amount = random.randint(10, 20)
        await message.channel.send(
            f"you ate your ginseng, and the ginseng gods gifted you `{amount} {name}(s)`."
        )
        a = db["members"][str(message.author.id)]
        if name not in a[thing["name"]]:
            if thing == animals:
                a["animals"][name] = {"amount": amount, "lastused": 0}
            if thing == tools:
                a["tools"][name] = {"durability": tools[name]["durability"]}
            if thing == merch:
                a["merch"][name] = amount
            if thing == seeds:
                a["seeds"][name] = {"amount": amount}
        else:
            if thing in [animals, seeds]:
                a[thing["name"]][name]["amount"] += amount
            if thing == tools:
                a["tools"][name]["durability"] = tools[name]["durability"]
            if thing == merch:

                a["merch"][name] += amount
        a = db["members"]

    if eated == "mushroom":
        await message.channel.send(
            "you ate your mushroom, got poisoned, and died. you paid 100 coins to be reborn"
        )

    if eated == "applepie":
        coins = random.randint(1, 3)
        thing = random.randint(1, 3)
        if thing == 1:
            await message.channel.send(
                "you ate your apple pie, and it tasted really good."
            )
        if thing == 2:
            await message.channel.send(
                "you were eating your apple pie when a bird swooped in from nowhere and stole it away."
            )
        if thing == 3:
            await message.channel.send(
                f"you ate your apple pie, and it tasted so good that `{coins} coins` appeared out of nowhere."
            )
            a = db["members"]
            a[str(message.author.id)]["money"] += coins
            db["members"] = a

    if eated == "mango":
        await message.channel.send(
            "you ate your mango, and you just wasted a mango because it didn't do anything."
        )

    if eated == "cake":
        await message.channel.send("you ate your cake, and you got another cake.")
        a = db["members"]
        a[str(message.author.id)]["merch"]["cake"] += 1
        db["members"] = a

    if "loottable" in merch[eated]:

        itemOut = ""
        allItems = {}
        money = 0

        user = db["members"][str(message.author.id)]
        if eated not in user["merch"]:
            return await message.channel.send("You don't have that")

        if len(args) == 4 and args[3].lower() in ["all", "a", "max"]:
            repeat = user["merch"][eated]

        elif len(args) == 4 and args[3].isnumeric() and user["merch"][eated] < int(args[3]) or int(args[3]) <= 0:
            await message.channel.send(
                "https://media.tenor.co/videos/e0b51ead5f9fd990f06a5582cdc996bf/mp4"
            )
            return
        repeat = int(args[3]) if len(args) == 4 and args[3].isnumeric() else 1

        if user["merch"][eated] < repeat:
            return await message.channel.send("You don't have that many")

        a = db["members"]
        user = a[str(message.author.id)]

        items = gatheringCmd(
            message,
            merch[eated]["loottable"],
            [
                merch[eated]["amount"][0] * repeat,
                merch[eated]["amount"][1] * repeat,
                merch[eated]["amount"][2],
            ],
        )

        money += floor(
            merch[eated]["money"][1]
            + (merch[eated]["money"][0] - merch[eated]["money"][1])
            * (uniform(0, 1) ** merch[eated]["money"][2])
        )

        for j in items:
            if j[0] in allItems:
                allItems[j[0]] += j[1]
            else:
                allItems[j[0]] = j[1]

        for i in items:
            for j in [merch, tools, animals, seeds]:
                if i[0] in j:
                    itemType = j["name"]

            if i[0] in user[itemType] and itemType != "tools" and itemType != "merch":
                user[itemType][i[0]]["amount"] += i[1]

            elif i[0] in user[itemType] and itemType == "merch":
                user["merch"][i[0]] += i[1]

            elif i[0] in user[itemType] and itemType == "tools":
                user["tools"][i[0]]["durability"] = tools[i[0]]["durability"]

            elif itemType == "merch":
                user["merch"][i[0]] = i[1]

            elif itemType == "animals":
                user["merch"][i[0]] = {"lastused": 0, "amount": i[1]}

            elif itemType == "tools":
                user["merch"][i[0]] = tools[i[0]]["durability"]

            elif itemType == "seeds":
                user["seeds"][i[0]] = {"amount": i[1]}

            user["money"] += money

        user["merch"][eated] -= repeat
        if user["merch"][eated] <= 0:
            del user["merch"][eated]

        db["members"] = a

        verb1 = ["ate", "opened", "used"]
        verb2 = [
            "out came",
            "received",
            "got",
            "farted out",
            "burped out",
            "found",
            "out of thick ear appeared",
            "a ufo came and dropped off",
        ]

        itemOut = ", ".join([f"{j} {i}(s)" for i, j in allItems.items()])

        await message.channel.send(
            f"You {verb1[randint(0, len(verb1) - 1)]} {repeat} {eated}(s) and {verb2[randint(0, len(verb2) - 1)]} {itemOut}, and {money} coins"
        )

    if eated == "pridewatermelon":
        await message.channel.send(
            "you ate a pridewatermelon, and you feel really proud"
        )

    else:
        a = db["members"]
        if eated in a[str(message.author.id)]["merch"]:
            a[str(message.author.id)]["merch"][eated] -= 1
            if a[str(message.author.id)]["merch"][eated] == 0:
                del a[str(message.author.id)]["merch"][eated]
        db["members"] = a
