from replit import db
from zstats import convertInt, getShop
import random


async def sell(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        await message.channel.send(" make an account to sell stuff")
        return
    if len(args) == 2:
        await message.channel.send(" what are you selling lol")
        return

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
        await message.channel.send(" that does not exist.")
        return
    smallest = min(allPos, key=len)
    thing = objs[allPos.index(smallest)]
    item = thing[smallest]
    key = smallest
    if not str(item["sellcost"]).isnumeric():
        await message.channel.send(" You can't sell that item!")
        return
    if thing["name"] != "animals":
        if key not in db["members"][str(message.author.id)][thing["name"]]:
            await message.channel.send(" you don't have that")
            return
    else:
        has = False
        for i in db["members"][str(message.author.id)]["land"]["animals"]:
            print(db["members"][str(message.author.id)]["land"]["animals"][i])
            if (
                key
                in db["members"][str(message.author.id)]["land"]["animals"][i][
                    "animals"
                ]
            ):
                has = True
        if not has:
            await message.channel.send("you don't have that")

    if key in tools:
        thing = tools
    if len(args) == 3:
        amount = 1
    elif len(args) == 4 and args[3] in ["a", "all", "max"]:
        if thing["name"] == "animals":
            amount = 0
            for i in db["members"][str(message.author.id)]["land"]["animals"]:
                if (
                    key
                    in db["members"][str(message.author.id)]["land"]["animals"][i][
                        "animals"
                    ]
                ):
                    amount += db["members"][str(message.author.id)]["land"]["animals"][
                        i
                    ]["animals"][key]["amount"]
        if thing["name"] in ["seeds"]:
            amount = db["members"][str(message.author.id)][thing["name"]][key]["amount"]
        if thing["name"] in ["merch"]:
            amount = db["members"][str(message.author.id)]["merch"][key]
        if thing == tools:
            amount = 1
    elif len(args) == 4:
        amount = convertInt(args[3])
        if not bool(amount):
            amount = 1
    else:
        amount = 1
    if amount <= 0:
        await message.channel.send(
            "what are you doing, how are you supposed to sell negative things, go back to kindergarten u idiot"
        )
        return

    thingr = random.randint(1, 35)
    if thingr == 1:
        if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
            return
        things = ["rock", "tree", "rock", "stone"]
        thing2 = random.choice(things)
        await message.channel.send(
            f"On the way over to sell your thingies, you accidentally punched a hard {thing2} and died. you paid 100 coins to be reborn."
        )
        a = db["members"]
        if a[str(message.author.id)]["money"] < 100:
            a[str(message.author.id)]["money"] = 0
        else:
            a[str(message.author.id)]["money"] -= 100
        db["members"] = a
        return

    got = thing[key]["sellcost"]
    got *= amount
    got = round(got)

    a = db["members"]
    if thing["name"] in ["seeds"]:
        if amount > a[str(message.author.id)][thing["name"]][key]["amount"]:
            await message.channel.send(" you don't have that many")
            return
    if thing["name"] == ["animals"]:
        total = 0
        for i in a[str(message.author.id)]["land"]["animals"]:
            for j in a[str(message.author.id)]["land"]["animals"][i]["animals"]:
                total += a[str(message.author.id)]["land"]["animals"][i]["animals"][j][
                    "amount"
                ]
        if amount > total:
            return "you don't have that many"
    if thing["name"] == "merch":
        if amount > a[str(message.author.id)]["merch"][key]:
            await message.channel.send(" you don't have that many")
            return
    if thing["name"] == "tools":
        if key not in a[str(message.author.id)]["tools"]:
            await message.channel.send("you dont have that")
            return
        amount = 1
    if thing["name"] == "tools":
        amount = 1

    a[str(message.author.id)]["money"] += got
    if thing["name"] in ["merch"]:
        a[str(message.author.id)][thing["name"]][key] -= amount
        if a[str(message.author.id)][thing["name"]][key] == 0:
            del a[str(message.author.id)]["merch"][key]
    elif thing["name"] in ["seeds"]:
        a[str(message.author.id)][thing["name"]][key]["amount"] -= amount
        if a[str(message.author.id)][thing["name"]][key]["amount"] == 0:
            del a[str(message.author.id)][thing["name"]][key]
    elif thing["name"] == "animals":
        for i in a[str(message.author.id)]["land"]["animals"]:
            if key in a[str(message.author.id)]["land"]["animals"][i]["animals"]:
                a[str(message.author.id)]["land"]["animals"][i]["animals"][key][
                    "amount"
                ] -= amount
                if (
                    a[str(message.author.id)]["land"]["animals"][i]["animals"][key][
                        "amount"
                    ]
                    == 0
                ):
                    del a[str(message.author.id)]["land"]["animals"][i]["animals"][key]
    else:
        del a[str(message.author.id)][thing["name"]][key]
    a[str(message.author.id)]["amounts"]["sold"] += amount
    db["members"] = a

    repgain = random.randint(1, 4)
    repmsg = ""
    if repgain == 1:
        rep = db["members"][str(message.author.id)]["reputation"]
        gain = random.randint(1, 3)
        rep = gain
        repmsg = f"market: thanks for selling that thing, i really wanted it\n**reputation +{gain}**"
        db["members"][str(message.author.id)]["reputation"] = rep

    money = db["members"][str(message.author.id)]["money"]
    tts = [
        f"You sold `{amount} {key}(s)` for `{got} coins`. you now have `{money} coins`",
        f"`{amount} {key}(s)` sold successfully.",
        f"yessir you got `{got} coins`, now you have `{money}` total",
        f"selling success, you gained `{got} coins`",
        f"here's ur money, you sold `{amount} {key}(s)`",
        f"ty for selling some of ur `{key}(s)`",
        f"{message.author.mention} sold `{amount} {key}(s)` for `{got} coins`",
        f"{message.author.name} got `{got} coins` from selling some of their `{key}(s)`",
    ]
    ts = random.choice(tts)
    await message.reply(f"{ts}\n{repmsg}")
