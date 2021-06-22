import discord
from replit import db
from zstats import animals, tools, merch, seeds, getMember


async def profile(message, client):
    args = message.content.split(" ")
    if len(args) == 2 and str(message.author.id) not in db["members"]:
        prefix = db["server"][str(message.guild.id)]["prefix"]
        await message.channel.send(f"Do `{prefix} start` to get a profile dummy")
        return

    userObj = getMember(args[2:], message.guild.id, client)
    user = str(userObj.id) if userObj else False

    if len(args) == 2 or not user:
        user = str(message.author.id)
        userObj = message.author

    if user not in db["members"]:
        await message.channel.send("thats not a user with an account!")
        return

    name = userObj.name
    e = discord.Embed(title=f"", colour=discord.Colour.gold())
    e.set_author(name=f"{name}'s inventory:", icon_url=userObj.avatar_url)

    totalworth = 0
    money = db["members"][user]["money"]
    for i in db["members"][user]["animals"]:
        if type(animals[i]["cost"]) == int:
            totalworth += animals[i]["cost"]
    for i in db["members"][user]["tools"]:
        if type(tools[i]["cost"]) == int:
            totalworth += tools[i]["cost"]
    for i in db["members"][user]["merch"]:
        if type(merch[i]["cost"]) == int:
            totalworth += merch[i]["cost"]
    for i in db["members"][user]["seeds"]:
        if type(seeds[i]["cost"]) == int:
            totalworth += seeds[i]["cost"]
    totalworth += money

    reputation = db["members"][user]["reputation"]
    e.add_field(
        name="- :moneybag: Currency:",
        value=f"coins: {money}\ntotal worth: {totalworth}\nreputation: {reputation}",
        inline=False,
    )

    totalanimals = 0
    for i in db["members"][user]["animals"]:
        totalanimals += db["members"][user]["animals"][i]["amount"]

    totaltools = 0
    for i in db["members"][user]["tools"]:
        totaltools += 1

    totalmerch = 0
    for i in db["members"][user]["merch"]:
        totalmerch += db["members"][user]["merch"][i]

    totalseeds = 0
    for i in db["members"][user]["seeds"]:
        totalseeds += db["members"][user]["seeds"][i]["amount"]

    e.add_field(
        name="- :1234: Totals:",
        value=f"animals: {totalanimals}\ntools: {totaltools}\nmerch: {totalmerch}",
        inline=False,
    )

    shared = db["members"][user]["amounts"]["shared"]
    gambled = db["members"][user]["amounts"]["gambled"]
    bought = db["members"][user]["amounts"]["bought"]
    sold = db["members"][user]["amounts"]["sold"]
    used = db["members"][user]["amounts"]["used"]
    commands = db["members"][user]["commandsused"]

    e.add_field(
        name="- :bar_chart: Other:",
        value=f"shared: {shared}\ngambled: {gambled}\nbought: {bought}\nsold: {sold}\nanimals used: {used}\ncommands used: {commands}",
        inline=False,
    )

    datemade = db["members"][str(message.author.id)]["datemade"]
    e.set_footer(text=f"Date made: {datemade}")

    await message.channel.send(embed=e)
