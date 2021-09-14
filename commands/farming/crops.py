from replit import db
import discord
import time
from zstats import seeds, merch, pages, choosecolour
import random
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio
from commands.profile.inventory import inventory


async def crops(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        await message.channel.send("make an account first strumfum")
        return
    if db["members"][str(message.author.id)]["land"]["crops"] == {}:
        await message.channel.send("no fields here")
        return

    fields = list(db["members"][str(message.author.id)]["land"]["crops"])
    field = fields[0]
    feld = 0
    if len(args) >= 3 and args[2].lower() == "rename":
        if len(args) == 3:
            return "which field u renaming lol"
        if int(args[3]) > len(fields):
            return "that's not a field"

        fields = db["members"][str(message.author.id)]["land"]["crops"]
        field = list(fields)[int(args[3]) - 1]
        print(field)
        print(args[4])

        newname = args[4]
        a = db["members"][str(message.author.id)]
        a["land"]["crops"][field]["name"] = newname
        print(a["land"]["crops"])
        db["members"][str(message.author.id)] = a
        print(db["members"][str(message.author.id)]["land"]["crops"][field]["name"])

        return f"you renamed `{field}` to `{args[4]}`"

    # if len()

    if (
        len(args) == 3
        and args[2].isnumeric()
        and int(args[2]) <= len(fields)
        and int(args[2]) > 0
    ):
        feld = max(min(int(int(args[2]) - 1), len(fields)), 0)
        field = fields[feld]
    e = discord.Embed(title=f"", colour=choosecolour())
    e.set_author(
        name=f"{message.author.name}'s farm", icon_url=message.author.avatar_url
    )

    fields = db["members"][str(message.author.id)]["land"]["crops"]
    fields = list(fields.values())

    now = int(round(time.time() * 1000))
    await pages(
        message,
        client,
        [
            {
                "name": i["name"],
                "value": "\n".join(
                    [
                        f'\n\n**- {merch[j]["name"]}:**\nAmount: **{i["crops"][j]["amount"]}** | Status: **{str(round((j["cooldown"] + merch[k]["cooldown"]-now)/1000))+" secs" if j["cooldown"] + merch[k]["cooldown"] > now else "Ready!"}**'
                        for j, k in i["crops"]
                    ]
                )
                if i["crops"] != {}
                else "Empty ***cricket noises***",
            }
            for i in fields
        ],
        1,
        startPage=feld + 1,
        baseEmbed=e,
    )
