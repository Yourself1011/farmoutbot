from replit import db
from time import time
from zstats import animals, tools, merch, seeds
from math import floor
import discord
from os import environ


async def vote(id, site, client):
    a = db["members"]
    discordUser = await client.fetch_user(id)

    if environ.get("ENV") == 'dev': print('yes'); return
    if id not in a:
        print('ehee')
        return await discordUser.send(
            "Thanks for voting for farmout! Create an account for the bot to start earning rewards for voting!\nDont like these messages? Create an account and use `set votedm off`"
        )
    if "votedm" in a[id]["settings"] and a[id]["settings"]["votedm"]:
        print('ahoo')
        await discordUser.send(
            "thanks for voting for farmout! you got 2 epicboxes that you can eat for items\nDont like these messages? use `set votedm off`"
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
