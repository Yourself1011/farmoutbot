from replit import db


async def changeprefix(message, client):
    args = message.content.split(" ")
    if len(args) == 2:
        return "gotta specify a new prefix dummo, make sure it has no space"
    elif not message.author.guild_permissions.manage_guild:
        return "no no no, gotta have `Manage Server` for that"
    else:
        oldprefix = db["server"][str(message.guild.id)]["prefix"]
        a = db["server"]
        a[str(message.guild.id)]["prefix"] = args[2]
        db["server"] = a

        newprefix = args[2]
        name = message.guild.name
        return f":white_check_mark: the prefix for `{name}` has been changed from `{oldprefix}` to `{newprefix}` by {message.author.mention}."
