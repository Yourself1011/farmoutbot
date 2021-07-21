from replit import db
from zstats import animals, tools, seeds, merch, convertInt, softSearch, getMember


async def gift(message, client):
    args = message.content.split(" ")
    if len(args) == 2:
        await message.channel.send("bruh")
        return
    if len(args) <= 4:
        await message.channel.send("`prefix gift person item amount` please")
        return

    userObj = getMember(args[2], message.guild.id, client)
    user = str(userObj.id) if userObj else False

    if not bool(user):
        return await message.channel.send("I couldn't find anybody")

    if str(user) not in db["members"]:
        await message.channel.send(
            f"Get {userObj.name}#{userObj.discriminator} to make an account"
        )
        return
    if str(message.author.id) not in db["members"]:
        await message.channel.send("make an account first u dumum")
        return
    if len(args) == 4:
        amount = 1
    if len(args) > 4:
        amount = args[4]
        if not amount.isnumeric() and not amount in ["a", "all", "max"]:
            amount = 1
        elif amount.isnumeric():
            amount = int(amount)
    if type(amount) is str or amount <= 0:
        await message.channel.send("whut")
        return

    thinggifted = softSearch(
        list(animals.keys())
        + list(tools.keys())
        + list(seeds.keys())
        + list(merch.keys()),
        args[3].lower(),
        ignore=["name"],
    )  # kekw hey i thought you were adding softSearch Me??? fine
    if not bool(thinggifted):
        await message.channel.send("thats not a thing idiot")
        return
    things = [animals, tools, seeds, merch]
    for i in things:
        if thinggifted in i:
            thing = i

    if thinggifted not in db["members"][str(message.author.id)][thing["name"]]:
        await message.channel.send("you don't own that, go buy it somewhere dumbo")
        return

    if amount in ["a", "all", "max"]:
        if thing == animals or thing == seeds:
            amount = db["members"][str(message.author.id)][thing["name"]][thinggifted][
                "amount"
            ]
        if thing == tools:
            amount = 1
        if thing == merch:
            amount = db["members"][str(message.author.id)][thing["name"]][thinggifted]

    if thing == animals:
        a = db["members"]
        if amount > a[str(message.author.id)]["animals"][thinggifted]["amount"]:
            await message.channel.send("you dont have that many lol :sheep:")
            return

        a[str(message.author.id)]["animals"][thinggifted]["amount"] -= amount
        if a[str(message.author.id)]["animals"][thinggifted]["amount"] == 0:
            del a[str(message.author.id)]["animals"][thinggifted]
        if thinggifted not in a[user]["animals"]:
            a[user]["animals"][thinggifted] = {"lastused": 0, "amount": amount}
        else:
            a[user]["animals"][thinggifted]["amount"] += amount
    if thing == tools:
        a = db["members"]
        a[user]["tools"][thinggifted] = a[str(message.author.id)]["tools"][thinggifted]
        del a[str(message.author.id)]["tools"][thinggifted]
        db["members"] = a
    if thing == merch:
        a = db["members"]
        if amount > a[str(message.author.id)]["merch"][thinggifted]:
            await message.channel.send("you dont have that many >(")
            return
        a[str(message.author.id)]["merch"][thinggifted] -= amount
        if a[str(message.author.id)]["merch"][thinggifted] == 0:
            del a[str(message.author.id)]["merch"][thinggifted]
        if thinggifted not in a[user]["merch"]:
            a[user]["merch"][thinggifted] = amount
        else:
            a[user]["merch"][thinggifted] += amount
        db["members"] = a
    if thing == seeds:
        a = db["members"]
        if amount > a[str(message.author.id)]["seeds"][thinggifted]["amount"]:
            await message.channel.send("you dont have that many >(")
            return
        a[str(message.author.id)]["seeds"][thinggifted]["amount"] -= amount
        if a[str(message.author.id)]["seeds"][thinggifted]["amount"] == 0:
            del a[str(message.author.id)]["seeds"][thinggifted]
        if thinggifted not in a[user]["seeds"]:
            a[user]["seeds"][thinggifted] = {"amount": amount}
        else:
            a[user]["seeds"][thinggifted]["amount"] += amount
        db["members"] = a
    name = await client.fetch_user(user)
    await message.channel.send(
        f"{message.author.mention} gave {name} `{amount} {thinggifted}(s)`."
    )
