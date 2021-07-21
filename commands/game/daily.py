from replit import db
import time
import datetime
import random
from zstats import dailys


async def daily(message, client):
    if str(message.author.id) not in db["members"]:
        await message.channel.send("market: make an account first dumum")
        return
    args = message.content.split(" ")
    if len(args) != 2 and args[2] == "show":
        lastdaily = db["members"][str(message.author.id)]["cooldowns"]["lastdaily"]
        await message.channel.send(f"your last daily was {lastdaily}")
        return
    now = int(round(time.time() * 1000))
    if db["members"][str(message.author.id)]["cooldowns"]["daily"] + 86400000 > now:
        now2 = int(round(time.time() * 1000))
        f = db["members"][str(message.author.id)]["cooldowns"]["daily"] - now2
        f = str(f)
        newvar = 86400000 + db["members"][str(message.author.id)]["cooldowns"]["daily"]
        e = round((newvar - now2) / 1000)
        e = str(datetime.timedelta(seconds=e))

        await message.channel.send(
            f"market: it's called daily for a reason, wait `{e}` (hours:minutes:seconds) before coming back"
        )
        return
    thing = random.randint(1, 35)

    one = round(500 / 25)
    two = round(500 / 5)
    moneygained = random.randint(one, two)

    a = db["members"]

    if db["members"][str(message.author.id)]["cooldowns"]["daily"] > now - (
        86400000 * 2
    ):
        a[str(message.author.id)]["cooldowns"]["streak"] += 1

    else:
        a[str(message.author.id)]["cooldowns"]["streak"] = 0

    streak = a[str(message.author.id)]["cooldowns"]["streak"]

    streakMulti = streak * 0.5 * moneygained

    totalmoneygained = (
        round(moneygained + streakMulti) if not bool(streak) else moneygained
    )

    a[str(message.author.id)]["money"] += totalmoneygained
    a[str(message.author.id)]["cooldowns"]["daily"] = now
    db["members"] = a

    dail = random.choice(dailys)
    await message.channel.send(
        f"you gained `{moneygained}` coins + `{streakMulti}` from streak {dail}\nyour current streak is `{streak} days in a row`"
    )
    return
