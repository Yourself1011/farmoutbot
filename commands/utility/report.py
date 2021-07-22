async def report(message, client):
    args = message.content.split(" ")
    if client.user.name == 'Farmout beta':
      return 'go do that on the main bot u meganerd'
    if len(args) == 2:
        await message.reply(
            "When reporting bugs, have a detailed description or send an image link."
        )
        return
    args.pop(0)
    args.pop(0)
    args = " ".join(args)
    channel = client.get_channel(806178919409254450)
    name = await client.fetch_user(message.author.id)
    me = await client.fetch_user(690577156006477875)
    await me.send(f'oy {name} reported a bug from {message.guild.name}:\n{args}')
    await channel.send(f"{name} has reported a bug: \n**[Farmout]** {args}")
    await message.add_reaction("✅")
