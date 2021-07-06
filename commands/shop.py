import discord
from replit import db
from zstats import softSearch, getShop, pages
from math import ceil

async def shop(message, client):
    args = message.content.split(" ")

    obj = {"animals": {}, "tools": {}, "seeds": {}, "merch": {}}
    getShop(
        obj,
        db["members"][str(message.author.id)]["location"]
        if str(message.author.id) in db["members"]
        else "default",
    )
    animals, tools, seeds, merch = (
        obj["animals"],
        obj["tools"],
        obj["seeds"],
        obj["merch"],
    )

    check = []
    check.extend(
        list(animals.keys())
        + list(tools.keys())
        + list(merch.keys())
        + list(seeds.keys())
    )

    allStats = []
    allStats.append(animals.copy())
    allStats.append(tools.copy())
    allStats.append(merch.copy())
    allStats.append(seeds.copy())

    if len(args) == 2:
        await message.channel.send("**shops:** \n-animals\n-tools\n-seeds\n-merch")
        return

    if args[2] not in ["animals", "tools", "merch", "merchandise", "seeds"]:
        search = softSearch(check, args[2], ["name"])

        if not bool(search):
            await message.channel.send("thats not a shop or item you can look at")
            return

        items = [d[search] for d in allStats if search in d]

        item = items[0]

        if item in list(animals.values()):

            name = item["name"]
            cost = item["cost"]
            sellcost = item["sellcost"]
            tv = item["tradevalue"]
            tool = item["tool"]
            result = item["result"]
            cooldown = item["cooldown"] / 1000
            e = discord.Embed(
                title=f"{name}:",
                description=f"Cost: `{cost}`\nSell amount: `{sellcost}`\nTrade Value: `{tv}`\nTool: `{tool}`\nResult: `{result}`\nCooldown: `{cooldown} seconds`",
                colour=discord.Colour.red(),
            )
            await message.channel.send(embed=e)
            return
        elif item in list(tools.values()):
            name = item["name"]
            cost = item["cost"]
            sellcost = item["sellcost"]
            tv = item["tradevalue"]
            durability = item["durability"]
            animal = (
                ", ".join(item["animal"])
                if type(item["animal"]) is list
                else item["animal"]
            )
            e = discord.Embed(
                title=f"{name}:",
                description=f"Cost: `{cost}`\nSell amount: `{sellcost}`"
                + (
                    ""
                    if "description" not in item
                    else f"\nDescription: {item['description']}"
                )
                + f"\nTrade Value: `{tv}`\nTo use: `{animal}`\nDurability: `{durability}`",
                colour=discord.Colour.red(),
            )
            await message.channel.send(embed=e)
            return
        elif item in list(seeds.values()):
            name = item["name"]
            cost = item["cost"]
            sellcost = item["sellcost"]
            growtime = (
                f"Grow time: `{item['stages'][0]/1000} seconds`\nCooldown: `{item['stages'][1]/1000} seconds`\nLifespan: `{item['stages'][2]/1000} seconds`"
                if "stages" in item
                else f"Grow time: `{item['growtime']/1000} seconds`"
            )
            result = item["result"]
            tv = item["tradevalue"]
            e = discord.Embed(
                title=f"{name}:",
                description=f"Cost: `{cost}`\nSell amount: `{sellcost}`\nTrade Value: `{tv}`\n{growtime}\nResult: `{result}`",
                colour=discord.Colour.red(),
            )
            await message.channel.send(embed=e)
            return
        elif item in list(merch.values()):
            name = item["name"]
            cost = item["cost"]
            sellcost = item["sellcost"]
            tv = item["tradevalue"]
            e = discord.Embed(
                title=f"{name}:",
                description=f"Cost: `{cost}`\nSell amount: `{sellcost}`"
                + (
                    ""
                    if "description" not in item
                    else f"\nDescription: {item['description']}"
                )
                + f"\nTrade Value: `{tv}`",
                colour=discord.Colour.red(),
            )
            await message.channel.send(embed=e)
            return

    prefix = db["server"][str(message.guild.id)]["prefix"]
    e = discord.Embed(
        title=f"",
        description=f"Use `{prefix} buy (thing)` to buy something",
        colour=discord.Colour.gold(),
    )
    shop = args[2]
    if len(args) == 3:
        i = 0
        amount = 0
    if len(args) >= 4 and args[3].isnumeric():
        i = int(int(args[3]) - 1)
        amount = args[3]
    else:
        i = 0
        amount = 0
    shopObj = {"animals": animals, "tools": tools, "seeds": seeds, "merch": merch}
    maxPage = ceil(len(shopObj[shop]) / 9)

    if i >= maxPage:
        i = maxPage - 1
        amount = maxPage

    i *= 9
    a2 = i + 9

    if shop == "animals":
        dictCopy = dict(animals)
        del dictCopy["name"]

        ints = {k: v for k, v in dictCopy.items() if type(v["cost"]) is int}

        strs = {k: v for k, v in dictCopy.items() if type(v["cost"]) is str}

        intsSorted = sorted(ints.keys(), key=lambda x: int(ints[x]["cost"]))

        strsSorted = sorted(strs.keys(), key=lambda x: str(strs[x]["cost"]))

        r = intsSorted + strsSorted

        await pages(
            message, 
            client, 
            [{"name": animals[j]["name"], "value": f"Cost: `{animals[j]['cost']}`\nSell amount: `{animals[j]['sellcost']}`\nNeeded tool: `{animals[j]['tool']}`\nTrade value: `{animals[j]['tradevalue']}`\nResult: `{animals[j]['result']}`\n"} for j in r],
            9,
            startPage = i/9 + 1,
            baseEmbed = e
        )
    elif shop == "tools":
        dictCopy = dict(tools)
        del dictCopy["name"]

        ints = {k: v for k, v in dictCopy.items() if type(v["cost"]) is int}

        strs = {k: v for k, v in dictCopy.items() if type(v["cost"]) is str}

        intsSorted = sorted(ints.keys(), key=lambda x: int(ints[x]["cost"]))

        strsSorted = sorted(strs.keys(), key=lambda x: str(strs[x]["cost"]))

        r = intsSorted + strsSorted

        await pages(
            message, 
            client, 
            [{"name": tools[j]["name"], "value": f"Cost: `{tools[j]['cost']}`\nSell amount: `{tools[j]['sellcost']}`\nUse on: `{', '.join(tools[j]['animal']) if type(tools[j]['animal']) is list else tools[j]['animal']}`\nTrade value: `{tools[j]['tradevalue']}`\nResult: `{tools[j]['result']}`\n"} for j in r],
            9,
            startPage = i/9 + 1,
            baseEmbed = e
        )
    elif shop == "merch":
        dictCopy = dict(merch)
        del dictCopy["name"]

        ints = {k: v for k, v in dictCopy.items() if type(v["cost"]) is int}

        strs = {k: v for k, v in dictCopy.items() if type(v["cost"]) is str}

        intsSorted = sorted(ints.keys(), key=lambda x: int(ints[x]["cost"]))

        strsSorted = sorted(strs.keys(), key=lambda x: str(strs[x]["cost"]))

        r = intsSorted + strsSorted

        await pages(
            message, 
            client, 
            [{"name": merch[j]["name"], "value": f"Cost: `{merch[j]['cost']}`\nSell amount: `{merch[j]['sellcost']}`\nTrade value: `{merch[j]['tradevalue']}`"} for j in r],
            9,
            startPage = i/9 + 1,
            baseEmbed = e
        )

    elif shop == "seeds":
        dictCopy = dict(seeds)
        del dictCopy["name"]

        ints = {k: v for k, v in dictCopy.items() if type(v["cost"]) is int}

        strs = {k: v for k, v in dictCopy.items() if type(v["cost"]) is str}

        intsSorted = sorted(ints.keys(), key=lambda x: int(ints[x]["cost"]))

        strsSorted = sorted(strs.keys(), key=lambda x: str(strs[x]["cost"]))

        r = intsSorted + strsSorted

        growtime = { 
            seeds[j]["name"]: (
                f"Grow time: `{seeds[j]['stages'][0]/1000}`\nCooldown: `{seeds[j]['stages'][1]/1000}`\nLifespan: `{seeds[j]['stages'][2]/1000}`"
                if "stages" in seeds[j]
                else f"Grow time: {seeds[j]['growtime']/1000}"
            ) for j in r
        }

        await pages(
            message, 
            client, 
            [{"name": seeds[j]["name"], "value": f"Cost: `{seeds[j]['cost']}`\nSell amount: `{seeds[j]['sellcost']}`\n{growtime[seeds[j]['name']]}\nTrade value: `{seeds[j]['tradevalue']}`"} for j in r],
            9,
            startPage = i/9 + 1,
            baseEmbed = e
        )
    thing = int(amount) + 1
    thing = str(thing)
    if thing == "1":
        thing = "2"
    e.set_footer(
        text=f"Use <{prefix} shop {args[2].lower()} {thing}> to see the next page of {args[2].lower()}. Page {int(thing) - 1}/{maxPage}"
    )
    e.set_author(name=f"{args[2].lower()} shop:", icon_url=message.author.avatar_url)
