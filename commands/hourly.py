from replit import db
import time
import datetime
import random
from zstats import dailys


async def hourly(message, client):
    if str(message.author.id) not in db["members"]:
        await message.channel.send("market: make an account first dumumum")
        return
    now = int(round(time.time() * 1000))
    if db["members"][str(message.author.id)]["hourlytimer"] + 3600000 > now:
        now2 = int(round(time.time() * 1000))
        f = db["members"][str(message.author.id)]["hourlytimer"] - now2
        f = str(f)
        newvar = 3600000 + db["members"][str(message.author.id)]["dailytimer"]
        e = round((newvar - now2) / 1000)
        e = str(datetime.timedelta(seconds=e))

        await message.channel.send(
            f"market: it's called hourly for a reason, wait `{e}` (hours:minutes:seconds) before coming back"
        )
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
            f"On the way over to claim your hourly coins, you accidentally slipped on a slippery {thing2} and died. you paid 100 coins to be reborn."
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

    one = round(db["members"][str(message.author.id)]["reputation"] / 500)
    two = round(db["members"][str(message.author.id)]["reputation"] / 100)
    moneygained = random.randint(one, two)
    a = db["members"]
    a[str(message.author.id)]["money"] += moneygained
    a[str(message.author.id)]["hourlytimer"] = now
    db["members"] = a

    dail = random.choice(dailys)
    await message.channel.send(f"you gained `{moneygained}` coins {dail}")
    return
