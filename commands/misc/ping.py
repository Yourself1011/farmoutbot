async def ping(message, client):
    await message.channel.send(
        f"get pinged {message.author.mention}\nalso the ping is `{round(client.latency*1000)} milliseconds` if you were wondering"
    )
