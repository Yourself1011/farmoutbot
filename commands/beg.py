from replit import db
import random
import time


async def beg(message, client):
    if str(message.author.id) not in db["members"]:
        await message.channel.send("your farm doesn't exist yet, do `start` first")
        return
    if db["members"][str(message.author.id)]["reputation"] <= 250:
        await message.channel.send(
            f"{message.author.mention} Your reputation is too low, it has to be at least `250` for this command to work."
        )
        return
    now = int(round(time.time() * 1000))
    if (
        "beg" in db["members"][str(message.author.id)]["cooldowns"]
        and db["members"][str(message.author.id)]["cooldowns"]["beg"] < now
    ):
        now = int(round(time.time() * 1000))
        if db["members"][str(message.author.id)]["cooldowns"]["beg"] + 30000 > now:
            now2 = int(round(time.time() * 1000))
            f = db["members"][str(message.author.id)]["cooldowns"]["beg"] - now2
            f = str(f)
            newvar = 30000 + db["members"][str(message.author.id)]["cooldowns"]["beg"]
            e = round((newvar - now2) / 1000)
            await message.channel.send(f"cant beg now, wait `{str(e)}` seconds.")
            return

    if db["members"][str(message.author.id)]["money"] >= 1000:
        await message.channel.send("you have too much money to beg. ")
        return
    coins = 0
    rep = 0
    thing = random.randint(1, 3)
    if thing == 1:
        rep = random.randint(20, 50)
        await message.channel.send(
            f"**market:** no.\n{message.author.mention} you lost `{rep} rep`"
        )
    if thing == 2:
        rep = random.randint(5, 10)
        coins = random.randint(5, 10)
        await message.channel.send(
            f"**market:** UGH fineeeee\n{message.author.mention} you gained `{coins} coins` but lost `{rep} rep`."
        )
    if thing == 3:
        coins = random.randint(10, 20)
        await message.channel.send(
            f"**market:** yessir\n{message.author.mention} you gained `{coins} coins`"
        )
    a = db["members"]
    a[str(message.author.id)]["reputation"] -= rep
    a[str(message.author.id)]["money"] += coins
    db["members"] = a
