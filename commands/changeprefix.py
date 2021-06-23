from replit import db


async def changeprefix(message, client):
    args = message.content.split(" ")
    if len(args) == 2:
        await message.channel.send(
            "gotta specify a new prefix dummo, make sure it has no space"
        )
    elif not message.author.guild_permissions.manage_guild:
        await message.channel.send("no no no, gotta have `Manage Server` for that")
    else:
        oldprefix = db["server"][str(message.guild.id)]["prefix"]
        a = db["server"]
        a[str(message.guild.id)]["prefix"] = args[2]
        db["server"] = a

        newprefix = args[2]
        name = message.guild.name
        await message.channel.send(
            f":white_check_mark: the prefix for `{name}` has been changed from `{oldprefix}` to `{newprefix}` by {message.author.mention}."
        )
