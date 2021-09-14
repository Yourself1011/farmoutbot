from replit import db
from contracts import contracts
import discord


async def contract(message, client):
    return

    prefix = db["server"][str(message.guild.id)]["prefix"]
    args = message.content.split(" ")
    if len(args) == 2:
        return "do a subcommand: `show`, `sign`, `complete`, or `current`"
        return
    if str(message.author.id) not in db["members"]:
        return "make a farm first"
        return
    if args[2].lower() not in ["show", "sign", "complete", "current"]:
        return "uhh wrong"
        return
    command = args[2].lower()
    try:
        currentpart = str(db["members"][str(message.author.id)]["currentcontract"][0])
    except:
        currentpart = "1"

    if command == "show":
        e = discord.Embed(title="", colour=discord.Colour.red())
        e.set_author(name="Contracts: ", icon_url=message.author.avatar_url)
        for i in contracts[currentpart]:
            desc = contracts[currentpart][i]["description"]
            need = contracts[currentpart][i]["need"][0]
            reward = contracts[currentpart][i]["reward"][0]
            title = contracts[currentpart][i]["title"]
            if (
                i
                in db["members"][str(message.author.id)]["donecontracts"][0][
                    str(currentpart)
                ]
            ):
                e.add_field(
                    name=f"- ~~{title}~~ COMPLETED",
                    value=f"~~**Description:** {desc}~~\n\n~~**Need:** {need}~~\n~~**Reward:** {reward}~~",
                )
            else:
                e.add_field(
                    name=f"- {title}",
                    value=f"**Description:** {desc}\n\n**Need:** {need}\n**Reward:** {reward}",
                )
        prefix = db["server"][str(message.guild.id)]["prefix"]
        e.set_footer(text=f"Part {currentpart} of 4")
        return e
        return

    if command == "sign":
        currentpart = str(currentpart)
        if len(args) == 3:
            return "which one are you signing lol"
            return
        if not args[3].isnumeric():
            return "gotta say a number corresponding to the contract id"
            return
        signed = int(args[3])
        if signed not in [1, 2, 3]:
            return "what"
            return
        if (
            signed
            in db["members"][str(message.author.id)]["donecontracts"][0][currentpart]
        ):
            return "oy you've already done that contract"
            return
        if (
            not db["members"][str(message.author.id)]["currentcontract"] == []
            and signed == db["members"][str(message.author.id)]["currentcontract"][1]
        ):
            return "you're doing that contract right now idot"
            return
        a = db["members"]
        a[str(message.author.id)]["currentcontract"] = [currentpart, signed]
        db["members"] = a
        return (
            f"You signed contract {signed} of part {currentpart}. Do `{prefix} contract current` to see your currently signed contract.",
            True,
        )
        return

    if command == "current":
        if (
            db["members"][str(message.author.id)]["currentcontract"] == []
            or len(db["members"][str(message.author.id)]["currentcontract"]) == 1
        ):
            return "you havent signed a contract yet"
            return
        e = discord.Embed(title="", colour=discord.Colour.orange())
        i = db["members"][str(message.author.id)]["currentcontract"][1]
        e.set_author(name="Current contract: ", icon_url=message.author.avatar_url)
        i = str(i)
        desc = contracts[currentpart][i]["description"]
        need = contracts[currentpart][i]["need"][0]
        reward = contracts[currentpart][i]["reward"][0]
        title = contracts[currentpart][i]["title"]
        e.add_field(
            name=f"- {title}",
            value=f"**Description:** {desc}\n\n**Need:** {need}\n**Reward:** {reward}",
        )
        e.set_footer(
            text=f"Do <{prefix} contract complete> to complete the contract once you have all the required items."
        )
        return (e, True)

    if command == "complete":
        if (
            db["members"][str(message.author.id)]["currentcontract"] == []
            or len(db["members"][str(message.author.id)]["currentcontract"]) == 1
        ):
            return "you havent signed a contract yet bruh"
            return
        completed = str(db["members"][str(message.author.id)]["currentcontract"][1])
        currentpart = str(db["members"][str(message.author.id)]["currentcontract"][0])
        if (
            contracts[currentpart][completed]["need"][2]
            not in db["members"][str(message.author.id)]["merch"]
            or contracts[currentpart][completed]["need"][1]
            > db["members"][str(message.author.id)]["merch"][
                contracts[currentpart][completed]["need"][2]
            ]
        ):
            return "you dont have what you need to complete the contract"
            return
        a = db["members"]
        if a[str(message.author.id)]["currentcontract"][1] == 3:
            a[str(message.author.id)]["currentcontract"] = [currentpart + 1]
        else:
            a[str(message.author.id)]["currentcontract"] = [currentpart]
        try:
            a[str(message.author.id)]["donecontracts"][0][int(currentpart)].append(
                completed
            )
        except:
            a[str(message.author.id)]["donecontracts"][0][int(currentpart)] = [
                completed
            ]
        if contracts[currentpart][completed]["reward"][2] != "ginsengseeds":
            if (
                contracts[currentpart][completed]["reward"][2]
                not in db["members"][str(message.author.id)]["merch"]
            ):
                a[str(message.author.id)]["merch"][
                    contracts[currentpart][completed]["reward"][2]
                ] = contracts[currentpart][completed]["reward"][1]
            else:
                a[str(message.author.id)]["merch"][
                    contracts[currentpart][completed]["reward"][2]
                ] += contracts[currentpart][completed]["reward"][1]
        else:
            if (
                contracts[currentpart][completed]["reward"][2]
                not in db["members"][str(message.author.id)]["seeds"]
            ):
                a[str(message.author.id)]["seeds"][
                    contracts[currentpart][completed]["reward"][2]
                ]["amount"] = contracts[currentpart][completed]["reward"][1]
            else:
                a[str(message.author.id)]["seeds"][
                    contracts[currentpart][completed]["reward"][2]
                ]["amount"] += contracts[currentpart][completed]["reward"][1]

        if len(contracts[currentpart][completed]["reward"]) == 4:
            a[str(message.author.id)]["money"] += contracts[currentpart][completed][
                "reward"
            ][3]
        a[str(message.author.id)]["merch"][
            contracts[currentpart][completed]["need"][2]
        ] -= contracts[currentpart][completed]["need"][1]
        if (
            a[str(message.author.id)]["merch"][
                contracts[currentpart][completed]["need"][2]
            ]
            == 0
        ):
            del a[str(message.author.id)]["merch"][
                contracts[currentpart][completed]["need"][2]
            ]
        db["members"] = a
        if currentpart == 4 and completed == 3:
            return (
                "as you come home with the eggs, you notice something. one of the eggs is very, very heavy, much heavier than the rest of them. \n\nyou crack it open, and see something that only has been mentioned in myths, stories, and rumors. you find the undead wool.\n\nthis wool will protect you, your animals, and your crops from death as long as you have it. you cannot trade for it, but you can gift it to others.\n**undeadwool +1**",
                True,
            )
            a = db["members"]
            a[str(message.author.id)]["merch"]["undeadwool"] = 1
            db["members"] = a
            return
        else:
            return (
                f"yay you completed contract #{completed} of part {currentpart}.",
                True,
            )
