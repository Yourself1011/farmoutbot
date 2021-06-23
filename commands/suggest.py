async def suggest(message, client):
    args = message.content.split(" ")
    if len(args) == 2:
        await message.channel.send("what are you suggesting lol")
        return

    args.pop(0)  # gets rid of prefix
    args.pop(0)  # gets rid of "suggest"
    args = " ".join(args)

    channel = client.get_channel(806165117049503775)
    name = await client.fetch_user(message.author.id)
    msg = await channel.send(f"{name} made a suggestion: \n**[Farmout]** {args}")
    await msg.add_reaction("⬆️")
    await msg.add_reaction("⬇️")
    await message.add_reaction("✅")
