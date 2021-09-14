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

    obj = {"animals": {}, "tools": {}, "seeds": {}, "merch": {}, "land": {}}
    getShop(obj, db["members"][str(message.author.id)]["location"])
    animals, tools, seeds, merch, land = (
        obj["animals"],
        obj["tools"],
        obj["seeds"],
        obj["merch"],
        obj["land"],
    )

    for i in [seeds, merch, tools, animals, land]:
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
    if cost * amount > db["members"][str(message.author.id)]["money"]:
        return f" you're too poor to buy `{amount} {key}(s)` at `{cost}` each."
        return
    if key in tools:
        amount = 1
        thing = tools

    async def buye(amount):
        a = db["members"]
        r = cost * amount
        if thing == animals:
            now = int(round(time.time() * 1000))
            if a[str(message.author.id)]["land"]["animals"] == {}:
                return "you don't have any pens to put the animals into, buy one first"

            pens = []
            for i in a[str(message.author.id)]["land"]["animals"]:
                if a[str(message.author.id)]["land"]["animals"][i]["total"] < 50:
                    pens.append(i)
            for i in pens:
                if (
                    50 - a[str(message.author.id)]["land"]["animals"][i]["total"]
                    < amount
                ):
                    newmount = (
                        50 - a[str(message.author.id)]["land"]["animals"][i]["total"]
                    )
                    amount = amount - newmount
                    a[str(message.author.id)]["land"]["animals"][i]["animals"][key] = {
                        "amount": newmount,
                        "lastused": now,
                        "lastbred": now,
                    }
                    a[str(message.author.id)]["land"]["animals"][i]["total"] = 50
                    continue
                elif (
                    50 - a[str(message.author.id)]["land"]["animals"][i]["total"]
                    > amount
                ):
                    a[str(message.author.id)]["land"]["animals"][i]["animals"][key] = {
                        "amount": amount,
                        "lastused": now,
                        "lastbred": now,
                    }
                    a[str(message.author.id)]["land"]["animals"][i]["total"] += amount

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
        if thing == land:
            amount = (
                len(list(db["members"][str(message.author.id)]["land"]["crops"])) + 1
            )
            print(key)
            if key == "pen":
                fartat = "animals"
                mass = "Animal Pen"
            if key == "field":
                fartat = "crops"
                mass = "Crop Field"
            mart = f"{mass} {amount}"
            print(mart)
            a[str(message.author.id)]["land"][fartat][mart] = {
                f"{fartat}": {},
                "total": 0,
                "name": mart,
            }
            amount = 1
        a[str(message.author.id)]["money"] -= r
        nowmoney = a[str(message.author.id)]["money"]
        a[str(message.author.id)]["amounts"]["bought"] += amount

        repgain = random.randint(1, 4)
        repmsg = ""
        if repgain == 1:
            rep = db["members"][str(message.author.id)]["reputation"]
            gain = random.randint(1, 3)
            rep = gain
            repmsg = f"market: thanks for buying that thing, i really wanted to sell it **reputation +{gain}**"
            db["members"][str(message.author.id)]["reputation"] = rep
        db["members"] = a

        thingstosay = [
            f"You bought `{amount} {key}(s)` for `{r} coins`. You now have `{nowmoney} coins`.",
            f"purchase successful, you paid `{r} coins` for `{amount} {key}(s)`.",
            f"yessir `{amount} {key}(s)` purchased",
            f"{message.author.name} bought `{amount} {key}(s)`",
            f"you paid `{r} coins` for `{amount} {key}(s)`.",
            f"mk, {message.author.name} bought `{amount} {key}(s)`",
            f"ty for `{r} coins` {message.author.mention}, please come again",
            f"hee hee hee money for me and `{key}(s)` for you",
            f"tysm tysm {message.author.mention}, have a good day",
            f"{message.author.name} just bought `{amount} {key}(s)`, from the market",
            f"{message.author.name} bought some `{key}(s)`, they're now {nowmoney} coins poor",
        ]
        thingsaid = random.choice(thingstosay)
        out = f"{thingsaid}\n{repmsg}"

        return out

    return await buye(amount)
