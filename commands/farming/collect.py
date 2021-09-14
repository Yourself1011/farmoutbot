from replit import db
from zstats import merch, seeds, softSearch, locations
import time
import random
from math import floor
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio
from commands.farming.crops import crops


async def collect(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        return f" {message.author.mention}'s to-do list:\n\n1: make an account\n2: buy a seed\n3: buy a watering can\n4: plant the seeds\n5: water the plants\n6: wait for them to grow\n7: collect them"
    if db["members"][str(message.author.id)]["land"]["crops"] == {}:
        return " you dont have any fields u idiot"
    if len(args) == 2:
        return " what plant are you collecting lol"
    plant = softSearch(merch, args[2], ["name"])
    if not bool(plant):
        return " That's not a plant!"
    planted = False
    for i in db["members"][str(message.author.id)]["land"]["crops"]:
        if plant in db["members"][str(message.author.id)]["land"]["crops"][i]["crops"]:
            planted = True
            field = i
    if not planted:
        return " you haven't planted that"

    for i in seeds:
        if i != "name":
            if seeds[i]["result"] == plant:
                seed = seeds[i]["name"]

    growTime = (
        seeds[seed]["stages"][
            db["members"][str(message.author.id)]["land"]["crops"][field]["crops"][
                plant
            ]["stage"]
        ]
        if "stages" in seeds[seed]
        else seeds[seed]["growtime"]
    )

    now = int(round(time.time() * 1000))
    if (
        db["members"][str(message.author.id)]["land"]["crops"][field]["crops"][plant][
            "cooldown"
        ]
        + growTime
        > now
    ):
        now2 = int(round(time.time() * 1000))
        f = (
            db["members"][str(message.author.id)]["land"]["crops"][field]["crops"][
                plant
            ]["cooldown"]
            - now2
        )
        f = str(f)
        newvar = (
            growTime
            + db["members"][str(message.author.id)]["land"]["crops"][field]["crops"][
                plant
            ]["cooldown"]
        )
        e = round((newvar - now2) / 1000)
        return f" your plant isn't ready yet, wait `{str(e)}` seconds dumbo"
        return

    a = db["members"]
    amount = a[str(message.author.id)]["land"]["crops"][field]["crops"][plant]["amount"]
    chance = random.randint(0, 40)
    if not bool(chance) and amount > 5:
        if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
            return
        things = [
            "whoops ur fat little fingers slipped and pulled out the plants by accident",
            "you farted on the plants because you ate too many beans last night",
            "you sneezed and blew all the plants away",
            "some dumb animal came by and pulled them out",
            "you were too fat and squeezed them by acccident",
            "your plants ran away",
            "you accidentally planted them in a volcano",
        ]
        thing = random.choice(things)
        thing2 = random.randint(1, 3)
        if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
            return
        return f"{thing}. `{thing2}` of your plants died."
        a[str(message.author.id)]["land"]["crops"][field]["crops"][plant][
            "amount"
        ] -= thing2
        db["members"] = a
        return

    if (
        "stages" in seeds[seed]
        and now
        - a[str(message.author.id)]["land"]["crops"][field]["crops"][plant]["start"]
        > seeds[seed]["stages"][2]
    ):
        del a[str(message.author.id)]["land"]["crops"][field]["crops"][plant]
        return f"Oop your {plant} died of old age"
        db["members"] = a

    user = a[str(message.author.id)]
    location = locations[user["location"]]
    if (
        not location["defaultLife"]
        and (
            plant not in location["lifeOverrides"]
            or not location["lifeOverrides"][plant]
        )
    ) or (
        location["defaultLife"]
        and plant in location["lifeOverrides"]
        and location["lifeOverrides"][plant]
    ):
        amountLost = floor(
            max(
                user["land"]["crops"][field]["crops"][plant]["amount"]
                * location["deathRate"],
                min(10, user["land"]["crops"][field]["crops"][plant]["amount"]),
            )
        )

        user["land"]["crops"][field]["crops"][plant]["amount"] -= amountLost
        return f"Idiot your {plant}(s) couldn't live there and {amountLost} died."

        a[str(message.author.id)] = user

    location = locations[db["members"][str(message.author.id)]["location"]]

    amount = a[str(message.author.id)]["land"]["crops"][field]["crops"][plant]["amount"]
    a[str(message.author.id)]["land"]["crops"][field]["total"] -= amount
    fart = round(amount / 13)
    if fart > 10:
        fart = 10
    fart += amount
    fart *= (
        location["multis"][plant]
        if plant in location["multis"]
        else location["baseMulti"]
    )

    if plant not in a[str(message.author.id)]["merch"]:
        a[str(message.author.id)]["merch"][plant] = fart
    else:
        a[str(message.author.id)]["merch"][plant] += fart

    if "stages" in seeds[seed]:
        a[str(message.author.id)]["land"]["crops"][field]["crops"][plant][
            "cooldown"
        ] = now
        a[str(message.author.id)]["land"]["crops"][field]["crops"][plant]["stage"] = 1

    else:
        del a[str(message.author.id)]["land"]["crops"][field]["crops"][plant]

    db["members"] = a
    name = merch[plant]["name"]
    tts = [
        f"You collected `{fart}` {name}(s) from `{amount} {seed}(s)`. ",
        f"nice, you got `{fart}` {name}(s) from `{amount} {seed}(s)`.",
        f"from your `{amount} {seed}(s)` planted, you got `{fart}` {name}(s).",
        f"collection successful, `{fart}` {name}(s) were collected from `{amount} {seed}(s)`.",
    ]
    ts = random.choice(tts)
    msg = await message.reply(
        ts,
        components=[
            Button(style=ButtonStyle.blue, label="Quick Sell All"),
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
            if res.component.label == "Quick Sell All":
                name = name.split(" ")[0]
                cost = merch[name]["cost"]
                gained = fart * cost
                a = db["members"][str(message.author.id)]
                a["money"] += gained
                a["merch"][name] -= fart
                if a["merch"][name] == 0:
                    del a["merch"][name]
                db["members"][str(message.author.id)] = a
                return f"{message.author.mention} gained `{gained} coins` from selling the {name}(s)"
                await msg.edit(components=[])
            if res.component.label == "View Crops":
                await msg.edit(components=[])
                msg = message
                msg.content = "i crops"
                await crops(msg, client)
