
# TEMPERARY THING IGNORE FOR NOW	NO IT"S NOT TEMPORARY ANYMORE


from replit import db
import discord
from math import floor
from random import randint
import random
from zstats import choosecolour

def mapFunc(x):
    return f"`{x[1]}x` **{x[0]['name']}**"


async def listtrades(message, client):
    user = db["members"][str(message.author.id)]
    if user["trades"]["lastTradeId"] != db["tradeId"]:

        m = db["members"]

        m[str(message.author.id)]["trades"] = {
            "lastTradeId": db["tradeId"],
            "tradeAmts": [0, 0, 0, 0, 0],
            "stock": [
                floor((500 / randint(200, 300)) * 10),
                floor((500 / randint(200, 300)) * 4),
                floor(500 / randint(200, 300)),
                floor(500 / randint(300, 400)),
                floor(500 / randint(400, 500)),
            ],
        }

        db["members"] = m

    user = db["members"][str(message.author.id)]

    e = discord.Embed(
        title="Trade Offers: ",
        description=f"Trades update every 6 hours. Next trade update <t:{(db['lastTradeDate'] + 1) * 21600}:R>",
        colour=choosecolour(),
    )
    for i in range(len(db["trades"])):
        give = db["trades"][i]["give"]
        get = db["trades"][i]["get"]

        giveVal = 0
        getVal = 0

        for j in give:
            giveVal += j[0]["tradevalue"] * j[1]

        for j in get:
            getVal += j[0]["tradevalue"] * j[1]

        e.add_field(
            name=f'{i} (Stock: {user["trades"]["stock"][i] - user["trades"]["tradeAmts"][i]}): ',
            value=f'{"~~" if user["trades"]["tradeAmts"][i] >= user["trades"]["stock"][i] else ""}*Give (trade value: {giveVal}):* {", ".join(list(map(mapFunc, give)))}\n*Get (trade value: {getVal}):* {", ".join(list(map(mapFunc, get)))}{"~~" if user["trades"]["tradeAmts"][i] >= user["trades"]["stock"][i] else ""}',
            inline=False,
        )

    prefix = db["server"][str(message.guild.id)]["prefix"]
    e.set_footer(
        text=f"Use <{prefix} trade (trade number)> to request a trade. If your reputation is too low, the trade may be rejected."
    )
    await message.channel.send(embed=e)
