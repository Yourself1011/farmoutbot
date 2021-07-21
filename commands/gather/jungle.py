from replit import db
from time import time
from math import floor
from random import randint
import random
from zstats import gatheringCmd, merch, tools, seeds, animals


async def jungle(message, client):
    user = str(message.author.id)
    if user not in db["members"]:
        await message.channel.send("make an account to search the jungle")
        return
    user = db["members"][str(message.author.id)]
    if "gather" in user["cooldowns"] and user["cooldowns"]["gather"] > time():
        await message.channel.send(
            f"you already gathered stuff, wait {floor(user['cooldowns']['gather'] - time())}s"
        )
        return

    if "shoes" not in user["tools"]:
        await message.channel.send("buy shoes first")
        return

    thing = random.randint(1, 40)
    if thing == 1:
        if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
            return
        things = ["bug", "fish", "tree", "plant", "elephant", "neighbour"]
        thing2 = random.choice(things)
        await message.channel.send(
            f"On the way over to the jungle, you accidentally smelled a really smelly {thing2} and died. you paid 100 coins to be reborn."
        )
        a = db["members"]
        if a[str(message.author.id)]["money"] < 100:
            a[str(message.author.id)]["money"] = 0
        else:
            a[str(message.author.id)]["money"] -= 100
        db["members"] = a
        return

    item = gatheringCmd(
        message,
        {
            "death": [40, 1, 1, 1],
            "mango": [40, 3, 1, 3],
            "coconut": [25, 4, 1, 3],
            "sunflower": [30, 5, 1, 1],
            "undeadwool": [1, 1, 1, 1],
            "nothing": [50, 1, 1, 1],
        },
    )

    m = db["members"]
    user = m[str(message.author.id)]
    if item[0] != "death":
        if item[0] in merch:
            if item[0] in user["merch"]:
                user["merch"][item[0]] += item[1]

            else:
                user["merch"][item[0]] = item[1]
            itemName = merch[item[0]]["name"]

        elif item[0] in seeds:
            if item[0] in user["seeds"]:
                user["seeds"][item[0]]["amount"] += item[1]

            else:
                user["seeds"][item[0]]["amount"] = item[1]
            itemName = seeds[item[0]]["name"]

    breakAmt = randint(3, 6)

    user["tools"]["shoes"] -= breakAmt

    if user["tools"]["shoes"] <= 0:
        del user["tools"]["shoes"]
        durabilityMsg = "Your shoes broke!"
    else:
        durabilityMsg = f"Your shoes lost {breakAmt} durability! They are now at {user['tools']['shoes']} durability."

    reserveMsg = ""
    if not bool(randint(0, 7)):
        fine = randint(floor(user["money"] / 10), floor(user["money"] / 4))

        user["money"] -= fine
        reserveMsg = f"When you got to the jungle, you saw a tourist who was highly trained in the art of the monkey. He didn't like the look on your face, so he punched you 150 million kilometres into the sun. At the same time, a large bottle of sunscreen shot out of your pocket and onto the sun, causing it to black out. You died of hyporthermia. You paid {fine} to be reborn."

    user["cooldowns"]["gather"] = time() + 60

    db["members"] = m

    if item[0] == "undeadwool":
        await message.channel.send(
            f"You wandered in the jungle, and there, behind a large bush, you saw it. The mystical undeadwool. Legend says that it was made eons ago, by the same people who made the sky and the sea.\n{durabilityMsg}\n{reserveMsg}"
        )

    elif item[0] == "nothing":
        things = [
            "except for a whole lot of sweaty tourists",
            "so maybe you should go search the beach instead",
            "because you got lost and fell in a hole",
            "except for a large gang of chimps",
        ]
        thing = random.choice(things)
        await message.channel.send(
            f"You found nothing in the jungle, {thing}\n{durabilityMsg}\n{reserveMsg}"
        )

    elif item[0] == "death":
        if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
            return
        await message.channel.send(
            "You were searching the jungle and came across a battle of babbons and baboons. When you started to watch their skillful dance in awe, one of the baboons noticed you. The battle instantly ceased. United against their common enemy, the babbons and baboons chased you out of their jungle.\n\nWhen you finally escaped, you got trampled by an elephant. You paid 100 coins to be reborn."
        )
        a = db["members"]
        if a[str(message.author.id)]["money"] < 100:
            a[str(message.author.id)]["money"] = 0
        else:
            a[str(message.author.id)]["money"] -= 100
        db["members"] = a
        return

    else:
        responses = [
            "looked on the jungle and found",
            "hiked around a bit and picked up",
            "discovered",
            "found",
            "looked atop a hilly hill and found",
        ]
        await message.channel.send(
            f"You {responses[randint(0, len(responses)-1)]} {item[1]}x {itemName}\n{durabilityMsg}\n{reserveMsg}"
        )
