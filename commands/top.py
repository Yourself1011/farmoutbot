from replit import db
import discord


async def top(message, client):
    members = [
        [i.id, f"{i.name}#{i.discriminator}"]
        for i in message.guild.members
        if str(i.id) in db["members"]
    ]
    balances = [[i[0], i[1], db["members"][str(i[0])]["money"]] for i in members]

    sort = sorted(balances, key=lambda x: x[2], reverse=True)

    page = (
        1
        if len(message.content.split(" ")) == 2
        or not message.content.split(" ")[2].isnumeric()
        else int(message.content.split(" ")[2])
    )

    display = sort[(page - 1) * 10 : (page) * 10]

    thing = "\n".join(
        [f"{sort.index(i) + 1}. <@{i[0]}> ({i[1]}) - {i[2]}" for i in display]
    )

    embed = discord.Embed(
        title=f"Richest users in {message.guild.name}",
        description=f"You are #{[i[0] for i in sort].index(message.author.id) + 1 if str(message.author.id) in db['members'] else '-1 since you do not have an account'}\n\n{thing}",
    )

    await message.channel.send(embed=embed)
