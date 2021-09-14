from replit import db
import discord
from zstats import animals, tools, merch, seeds, getMember, choosecolour
import time
from emoji import emojize


async def inventory(message, client):
    args = message.content.split(" ")

    if len(args) == 2 and str(message.author.id) not in db["members"]:
        await message.channel.send("Gotta make an account first dummy")
        return

    if len(args) >= 3 and args[2].lower() == "stats":
        userObj = getMember(args[3:], message.guild.id, client)
        user = str(userObj.id) if userObj else False

        if len(args) == 3 or not user:
            user = str(message.author.id)

        if user not in db["members"]:
            await message.channel.send(
                f"Ask {userObj.name}#{userObj.discriminator} to make an account first stupid"
            )
            return
        name = await client.fetch_user(user)
        e = discord.Embed(title=f"", colour=choosecolour())

        e.set_author(name=f"{name	}'s inventory stats:", icon_url=name.avatar_url)

        animaltotal = 0
        if db["members"][user]["land"]["animals"] != {}:
            for i in db["members"][user]["land"]["animals"]:
                if db["members"][user]["land"]["animals"][i]["total"] != 0:
                    for j in db["members"][user]["land"]["animals"][i]["animals"]:
                        animaltotal += db["members"][user]["land"]["animals"][i][
                            "animals"
                        ][j]["amount"]

        tooltotalunique = len(list(db["members"][user]["tools"].values()))
        merchtotalunique = len(list(db["members"][user]["merch"].values()))
        merchtotal = 0
        for i in db["members"][user]["merch"]:
            merchtotal += db["members"][user]["merch"][i]
        e.add_field(
            name="- :sheep: Animals ",
            value=f"Total: {animaltotal}",
            inline=False,
        )
        e.add_field(
            name="- :hammer: Tools ", value=f"Total: {tooltotalunique}", inline=False
        )
        e.add_field(
            name="- :moneybag: Merch ",
            value=f"Total: {merchtotal}\nUnique Total: {int(merchtotalunique)}",
        )
        prefix = db["server"][str(message.guild.id)]["prefix"]
        e.set_footer(text=f"<{prefix} inv> for more info")
        await message.channel.send(embed=e)
        return

    userObj = getMember(args[2:], message.guild.id, client)
    user = str(userObj.id) if userObj else False

    if len(args) == 2 or not user:
        user = str(message.author.id)

    if user not in db["members"]:
        await message.channel.send(
            f"Ask {userObj.name}#{userObj.discriminator} to make an account first stupid"
        )
        return

    name = await client.fetch_user(user)
    e = discord.Embed(title=f"", colour=choosecolour())
    e.set_author(name=f"{name}'s inventory:", icon_url=name.avatar_url)

    aout = f"Use `i pens` to see your animal pens"
    tout = []
    mout = []
    sout = []

    # if db["members"][user]["animals"] == {}:
    #     aout = None
    # else:
    #     for i in db["members"][user]["animals"]:
    #         c = db["members"][user]["animals"][i]["amount"]
    #         kare = animals[i]["name"]
    #         if (
    #             "emojionlyinv" in db["members"][user]["settings"]
    #             and db["members"][user]["settings"]["emojionlyinv"] == True
    #             or (db["members"][user]["settings"]["emojionlyinv"] == "auto" and not message.author.is_on_mobile())
    #         ):
    #             kare = kare.split(" ")
    #             hyperlinked = f"[{kare[1]}](https://youtu.be/dQw4w9WgXcQ \"{kare[0]}\")"
    #             kare = f"{kare[0]} {kare[1]}" if hyperlinked == emojize(hyperlinked, use_aliases=True) else emojize(hyperlinked, use_aliases=True)
    #         aout.append(f"{kare}: {c}")

    #     aout = "".join([f"{val}\n" if (index + 1) % 5 == 0 else f"{val}, " for index, val in enumerate(aout)],
    #     )

    if db["members"][user]["tools"] == {}:
        tout = None
    else:
        for i in db["members"][user]["tools"]:
            c = db["members"][user]["tools"][tools[i]["name"]]
            name = tools[i]["name"]
            dura = tools[i]["durability"]
            tout.append(f"{name}: {int(c)}/{dura}")

        tout = "".join(  # Join an array together
            [
                # If the index is a multiple of, add a newline
                f"{val}\n" if (index + 1) % 4 == 0 else f"{val}, "
                for index, val in enumerate(tout)  # For every element in arr
            ],
        )

    lengggg = 4
    mercha = db["members"][user]["merch"]
    if mercha == {}:
        mout = None
    else:
        for m in mercha:
            if (
                "emojionlyinv" in db["members"][user]["settings"]
                and db["members"][user]["settings"]["emojionlyinv"] == True
            ):
                kare = merch[m]["name"].split(" ")[1]
                lengggg = 9
            else:
                kare = merch[m]["name"]

            # if (
            #     "emojionlyinv" in db["members"][user]["settings"]
            #     and db["members"][user]["settings"]["emojionlyinv"] == True
            #     or (db["members"][user]["settings"]["emojionlyinv"] == "auto" and not message.author.is_on_mobile())
            # ):
            #     lengggg = 8
            #     kare = kare.split(" ")
            #     hyperlinked = f"[{kare[1]}](https://youtu.be/dQw4w9WgXcQ \"{kare[0]}\")"
            #     kare = f"{kare[0]} {kare[1]}" if hyperlinked == emojize(hyperlinked, use_aliases=True) else emojize(hyperlinked, use_aliases=True)
            mout.append(f"{kare}: {mercha[m]}")

        mout = "".join(  # Join an array together
            [
                # If the index is a multiple of, add a newline
                f"{val}\n" if (index + 1) % lengggg == 0 else f"{val}, "
                for index, val in enumerate(mout)  # For every element in arr
            ],
        )

    seed = db["members"][user]["seeds"]
    if seed == {}:
        sout = None
    else:
        for m in db["members"][user]["seeds"]:
            amount = str(db["members"][user]["seeds"][m]["amount"])
            sout.append(f"{seeds[m]['name']}: {amount}")

        sout = "".join(  # Join an array together
            [
                # If the index is a multiple of, add a newline
                f"{val}\n" if (index + 1) % 5 == 0 else f"{val}, "
                for index, val in enumerate(sout)  # For every element in arr
            ],
        )

    e.add_field(name="- :sheep: Animals: ", value=aout, inline=False)

    e.add_field(name="- :hammer: Tools: ", value=tout, inline=False)

    e.add_field(name="- :seedling: Seeds: ", value=sout, inline=False)

    e.add_field(
        name="- :herb: Plants: ",
        value="Use `i crops` to see planted plants",
        inline=False,
    )

    e.add_field(name="- :moneybag: Merchandise: ", value=mout, inline=False)

    await message.reply(embed=e)
