import random
from replit import db
import discord


async def beetlerace(message, client):
    return
    if str(message.author.id) not in db["members"]:
        await message.channel.send("you dont exist yet my guy")
        return
    args = message.content.split(" ")
    if len(args) == 2:
        await message.channel.send(
            "please specify which beetle you are racing, and how much you bet for him to win"
        )
        return
    if not args[2].isnumeric() or not args[3].isnumeric():
        await message.channel.send(
            "ur dumb both the beetle number and the amount bet have to be integers greater than 0"
        )
        return
    if int(args[2]) > 5 or int(args[2]) < 0:
        await message.channel.send(f"there is no {args[2]} beetle, only 1-5")
        return
    if int(args[3]) < 0:
        await message.channel.send("gotta bet more than 0")
        return
    betted = int(args[3])
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    b5 = 0
    beetles = [b1, b2, b3, b4, b5]
    while b1 < 25 and b2 < 25 and b3 < 25 and b4 < 25 and b5 < 25:
        for i in beetles:
            randomn = random.randint(1, 3)
            i += randomn
            if i >= 25:
                break
        if b1 >= 25 or b2 >= 25 or b3 >= 25 or b4 >= 25 or b5 >= 25:
            break
    if args[2] == "1":
        beetle = b1
    if args[2] == "2":
        beetle = b2
    if args[2] == "3":
        beetle = b3
    if args[2] == "4":
        beetle = b4
    if args[2] == "5":
        beetle = b5
    for i in beetles:
        if i >= 25:
            beetlewon = i
    beetles = sorted(beetles)
    e = discord.Embed(title="", colour=discord.Colour.gold())
    e.set_author(
        name=f"{message.author.name}'s beetle race:", icon_url=message.author.avatar_url
    )
    for i in beetles:
        if i == beetle:
            beetles[i] = f"YOUR BEETLE: {beetle}"
        beetles[i] = f"{beetles[i]} :beetle:"
    e.add_field(
        name="Beetles",
        value=f"1st: {beetles[0]}\n2nd: {beetles[1]}\n3rd: {beetles[2]}\n4th: {beetles[3]}\n5th: {beetles[4]}",
    )
    if beetle == beetles[0]:
        a = db["members"]
        a[str(message.author.id)]["money"] += betted * 2
        db["members"] = a
        thing = f"your beetle got 1st, you won {betted*3} coins"
    elif beetle == beetles[1]:
        a = db["members"]
        a[str(message.author.id)]["money"] += betted
        db["members"] = a
        thing = f"your beetle got 2nd, you won {betted*2} coins"
    elif beetle == beetles[2]:
        thing = f"your beetle got 3rd, nothing happened"
    else:
        a = db["members"]
        a[str(message.author.id)]["money"] -= betted
        db["members"] = a
        thing = "your beetle got 4th or 5th, you lose your betted coins"
    e.set_footer(text="lmao beetles")
    await message.channel.send(embed=e, content=f"\n{thing}")
