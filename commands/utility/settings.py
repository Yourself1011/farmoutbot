import discord
from replit import db
from zstats import softSearch


async def settings(message, client):
    args = message.content.split(" ")
    if str(message.author.id) not in db['members']:
      return 'do `i start` first, make a farm to have settings'

    boolean = ["true", "false", "yes", "no", "y", "n", "enable", "disable", "on", "off"]

    settings = {
        "votedm": {
            "name": "Vote Dms",
            "desc": "Enable or disable dms when you can vote again",
            "options": boolean,
        },
        "tips": {
            "name": "Tips",
            "desc": "Enable or disable whether you get tips",
            "options": boolean,
        },
        "emojionlyinv": {
            "name": "Emoji Only Inventory",
            "desc": "Makes the inventory only show emojis for animals and merch. Auto detects if youre on mobile and sets it off",
            "options": boolean + ["auto"],
        },
        "replypings": {
            "name": "Reply pings",
            "desc": "Enable or disable whether you get pings on replies",
            "options": boolean,
        },
    }

    if len(args) == 2 or (len(args) >= 3 and args[2].isnumeric()):
        page = args[2] - 1 if len(args) >= 3 else 0
        embed = discord.Embed(
            title="Settings",
        )
        ids = list(settings.keys())[page * 5 : page * 5 + 5]
        values = list(settings.values())[page * 5 : page * 5 + 5]

        for i in range(len(ids)):
            currentValue = db["members"][str(message.author.id)]["settings"][ids[i]]

            embed.add_field(
                name=values[i]["name"],
                value=f"`{ids[i]}`\n- Description: {values[i]['desc']}\n- Options: {', '.join(values[i]['options'])}\n- Currently: {currentValue}",
            )

        return await message.channel.send(embed=embed)

    if len(args) >= 3:
        search = softSearch(settings.keys(), args[2])

        if not bool(search):
            return await message.channel.send("That's not a setting")

        setting = settings[search]
        currentValue = db["members"][str(message.author.id)]["settings"][search]

        if len(args) == 3:
            embed = discord.Embed(
                title=setting["name"],
                description=f"`{search}`\nDescription: {setting['desc']}\nOptions: {', '.join(setting['options'])}\nCurrently: {currentValue}",
            )
            return await message.channel.send(embed=embed)

        elif len(args) > 3:
            option = args[3]

            if option not in setting["options"]:
                return await message.channel.send("That's not an option")

            if setting["options"] == boolean:
                if option in ["true", "yes", "y", "enable", "on"]:
                    option = True

                elif option in ["false", "no", "n", "disable", "off"]:
                    option = False

            if option == currentValue:
                return await message.channel.send(
                    f"{setting['name']} is already set to {option}"
                )

            a = db["members"]

            a[str(message.author.id)]["settings"][search] = option

            db["members"] = a

            return await message.channel.send(
                f"{setting['name']} has been set to {option}!"
            )
