import discord
import random
from replit import db


async def suggest(message, client):

    if message.author.id in db["blacklist"]["suggest"]:
        return "you've been blacklisted omegaLUL"
    args = message.content.split(" ")
    if client.user.name == "Farmout beta":
        return "go do that on the main bot u meganerd"
    if len(args) == 2:
        await message.channel.send("what are you suggesting lol")
        return

    args.pop(0)  # gets rid of prefix
    args.pop(0)  # gets rid of "suggest"
    args = " ".join(args)

    channel = client.get_channel(806165117049503775)
    name = await client.fetch_user(message.author.id)
    colours = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold()]
    color = random.choice(colours)
    me = await client.fetch_user(690577156006477875)
    await me.send(f"{name} has a suggestion in {message.guild.name}:\n{args}")
    e = discord.Embed(title=f"", colour=color, description=args)
    e.set_author(name=f"{name}'s suggestion:", icon_url=message.author.avatar_url)
    msg = await channel.send(embed=e)
    await msg.add_reaction("⬆️")
    await msg.add_reaction("⬇️")
    await message.add_reaction("✅")
