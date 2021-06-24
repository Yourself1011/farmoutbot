import discord
from time import time
from math import floor

start = time()

async def stats(message, client):
    uptime = floor(time() - start)

    min, sec = divmod(uptime, 60)
    hour, min = divmod(min, 60)
    day, hour = divmod(hour, 24)

    return discord.Embed(
        title = "Bot stats",
        colour = discord.Colour.gold(),
        description = f"""
**Ping**
{round(client.latency * 1000)}ms

**Uptime**
{day} days, {hour} hours, {min} minutes, {sec} seconds

**Guilds**
{len(client.guilds)}

**Users**
{len(client.users)}
        """
    )
