from replit import db
import random
from zstats import convertInt


async def dice(message, client):
    if str(message.author.id) not in db["members"]:
        await message.channel.send("::")
        return
    args = message.content.split(" ")
    if len(args) == 2:
        await message.channel.send("you gotta bet something bro")
        return

    if args[2] in ["a", "all", "max"]:
        amount = db["members"][str(message.author.id)]["money"]
        if db["members"][str(message.author.id)]["money"] > 100000:
            amount = 100000
    else:
        amount = convertInt(args[2])
        if not bool(amount):
            await message.channel.send("bet a number")
            return

    if amount > db["members"][str(message.author.id)]["money"]:
        await message.channel.send("thats more than u have lol")
        return
    if db["members"][str(message.author.id)]["reputation"] > 1000:
        await message.channel.send(
            "your reputation is too high to gamble,go do something better with your money"
        )
        return
    if db["members"][str(message.author.id)]["money"] == 0:
        await message.channel.send("You have no money. '-'")
        return
    if amount <= 0:
        await message.channel.send("can't bet less than 0")
        return
    you = random.randint(1, 6)
    other = random.randint(1, 6)
    a = db["members"]
    a[str(message.author.id)]["amounts"]["gambled"] += amount
    db["members"] = a
    if you > other:
        amountwon = int(round(amount / 2))
        await message.channel.send(
            f"{message.author.mention} got `{you}` and they got `{other}`, you win `{amountwon}` coins."
        )
        a = db["members"]
        a[str(message.author.id)]["money"] += amountwon
        db["members"] = a
    if other > you:
        await message.channel.send(
            f"{message.author.mention}you got `{you}` and they got `{other}`, you lose `{amount}` coins."
        )
        a = db["members"]
        a[str(message.author.id)]["money"] -= amount
        db["members"] = a
    if other == you:
        await message.channel.send(
            f"{message.author.mention} you got `{you}` and they got `{other}`, nothing happened. :/"
        )
        return
