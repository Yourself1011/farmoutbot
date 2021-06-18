import random
from replit import db
import asyncio


async def thinghappen(message, client):
    if str(message.author.id) not in db["members"]:
        return
    if db["members"][str(message.author.id)]["animals"] == {}:
        return
    if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
        return
    thing = False
    for i in db["members"][str(message.author.id)]["animals"]:
        if db["members"][str(message.author.id)]["animals"][i]["amount"] > 5:
            thing = True
    if thing == False:
        return

    animal = random.choice(
        list(db["members"][str(message.author.id)]["animals"].keys())
    )
    while db["members"][str(message.author.id)]["animals"][animal]["amount"] < 5:
        animal = random.choice(
            list(db["members"][str(message.author.id)]["animals"].keys())
        )
    amount = random.randint(
        1,
        int(
            round(
                db["members"][str(message.author.id)]["animals"][animal]["amount"] / 4
            )
        ),
    )

    diseases = [
        "big belly disease",
        "too many bugs disease",
        "dumb disease",
        "listening to im blue for 10 hours disease",
        "pls beg dank memer thingy disease",
        "fat illness",
        "tree illness",
        "stinky old man sickness",
        "too much illness",
        "big fat fart big sickness",
        "python disease",
        "single quote disease",
    ]
    disease = random.choice(diseases)
    thingr = random.randint(1, 5)
    if thingr in [1, 2]:
        amountpaid = random.randint(1, 5)
    if thingr in [3, 4]:
        amountpaid = random.randint(15, 35)
    if thingr == 5:
        amountpaid = random.randint(50, 100)
    if amountpaid > db["members"][str(message.author.id)]["money"]:
        amountpaid = int(round(db["members"][str(message.author.id)]["money"] / 5))
    await message.channel.send(
        f"{message.author.mention} hey {amount} of your `{animal}(s)` have gotten {disease}, say `pay` to pay for their {amountpaid} coin treatment or they will die"
    )

    channel = message.channel
    reply = None

    def check(m):
        return m.content.lower() == "pay" and m.author.id == message.author.id

    try:
        reply = await client.wait_for("message", timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await channel.send("idiot your animals died")
        a = db["members"]
        a[str(message.author.id)]["animals"][animal]["amount"] -= amount
        if a[str(message.author.id)]["animals"][animal]["amount"] == 0:
            del a[str(message.author.id)]["animals"][animal]
        db["members"] = a
        return
    else:
        await channel.send(
            f"your animals are saved, but you paid {amountpaid*amount} coins for the medical bills"
        )
        a = db["members"]
        a[str(message.author.id)]["money"] -= amountpaid * amount
        if a[str(message.author.id)]["money"] < 0:
            a[str(message.author.id)]["money"] = 0
        db["members"] = a
        return
