from zstats import getMember
from replit import db


async def blacklist(message, client):

    if message.author.id not in [690577156006477875, 690575294674894879]:
        return "n o"

    args = message.content.split(" ")
    if len(args) == 2:
        return 'which subcommand "dev"'

    if args[2].lower() == "add":
        if len(args) == 3:
            return "suggest, report, or use"

        if args[3].lower() in ["suggest", "report", "use"]:
            if len(args) == 4:
                return "what"

        user = await getMember(args[4], message.guild.id, client)
        user = str(user.id) if user else False

        if not user:
            return "thats not a person"

        a = db["blacklist"]
        a[args[3].lower()].append(user)
        db["blacklist"] = a

        user = await client.fetch_user(user)

        return await message.reply(
            f"{user.name} was added to {args[3].lower()} blacklist"
        )

    if args[2].lower() == "remove":
        if len(args) == 3:
            return "suggest, report, or use"

        if args[3].lower() in ["suggest", "report", "use"]:
            if len(args) == 4:
                return "what"

        user = getMember(args[4], message.guild.id, client)
        user = str(user.id) if user else False

        if not user or not user in db["blacklist"][args[3].lower()]:
            return "thats not a person that's blacklisted"

        a = db["blacklist"]
        a[args[3].lower()].remove(user)
        db["blacklist"] = a

        user = await client.fetch_user(user)

        return await message.reply(
            f"{user.name} was removed from {args[3].lower()} blacklist"
        )
