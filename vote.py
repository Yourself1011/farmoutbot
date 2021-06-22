from replit import db
from time import time
from zstats import animals, tools, merch, seeds
from math import floor
import discord


async def vote(id, site, client):
    a = db["members"]
    discordUser = await client.fetch_user(id)

    if id not in a:
        return await discordUser.send(
            "Thanks for voting for farmout! Create an account for the bot to start earning rewards for voting!"
        )

    await discordUser.send(
        "thanks for voting for farmout! you got 2 epicboxes that you can eat for items"
    )

    user = a[id]
    user["cooldowns"][site] = (floor(time()) + 43200) * 10

    rewards = [["epicbox", 2]]

    for i in rewards:
        if i[0] in merch:
            if i[0] in user["merch"]:
                user["merch"][i[0]] += i[1]

            else:
                user["merch"][i[0]] = i[1]

    db["members"] = a
