from replit import db
from time import time
from math import floor
from random import randint
import random
from zstats import gatheringCmd, merch, tools, seeds, animals


async def arctic(message, client):

    user = str(message.author.id)
    if user not in db["members"]:
        responses = [
            "make an account to scour the arctic",
            "gotta exist before exploring the arctic we don't do that here",
        ]
        return random.choice(responses)

    user = db["members"][str(message.author.id)]
    if "gather" in user["cooldowns"] and user["cooldowns"]["gather"] > time():
        return f"you already gathered stuff, wait {floor(user['cooldowns']['gather'] - time())}s"

    if "wintercoat" not in user["tools"]:
        return "buy a winter coat first or you'll freeze to death"

    thing = random.randint(1, 35)
    if thing == 1:
        if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
            return
        things = ["bug", "fish", "tree", "plant", "elephant", "neighbour"]
        thing2 = random.choice(things)
        return f"On the way into the arctic, you accidentally saw a really strange {thing2} and died. you paid 100 coins to be reborn."
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
            "death": [30, 1, 1, 1],
            "snowball": [10, 9, 5, 3],
            "ice": [20, 5, 1, 1],
            "gamingpc": [3, 2, 1, 10],
            "nothing": [30, 1, 1, 1],
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

    user["tools"]["wintercoat"] -= breakAmt

    if user["tools"]["wintercoat"] <= 0:
        del user["tools"]["wintercoat"]
        durabilityMsg = "Your wintercoat broke when you wore it somehow idek lol"
    else:
        durabilityMsg = f"Your wintercoat lost {breakAmt} durability! They are now at {user['tools']['wintercoat']} durability."

    reserveMsg = ""
    if not bool(randint(0, 7)):
        fine = randint(floor(user["money"] / 10), floor(user["money"] / 4))

        user["money"] -= fine
        lesréponses = [
            f"You met a polarbear and taunted it with maracas for some reason. It pushed you onto a floating ice cube, which drifted for a week and took you to a volcano. You fell in and died, and had to pay {fine} to be reborn. \n\nno polarbears were harmed",
            f"you searched the arctic for a while, and found nothing. when you turned to leave, you tripped over the outhouse that everyone was sharing and fell into a frozen lake. you paid {fine} to be rescued",
            f"you got impaled on a dead walrus\nyou paid {fine} to be reborn",
        ]
        reserveMsg = random.choice(lesréponses)

    user["cooldowns"]["gather"] = time() + 60

    db["members"] = m

    if item[0] == "gamingpc":
        return f"You dug some ~~dirt~~ snow in the arctic. After a few long, cold hours, and battling a couple wolves and a polar bear, you finally found it. Hidden behind a prehistoric snowman, there were {item[1]} gaming pc(s).\n{durabilityMsg}\n{reserveMsg}"

    elif item[0] == "nothing":
        responses = [
            "You didn't find anything in the arctic, not even snow",
            "you found absolutely nothing in the arctic",
        ]
        return f"{random.choice(responses)}\n{durabilityMsg}\n{reserveMsg}"

    elif item[0] == "death":
        if "undeadwool" in db["members"][message.author.id]["merch"]:
            return
        return "You had just entered the arctic and was about to start digging for treasure when you slipped on some slippery ice and died."
        m = db["members"]
        m[str(message.author.id)]["money"] -= 100
        db["members"] = m

    else:
        responses = [
            "looked around a bit and found",
            "walked around a little and picked up",
            "discovered",
            "found",
            "looked in a polar bear's den and found",
            "brushed a walrus's teeth and discovered",
            "sacrificed your pants and conjured",
        ]
        return f"You {responses[randint(0, len(responses)-1)]} {item[1]}x {itemName}\n{durabilityMsg}\n{reserveMsg}"
