from replit import db
from zstats import seeds, tools, softSearch, convertInt
import asyncio
import random
import time
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from commands.farming.crops import crops


async def plant(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        await message.channel.send(" n o ")
        return
    if db["members"][str(message.author.id)]["seeds"] == {}:
        await message.channel.send(" n o ")
        return
    if len(args) == 2:
        await message.channel.send(" what are you planting lol")
        return
    thing = random.randint(1, 35)
    if thing == 1:
        if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
            return
        await message.channel.send(
            "On the way over to plant some plants, you accidentally read a really dumb book and died. you paid 100 coins to be reborn."
        )
        a = db["members"]
        if a[str(message.author.id)]["money"] < 100:
            a[str(message.author.id)]["money"] = 0
        else:
            a[str(message.author.id)]["money"] -= 100
        db["members"] = a
        return

    seed = softSearch(seeds, args[2], ["name"])
    if not bool(seed):
        await message.channel.send("don't try to fool me, that's not a seed")
        return
    if seed not in db["members"][str(message.author.id)]["seeds"]:
        await message.channel.send(" you dont have that")
        return

    tool = None
    for i in tools:
        if tools[i] != "tools":
            if tools[i]["animal"] == "seed":
                if tools[i]["name"] in db["members"][str(message.author.id)]["tools"]:
                    tool = tools[i]["name"]
    if tool == None:
        await message.channel.send(" buy a watering can first")
        return

    if len(args) == 3:
        amount = 1
    if len(args) >= 4 and args[3] in ["a", "all", "max"]:
        amount = db["members"][str(message.author.id)]["seeds"][seed]["amount"]
    elif len(args) >= 4:
        amount = convertInt(args[3])
        if not bool(amount):
            amount = 1
    if amount <= 0:
        await message.channel.send(" cant be less than 0 bro")
        return

    if db["members"][str(message.author.id)]["land"]["crops"] == {}:
        return "you don't have any fields to plant stuff in lol"
    if len(args) >= 5:
        length = len(
            list(db["members"][str(message.author.id)]["land"]["crops"].values())
        )
        if args[4].isnumeric() and int(args[4]) == length:
            place = int(args[4]) - 1
            print(place)
            field = list(db["members"][str(message.author.id)]["land"]["crops"])[place]
            if (
                100
                - db["members"][str(message.author.id)]["land"]["crops"][field]["total"]
                < amount
            ):
                return "there isnt enough space on that field to plant stuff"
            if (
                seeds[seed]["result"]
                in db["members"][str(message.author.id)]["land"]["crops"][field][
                    "crops"
                ]
            ):
                return "you already planted that in that field"
    else:
        field = False
        for i in db["members"][str(message.author.id)]["land"]["crops"]:
            if (
                100 - db["members"][str(message.author.id)]["land"]["crops"][i]["total"]
                > amount
                and seeds[seed]["result"]
                not in db["members"][str(message.author.id)]["land"]["crops"][i][
                    "crops"
                ]
            ):
                field = i
        if field == False:
            return "bruh you don't have enough land to plant stuff on, or you already planted the seed in all of your fields"

    if amount > db["members"][str(message.author.id)]["seeds"][seed]["amount"]:
        await message.channel.send(" thats more than you have nerd")
        return
    if amount >= db["members"][str(message.author.id)]["tools"][tool]:
        amount = db["members"][str(message.author.id)]["tools"][tool]
        a = db["members"]
        del a[str(message.author.id)]["tools"][tool]
        db["members"] = a
        await message.channel.send(f"your {tool} broke LOL")
    else:
        a = db["members"]
        a[str(message.author.id)]["tools"][tool] -= amount
        db["members"] = a

    thingr = random.randint(1, 2)
    if thingr == 1:
        things = [
            "water",
            "watering",
            "undie",
            "hydrate",
            "sea",
            "ocean",
            "water",
            "drink",
            "plant",
            "water",
            "slurp",
            "ice",
            "snow",
            "pool",
            "lake",
        ]
        thingtotype = random.choice(things)
        await message.channel.send(
            f"{message.author.name} you're planting `{amount} {seed}(s)`, but plants need water, type `{thingtotype}` in the chat now"
        )

        channel = message.channel

        reply = None

        def check(m):
            return m.content.lower() == thingtotype and m.author.id == message.author.id

        try:
            reply = await client.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await channel.send("idiot your plants died")
            a = db["members"]
            a[str(message.author.id)]["seeds"][seed]["amount"] -= amount
            if a[str(message.author.id)]["seeds"][seed]["amount"] == 0:
                del a[str(message.author.id)]["seeds"][seed]
            db["members"] = a
            return
    elif thingr == 2:
        emojis = ["🌾", "🌱", "🌿"]
        emoji = random.choice(emojis)
        await message.reply(
            f"you planted your plants, but now it's time to water them, react to this message with {emoji}"
        )

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == emoji

        try:
            reaction, user = await client.wait_for(
                "reaction_add", timeout=15.0, check=check
            )
        except asyncio.TimeoutError:
            await message.channel.send("idiot your plants died")
            a = db["members"]
            a[str(message.author.id)]["seeds"][seed]["amount"] -= amount
            if a[str(message.author.id)]["seeds"][seed]["amount"] == 0:
                del a[str(message.author.id)]["seeds"][seed]
            db["members"] = a
            return

    amountwait = (
        seeds[seed]["stages"][0] if "stages" in seeds[seed] else seeds[seed]["growtime"]
    )
    prefix = db["server"][str(message.guild.id)]["prefix"]
    plantr = seeds[seed]["result"]
    tts = [
        f" You watered your plants. Wait `{amountwait/1000}` seconds before collecting them, and use `{prefix} collect {plantr}` to collect them.",
        f"yessir, plants are watered and are now growing, see them using `{prefix} crops`",
        f"plants are successfully watered. they will be ready to collect in `{amountwait/1000}`s.",
        f"plants watered. be sure to collect them in `{amountwait/1000}s` using `{prefix} collect {plantr}`.",
    ]

    a = db["members"]
    now = int(round(time.time() * 1000))

    a[str(message.author.id)]["land"]["crops"][field]["crops"][
        seeds[seed]["result"]
    ] = {
        "name": seeds[seed]["name"],
        "cooldown": now,
        "amount": amount,
    }
    a[str(message.author.id)]["land"]["crops"][field]["total"] += amount
    if "stages" in seeds[seed]:
        a[str(message.author.id)]["land"]["crops"][field][seeds[seed]["result"]][
            "start"
        ] = now
        a[str(message.author.id)]["land"]["crops"][field][seeds[seed]["result"]][
            "stage"
        ] = 0

    a[str(message.author.id)]["seeds"][seed]["amount"] -= amount
    if a[str(message.author.id)]["seeds"][seed]["amount"] == 0:
        del a[str(message.author.id)]["seeds"][seed]
    db["members"] = a

    tt = random.choice(tts)
    msg = await message.reply(
        tt,
        components=[
            Button(style=ButtonStyle.blue, label="View Crops"),
            Button(style=ButtonStyle.grey, label="❌"),
        ],
    )

    try:
        res = await client.wait_for("button_click", timeout=60)
    except asyncio.TimeoutError:
        await msg.edit(components=[])
    else:
        if res.author == message.author:
            if res.component.label == "❌":
                await msg.edit(components=[])
                return
            if res.component.label == "View Crops":
                await msg.edit(components=[])
                mass = message
                mass.content = "i crops"
                await crops(mass, client)
