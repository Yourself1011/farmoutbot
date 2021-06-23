import discord
from replit import db
from acommands import commands


async def help(message, client):
    prefix = db["server"][str(message.guild.id)]["prefix"]
    args = message.content.split(" ")
    if len(args) == 2:
        e = discord.Embed(title="", colour=discord.Colour.orange())
        prefix = db["server"][str(message.guild.id)]["prefix"]

        misc = []
        game = []
        other = []
        market = []
        farming = []
        profile = []
        utility = []
        gamble = []
        gather = []
        for i in commands:
            if commands[i]["category"] == "misc":
                misc.append(commands[i]["name"])
            if commands[i]["category"] == "game":
                game.append(commands[i]["name"])
            if commands[i]["category"] == "other":
                other.append(commands[i]["name"])
            if commands[i]["category"] == "market":
                market.append(commands[i]["name"])
            if commands[i]["category"] == "farming":
                farming.append(commands[i]["name"])
            if commands[i]["category"] == "utility":
                utility.append(commands[i]["name"])
            if commands[i]["category"] == "gamble":
                gamble.append(commands[i]["name"])
            if commands[i]["category"] == "profile":
                profile.append(commands[i]["name"])
            if commands[i]["category"] == "gather":
                gather.append(commands[i]["name"])

        r = ", "
        misc = r.join(misc)
        game = r.join(game)
        other = r.join(other)
        market = r.join(market)
        farming = r.join(farming)
        profile = r.join(profile)
        utility = r.join(utility)
        gamble = r.join(gamble)
        gather = r.join(gather)
        e.add_field(
            name="- :farmer:  Miscellaneous Commands:", value=misc, inline=False
        )
        e.add_field(name="- :1234:  Profile Commands: ", value=profile, inline=False)
        e.add_field(name="- :video_game:  Game Commands:", value=game, inline=False)
        e.add_field(
            name="- :shopping_cart:   Market Commands: ", value=market, inline=False
        )
        e.add_field(
            name="- :ear_of_rice:  Farming Commands: ", value=farming, inline=False
        )
        e.add_field(name="- :mag_right: Gather Commands: ", value=gather, inline=False)
        e.add_field(name="- :game_die:  Gamble Commands:", value=gamble, inline=False)
        e.add_field(name="- :tools:  Utility Commands: ", value=utility, inline=False)
        e.add_field(name="- :dash:  Other Commands: ", value=other, inline=False)
        prefix = db["server"][str(message.guild.id)]["prefix"]
        e.set_footer(
            text=f"Use <{prefix} help (command)> to get help about a specific command"
        )
        e.set_author(name="Commands:", icon_url=message.author.avatar_url)
        await message.channel.send(embed=e)

    if len(args) > 2:
        if args[2] not in commands:
            await message.channel.send("thats not a command dummy")
            return
        description = commands[args[2]]["description"]
        usage = commands[args[2]]["usage"]
        if commands[args[2]]["aliases"] == []:
            aliases = None
        else:
            aliases = ", ".join(commands[args[2]]["aliases"])
        sfasd = commands[args[2]]["name"]
        e = discord.Embed(
            title=sfasd,
            colour=discord.Colour.gold(),
            description=f"**Usage:** `{usage}`\n**Description:** {description}\n**Aliases:** {aliases}",
        )
        e.set_footer(text="Use <" + prefix + " help> to see all commands.")
        await message.channel.send(embed=e)
