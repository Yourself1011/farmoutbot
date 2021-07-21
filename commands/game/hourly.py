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

    one = round(500 / 500)
    two = round(500 / 100)
    moneygained = random.randint(one, two)
    a = db["members"]
    a[str(message.author.id)]["money"] += moneygained
    a[str(message.author.id)]["hourlytimer"] = now
    db["members"] = a

    dail = random.choice(dailys)
    await message.channel.send(f"you gained `{moneygained}` coins {dail}")
    return
