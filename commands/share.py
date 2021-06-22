import discord
from replit import db
from zstats import convertInt, getMember


async def share(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        await message.channel.send("u don't exist")
        return
    if len(args) == 2:
        await message.channel.send("who and how much")
        return
    if len(args) == 3:
        await message.channel.send("who what")
        return

    userObj = getMember(args[3:], message.guild.id, client)
    person = str(userObj.id) if userObj else False

    amount = convertInt(args[2])
    if args[2] in ["a", "all", "max"]:
        amount = db["members"][str(message.author.id)]["money"]

    if not bool(amount):
        await message.channel.send("gotta say a number")
        return
    if amount <= 0:
        await message.channel.send("say a number more than 0")
        return

    if person not in db["members"]:
        await message.channel.send("that's not a user with an account!")
        return
    if not person:
        return await message.channel.send("That's not a user")
    if str(person) == str(message.author.id):
        await message.channel.send(
            "you tried to give coins to yourself, but you were too stupid and lost the coins in the process somehow kekw"
        )
        a = db["members"]
        a[str(message.author.id)]["money"] -= amount
        db["members"] = a
        return

    if amount > db["members"][str(message.author.id)]["money"]:
        await message.channel.send(
            "that's more money than you have, learn to count dummy"
        )
        return

    a = db["members"]
    a[str(message.author.id)]["money"] -= amount
    a[person]["money"] += amount
    a[str(message.author.id)]["amounts"]["shared"] += amount
    db["members"] = a

    person = await client.fetch_user(person)
    await message.channel.send(
        f"{message.author.mention} gave `{amount}` coins to {person.name}. "
    )
