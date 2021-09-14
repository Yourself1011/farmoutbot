import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from replit import db
from time import time
from math import floor


async def vote(message, client):
    sites = ["discordbotlist.com", "top.gg"]
    desc = ""

    for i in sites:
        if (
            str(message.author.id) not in db["members"]
            or i not in db["members"][str(message.author.id)]["cooldowns"]
        ):
            desc += f"{i}: Unknown\n"

        elif db["members"][str(message.author.id)]["cooldowns"][i] / 10 <= time():
            desc += f"{i}: Now!\n"

        else:
            desc += f"{i}: <t:{floor(db['members'][str(message.author.id)]['cooldowns'][i] / 10)}:R>\n"

    embed = discord.Embed(title="you can vote again in", description=desc)
    await message.channel.send(
        'vote for farmout by clicking the "vote" button\nfrom voting, you can support our bot and get 2 epicboxes which you can eat\nyou can vote every 12 hours',
        embed=embed,
        components=[
            [
                Button(
                    style=ButtonStyle.URL,
                    label="discordbotlist.com",
                    url="https://discordbotlist.com/bots/farmout/upvote",
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="top.gg",
                    url="https://top.gg/bot/795319933314662452/vote",
                ),
            ]
        ],
    )
