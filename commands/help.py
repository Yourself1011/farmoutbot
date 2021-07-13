import discord
from replit import db
from acommands import commands
from zstats import choosecolour

async def help(message, client):
    prefix = db["server"][str(message.guild.id)]["prefix"]
    args = message.content.split(" ")
    if len(args) == 2:
        e = discord.Embed(title="", colour=choosecolour())
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
            text=f"Use <{prefix} help (command)> to get help about a specific command\nUse <{prefix} help (category)> to get help about a category\mUse <{prefix} guide> to get help about playing the bot or setting up the bot"
        )
        e.set_author(name="Commands:", icon_url=message.author.avatar_url)
        await message.channel.send(embed=e)

    if len(args) > 2:
        categories = [
            "misc",
            "game",
            "farming",
            "utility",
            "gamble",
            "other",
            "market",
            "profile",
        ]
        if args[2].lower() in categories:
            if args[2].lower() in ["misc", "miscellaneous"]:
                await message.reply(
                    "Miscellaneous commands are the main commands that don't relate to the currency/game aspect of the bot. Here, you may find commands like help, ping, and vote."
                )
            elif args[2].lower() in ["game", "gaming"]:
                await message.reply(
                    "Gaming commands are commands that relate to currency. These are commands that help you get money. Share and gift are for trading items and coins with other people. Here, you'll find commands like daily, lottery, and location."
                )
            elif args[2].lower() in ["profilecmd", "pfc"]:
                await message.reply(
                    "Profile commands help you see info about your farm. For example, you can see your belongings with inventory, your coins with balance, and your statistics with profile."
                )
            elif args[2].lower() in ["farming", "farm"]:
                await message.reply(
                    "Farming commands relate to the farming aspect of farmout. You plant seeds and trees, collect them, and sell them at the market."
                )
            elif args[2].lower() in ["utility", "util"]:
                await message.reply(
                    "Utility commands are commands that relate to bot settings, like changing the prefix, reporting bugs, and dming you when you vote."
                )
            elif args[2].lower() in ["gamblecmd", "gmb"]:
                await message.reply(
                    "Gamble commands are commands that you use to gamble your coins."
                )
            elif args[2].lower() in ["market", "mr"]:
                await message.reply(
                    "Market commands are commands that you use to interact with the market, like shop, buy, sell, and trade. Buy and sell are for buying and selling items. Trade is for trading your items with the market. "
                )
            elif args[2].lower() in ["other"]:
                await message.reply(
                    "Other commands are commands that don't really relate to farmout, but we have them anyway."
                )

        allcommands = {}

        for i in commands:
            allcommands[i] = i
            allcommands.update({aliases: i for aliases in commands[i]["aliases"]})

        if args[2] not in allcommands:
            await message.channel.send("thats not a command dummy")
            return

        command = commands[allcommands[args[2]]]
        description = command["description"]
        usage = command["usage"]
        if command["aliases"] == []:
            aliases = None
        else:
            aliases = ", ".join(command["aliases"])
        sfasd = command["name"]
        e = discord.Embed(
            title=sfasd,
            colour=discord.Colour.gold(),
            description=f"**Usage:** `{usage}`\n**Description:** {description}\n**Aliases:** {aliases}",
        )
        e.set_footer(text="Use <" + prefix + " help> to see all commands.")
        await message.channel.send(embed=e)
