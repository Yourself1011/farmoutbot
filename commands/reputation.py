from replit import db


async def reputation(message, client):
    rep = db["members"][str(message.author.id)]["reputation"]
    await message.channel.send(
        f"{message.author.name}'s reputation: `{rep}`\nMinimum reputation for daily and hourly: `250`\nMaximum reputation from donating: `1000`\n{message.author.mention}"
    )
