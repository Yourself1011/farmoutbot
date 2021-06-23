from replit import db
import random
from zstats import animals, tools, merch, seeds, eatable


async def eat(message, client):
    args = message.content.split(" ")
    if len(args) == 2:
        await message.channel.send("what u gonna eat lol")
        return
    if str(message.author.id) not in db["members"]:
        await message.channel.send("cant eat if you dont exist")
        return
    eated = args[2].lower()
    if eated not in eatable:
        await message.channel.send("cant eat that")
        return
    if eated not in db["members"][str(message.author.id)]["merch"]:
        await message.channel.send("you dont have that")
        return
    if eated == "ginseng":
        thing = random.choice([animals, tools, merch, seeds])
        thingr = random.choice(list(thing.keys))
        if not str(thing[thingr]["cost"]).isnumeric():
            while not str(thing[thingr]["cost"].isnumeric()):
                thing = random.choice([animals, tools, merch, seeds])
                if str(thing[thingr]["cost"].isnumeric()):
                    break
        if thing == animals:
            amount = random.randint(1, 3)
        if thing == tools:
            amount = 1
        if thing == merch:
            amount = random.randint(3, 6)
        if thing == seeds:
            amount = random.randint(10, 20)
        await message.channel.send(
            f"you ate your ginseng, and the ginseng gods gifted you `{amount} {thingr}(s)`."
        )
        a = db["members"][str(message.author.id)]
        if thing not in a[thing["name"]]:
            if thing == animals:
                a["animals"][thingr] = {"amount": amount, "lastused": 0}
            if thing == tools:
                a["tools"][thingr] = {"durability": tools[thingr]["durability"]}
            if thing == merch:
                a["merch"][thingr] = amount
            if thing == seeds:
                a["seeds"][thingr] = {"amount": amount}
        else:
            if thing in [animals, seeds]:
                a[thing["name"]][thingr]["amount"] += amount
            if thing == tools:
                a["tools"][thingr]["durability"] = tools[thingr]["durability"]
            if thing == merch:
                a["merch"][thingr] += amount

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

    a = db["members"]
    a[str(message.author.id)]["merch"][eated] -= 1
    if a[str(message.author.id)]["merch"][eated] == 0:
        del a[str(message.author.id)]["merch"][eated]
    db["members"] = a
