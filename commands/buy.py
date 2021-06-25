from replit import db
from zstats import market, convertInt, getShop
import time
import random
import asyncio


async def buy(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        return " babbon butt boo make an account or poo"

    if len(args) == 2:
        return " what are you buying lol"
    amount = 1

    # thingbought = args[2].lower()
    thing = None
    allPos = []
    objs = []

    obj = {"animals": {}, "tools": {}, "seeds": {}, "merch": {}}
    getShop(obj, db["members"][str(message.author.id)]["location"])
    animals, tools, seeds, merch = (
        obj["animals"],
        obj["tools"],
        obj["seeds"],
        obj["merch"],
    )

    for i in [seeds, merch, tools, animals]:
        possibilities = [j for j in list(i.keys()) if args[2] in j and j != "name"]
        if not bool(possibilities):
            continue
        allPos.extend(possibilities)
        for j in possibilities:
            objs.append(i)
    if not bool(allPos):
        return " that does not exist."
        return
    smallest = min(allPos, key=len)
    thing = objs[allPos.index(smallest)]
    item = thing[smallest]
    key = smallest
    if not str(item["cost"]).isnumeric():
        return " You can't buy that item!"
        return
    if len(args) == 4 and args[3] in ["a", "all", "max"]:
        if thing == tools:
            amount = 1
        else:
            amount = db["members"][str(message.author.id)]["money"] // item["cost"]
    elif len(args) == 4:
        if args[3] == "0":
            return "you bought 0 things. are you proud of yourself?"
        amount = convertInt(args[3])

        if not bool(amount):
            return " That's not a number"

    if amount <= 0:
        return "I should take that away from you and charge you the normal price"

    cost = item["cost"]
    rep = db["members"][str(message.author.id)]["reputation"]
    if rep > 450 and rep < 550:
        cost = cost
    if rep < 450 and rep > 250:
        cost = int(round(cost * 1.25))
    if rep < 250:
        cost = int(round(cost * 1.75))
    if rep > 550 and rep < 750:
        cost = int(round(cost * 0.95))
    if rep > 750:
        cost = int(round(cost * 0.9))
    regprice = item["cost"]
    if cost * amount > db["members"][str(message.author.id)]["money"]:
        return f" you're too poor to buy `{amount} {key}(s)` at `{cost}` each."
        return
    if key in tools:
        amount = 1
        thing = tools

    async def buye():
        a = db["members"]
        r = cost * amount
        if thing == animals:
            if key not in db["members"][str(message.author.id)]["animals"]:
                a[str(message.author.id)]["animals"][key] = {
                    "lastused": 0,
                    "amount": amount,
                }
            else:
                a[str(message.author.id)]["animals"][key]["amount"] += amount
        if thing == tools:
            a[str(message.author.id)]["tools"][key] = tools[key]["durability"]
        if thing == seeds:
            if key not in a[str(message.author.id)]["seeds"]:
                a[str(message.author.id)]["seeds"][key] = {"amount": amount}
            else:
                a[str(message.author.id)]["seeds"][key]["amount"] += amount
        if thing == merch:
            if key not in a[str(message.author.id)]["merch"]:
                a[str(message.author.id)]["merch"][key] = amount
            else:
                a[str(message.author.id)]["merch"][key] += amount
        a[str(message.author.id)]["money"] -= r
        nowmoney = a[str(message.author.id)]["money"]
        rep = a[str(message.author.id)]["reputation"]
        a[str(message.author.id)]["amounts"]["bought"] += amount
        db["members"] = a
        thingstosay = [
            f"You bought `{amount} {key}(s)` for `{r} coins`. You now have `{nowmoney} coins` and `{rep} reputation`.",
            f"purchase successful, you paid `{r} coins` for `{amount} {key}(s)`.",
            f"yessir `{amount} {key}(s)` purchased",
            f"{message.author.name} bought `{amount} {key}(s)`",
            f"you paid `{r} coins` for `{amount} {key}(s)`.",
        ]
        thingsaid = random.choice(thingstosay)
        out = thingsaid
        thingi = random.randint(1, 20)
        if thingi == 1:
            thingj = random.randint(4, 9)
            out += f"\n{message.author.mention} you lucky ducky, you bought something that the market was trying to get rid of and your rep increased by `{thingj}`."
            a = db["members"]
            a[str(message.author.id)]["reputation"] += thingj
            db["members"] = a
        if thingi == 2:
            thingj = random.randint(10, 20)
            out += f"\n{message.author.mention} bruh you bought something that the market didnt want to give, you lost `{thingj}` rep **and** `{int(round(thingj*2))} coins`."
            a = db["members"]
            if int(round(thingj * 2)) > a[str(message.author.id)]["money"]:
                a[str(message.author.id)]["money"] = 0
            else:
                a[str(message.author.id)]["money"] -= int(round(thingj * 2))
            a[str(message.author.id)]["reputation"] -= thingj
            db["members"] = a

        return (out, True)

    return await buye()