from replit import db
from zstats import convertInt
import random


async def donate(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        await message.channel.send("you don't exist LOL")
        return
    if len(args) == 2:
        await message.channel.send("how much are you donating lol")
        return
    if db["members"][str(message.author.id)]["money"] == 0:
        await message.channel.send("you have no money, dummy")
        return

    thing = random.randint(1, 35)
    if thing == 1:
        things = [
            "pebble",
            "stone",
            "slipper",
            "sweater",
            "ice",
            "tree branch",
            "neighbour's crops",
        ]
        thing2 = random.choice(things)
        await message.channel.send(
            f"On the way over to donate some money, you accidentally slipped on a slippery {thing2} and died. you paid 100 coi3ns to be reborn."
        )
        a = db["members"]
        if a[str(message.author.id)]["money"] < 100:
            a[str(message.author.id)]["money"] = 0
        else:
            a[str(message.author.id)]["money"] -= 100
        db["members"] = a
        return
    if db["members"][str(message.author.id)]["reputation"] < 250:
        await message.channel.send(
            "market: nah, your reputation is too low so i'm not giving you anything"
        )
        chance = random.randint(1, 5)
        if chance > 3:
            a = db["members"]
            a[str(message.author.id)]["reputation"] += chance
            db["members"] = a
        return

    gave = convertInt(args[2])
    if not bool(gave) and args[2] not in ["a", "all", "max"]:
        await message.channel.send("gotta say a number")
        return
    if gave > db["members"][str(message.author.id)]["money"]:
        await message.channel.send("you don't have that much")
        return
    if gave == 0:
        await message.channel.send("how you gonna give 0 coins u dumdum")
        return

    if args[2] in ["all", "a", "max"]:
        gave = db["members"][str(message.author.id)]["money"]
    if gave <= 0:
        await message.channel.send("cant donate less than 1")
        return

    if db["members"][str(message.author.id)]["reputation"] >= 750:
        await message.channel.send(
            "your reputation is too high, thanks for the free money nerd"
        )
        a = db["members"]
        a[str(message.author.id)]["money"] -= gave
        db["members"] = a
        return

    a = db["members"]
    a[str(message.author.id)]["money"] -= gave
    repgained = int(round(gave / 3))
    a[str(message.author.id)]["reputation"] += repgained
    if a[str(message.author.id)]["reputation"] > 1000:
        repgained = 1000
        a[str(message.author.id)]["reputation"] = 1000
    nowmoney = a[str(message.author.id)]["money"]
    nowrep = a[str(message.author.id)]["reputation"]
    db["members"] = a
    await message.reply(
        f"You gave `{gave}` coins to the marketplace. Your reputation increased by `{repgained}`. \nYou now have `{nowmoney}` coins and `{nowrep}` reputation."
    )
