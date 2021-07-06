from replit import db
import discord
from zstats import pages

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
        else max(1, min(len(balances, int(message.content.split(" ")[2]))))
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
        description=f"You are #{placement}\n\n",
        colour=discord.Colour.red(),
    )

    await pages(message, client, list(map(lambda x: f"<@{x[0]}> ({x[1]}) - {x[2]}", balances)), 10, startPage = page, baseEmbed = embed, newField = False)