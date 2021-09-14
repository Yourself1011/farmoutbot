import discord
from time import time
from math import floor
from replit import db

start = time()


async def stats(message, client):
    uptime = floor(time() - start)

    min, sec = divmod(uptime, 60)
    hour, min = divmod(min, 60)
    day, hour = divmod(hour, 24)

    e = discord.Embed(
        title="",
        colour=discord.Colour.gold(),
        description=f"""
**Ping**
{round(client.latency * 1000)}ms

**Uptime**
{day} days, {hour} hours, {min} minutes, {sec} seconds

**Servers**
{len(client.guilds)}	

**Users**
{len(client.users)}

**Players**
{len(db["members"])}
        """,
    )
    e.set_author(name="Stats", icon_url=client.user.avatar_url)
    return e
