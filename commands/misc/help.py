import discord
from replit import db
from acommands import commands
from zstats import choosecolour
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


async def help(message, client):
    prefix = db["server"][str(message.guild.id)]["prefix"]
    rmsg = ""
    if str(message.author.id) not in db["members"]:
        rmsg = "new to farmout? here's a couple things you can do:\n\n- `i start` to start your farming journey and get some tips\n- `i guide` gives help about some aspects of the bot"
    args = message.content.split(" ")
    if len(args) == 2:
        e = discord.Embed(title="", colour=choosecolour())
        prefix = db["server"][str(message.guild.id)]["prefix"]

        embed = {
            "misc": [],
            "game": [],
            "other": [],
            "market": [],
            "farming": [],
            "profile": [],
            "utility": [],
            "gamble": [],
            "gather": [],
        }

        for i in commands:
            category = commands[i]["category"]
            embed[category].append(commands[i]["name"])

        r = ", "
        for i in embed:
            embed[i] = r.join(embed[i])

        e.add_field(
            name="- :farmer:  Miscellaneous Commands:",
            value=embed["misc"],
            inline=False,
        )
        e.add_field(
            name="- :1234:  Profile Commands: ", value=embed["profile"], inline=False
        )
        e.add_field(
            name="- :video_game:  Game Commands:", value=embed["game"], inline=False
        )
        e.add_field(
            name="- :shopping_cart:   Market Commands: ",
            value=embed["market"],
            inline=False,
        )
        e.add_field(
            name="- :ear_of_rice:  Farming Commands: ",
            value=embed["farming"],
            inline=False,
        )
        e.add_field(
            name="- :mag_right: Gather Commands: ", value=embed["gather"], inline=False
        )
        e.add_field(
            name="- :game_die:  Gamble Commands:", value=embed["gamble"], inline=False
        )
        e.add_field(
            name="- :tools:  Utility Commands: ", value=embed["utility"], inline=False
        )
        e.add_field(
            name="- :dash:  Other Commands: ", value=embed["other"], inline=False
        )
        prefix = db["server"][str(message.guild.id)]["prefix"]
        e.set_footer(
            text=f"Use <{prefix} help (command)> to get help about a specific command\nUse <{prefix} help (category)> to get help about a category\nUse <{prefix} guide> to get help about playing the bot or setting up the bot\nUse <{prefix} about> to see some info about the bot"
        )
        e.set_author(name="Commands:", icon_url=message.author.avatar_url)
        await message.channel.send(
            rmsg,
            embed=e,
            components=[
                Button(
                    style=ButtonStyle.URL,
                    label="Support Server",
                    url="https://discord.gg/TX57HyWpsk",
                ),
            ],
        )

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
                return "Miscellaneous commands are the main commands that don't relate to the currency/game aspect of the bot. Here, you may find commands like help, ping, and vote."

            elif args[2].lower() in ["game", "gaming"]:
                return "Gaming commands are commands that relate to currency. These are commands that help you get money. Share and gift are for trading items and coins with other people. Here, you'll find commands like daily, lottery, and location."

            elif args[2].lower() in ["profilecmd", "pfc"]:
                return "Profile commands help you see info about your farm. For example, you can see your belongings with inventory, your coins with balance, and your statistics with profile."

            elif args[2].lower() in ["farming", "farm"]:
                return "Farming commands relate to the farming aspect of farmout. You plant seeds and trees, collect them, and sell them at the market."

            elif args[2].lower() in ["utility", "util"]:
                return "Utility commands are commands that relate to bot settings, like changing the prefix, reporting bugs, and dming you when you vote."

            elif args[2].lower() in ["gamblecmd", "gmb"]:
                return "Gamble commands are commands that you use to gamble your coins."

            elif args[2].lower() in ["market", "mr"]:
                return "Market commands are commands that you use to interact with the market, like shop, buy, sell, and trade. Buy and sell are for buying and selling items. Trade is for trading your items with the market. "

            elif args[2].lower() == "gather":
                return "Gather commands are commands that you can use to get items or coins. Be careful though, because there might be same dangerous things in some areas."

            elif args[2].lower() in ["other"]:
                return "Other commands are commands that don't really relate to farmout, but we have them anyway."

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
