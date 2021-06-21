from replit import db
import discord


async def top(message: discord.Message, client):
    dbMembers = db["members"]

    def userInDb(user: discord.Member) -> bool:
        return str(user.id) in dbMembers

    members = map(
        lambda i: (i.id, f"{i.name}#{i.discriminator}"),
        filter(userInDb, message.guild.members),
    )

    balances = [(i[0], i[1], dbMembers[str(i[0])]["money"]) for i in members]

    balances.sort(key=lambda x: x[2], reverse=True)

    page = (
        1
        if len(message.content.split(" ")) == 2
        or not message.content.split(" ")[2].isnumeric()
        else int(message.content.split(" ")[2])
    )

    display = balances[(page - 1) * 10 : (page) * 10]

    thing = "\n".join(
        map(lambda i: f"{balances.index(i) + 1}. <@{i[0]}> ({i[1]}) - {i[2]}", display)
    )

    placement = (
        next(
            filter(
                lambda info: message.author.id == info[1],
                map(lambda info: (info[0], info[1][0]), enumerate(balances)),
            )
        )[0]
        + 1
        if str(message.author.id) in dbMembers
        else "-1 since you do not have an account"
    )

    embed = discord.Embed(
        title=f"Richest users in {message.guild.name}",
        description=f"You are #{placement}\n\n{thing}",
        colour=discord.Colour.red(),
    )

    await message.channel.send(embed=embed)
