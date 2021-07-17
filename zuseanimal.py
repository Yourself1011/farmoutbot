from replit import db
from zstats import animals, tools, deaths, births, locations
import time
import random
import asyncio
from math import floor
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import discord

async def useanimal(message, animal, client, thing):
    if str(message.author.id) not in db["members"]:
        await message.channel.send(" Make an account first, then worry about animals**")
        return

    if animal not in db["members"][str(message.author.id)]["animals"]:
        await message.channel.send(" You don't have that :angry:")
        return

    now2 = int(round(time.time() * 1000))

    f = db["members"][str(message.author.id)]["animals"][animal]["lastused"] - now2

    f = str(f)

    newvar = (
        animals[animal]["cooldown"]
        + db["members"][str(message.author.id)]["animals"][animal]["lastused"]
    )

    e = round((newvar - now2) / 1000)

    f = animals[animal]["cooldown"] / 1000

    if f - e <= 10 and db['members'][str(message.author.id)]['money'] > 250:

        paid = random.randint(1, 3)

        if db["members"][str(message.author.id)]["money"] < paid:
            paid = db["members"][str(message.author.id)]["money"]

        await message.channel.send(
            f" You used your {animal} too early and hurt it. You paid `{paid}` coins for the medical bills"
        )

        a = db["members"]
        a[str(message.author.id)]["money"] -= paid
        db["members"] = a

    now = int(round(time.time() * 1000))

    if (
        db["members"][str(message.author.id)]["animals"][animal]["lastused"]
        + animals[animal]["cooldown"]
        > now
    ):
        now2 = int(round(time.time() * 1000))

        f = db["members"][str(message.author.id)]["animals"][animal]["lastused"] - now2
        f = str(f)

        newvar = (
            animals[animal]["cooldown"]
            + db["members"][str(message.author.id)]["animals"][animal]["lastused"]
        )

        e = round((newvar - now2) / 1000)
        await message.reply(
            f" Your {animal}(s) are not ready, wait `" + str(e) + "` seconds.", True
        )
        return

    tool = None
		for i in animals[animal]['tools']:
			if i in db['members'][str(message.author.id)]['tools']:
				tool = i 
				break

    if tool == None:
        r = animals[animal]["tool"][0]
        await message.channel.send(f" buy a(n) `{r}` first")
        return

    toolbreak = ""

		a = db['members']

    amount = a[str(message.author.id)]["animals"][animal]["amount"]
    
    if amount > db["members"][str(message.author.id)]["tools"][tool]:
			a = db["members"]
			del a[str(message.author.id)]["tools"][tool]
			db["members"] = a

      things = ["LOL", "u dum dum", "ur fat", "go donate to yogogiddap", "idiot"]
      thing = random.choice(things)
      toolbreak = f"your `{tool}` broke {thing}"
  
    else:
        a = db["members"]
        a[str(message.author.id)]["tools"][tool] -= amount
        if a[str(message.author.id)]["tools"][tool] <= 0:
            del a[str(message.author.id)]["tools"][tool]
        db["members"] = a

    now = int(round(time.time() * 1000))
    a = db["members"]
    a[str(message.author.id)]["animals"][animal]["lastused"] = now
    merch = animals[animal]["result"]

    location = locations[db["members"][str(message.author.id)]["location"]]

    amount += (
        location["multis"][animal]
        if animal in location["multis"]
        else location["baseMulti"]
    )

    if amount > 50:
      randomrea = random.randint(1, 5)
      if randomrea == 1:
      		amount = int(round(amount * 0.7))
      if randomrea == 2:
      		amount = int(round(amount * 0.8))
    if merch not in a[str(message.author.id)]["merch"]:
        a[str(message.author.id)]["merch"][merch] = amount
    else:
        a[str(message.author.id)]["merch"][merch] += amount

    a[str(message.author.id)]["amounts"]["used"] += amount
    thing = animals[animal]["thing"]
    db["members"] = a
    cooldown = animals[animal]["cooldown"] / 1000

    a = db["members"]
    user = a[str(message.author.id)]
    location = locations[user["location"]]
    if (
        not location["defaultLife"]
        and (
            animal not in location["lifeOverrides"]
            or not location["lifeOverrides"][animal]
        )
    ) or (
        location["defaultLife"]
        and animal in location["lifeOverrides"]
        and location["lifeOverrides"][animal]
    ):
        amountLost = floor(
            max(
                user["animals"][animal]["amount"] * location["deathRate"],
                min(10, user["animals"][animal]["amount"]),
            )
        )

        user["animals"][animal]["amount"] -= amountLost
        await message.channel.send(
            f"Idiot your {animal}(s) couldn't live there and {amountLost} died."
        )
        db["members"] = a
        return

    print(f"{message.author.name} used {amount} {animal}")

    thingsaid = ""
    echance = random.randint(1, 2)
    if toolbreak == '':
          regdur = tools[tool]['durability']
          currentdur = db['members'][str(message.author.id)]['tools'][tool]
          toolbreak = f'{tool}: {currentdur}/{regdur} durability'
    emoji = animals[animal]['name'].split(' ')[1]
    e = discord.Embed(
        	title = '',
        	colour = discord.Colour.green()
        )
    e.set_author(
				name=f"{message.author.name}",         icon_url=message.author.avatar_url
		)
    animalamount = db['members'][str(message.author.id)]['animals'][animal]['amount']
    e.add_field(name = f'{emoji} - {animalamount} {animal}(s) {thing}ed', value = f'- {animal} cooldown +{int(cooldown)}s\n- {toolbreak}\n- {merch} +{amount}')
    e.set_footer(text = f'Wait {int(cooldown)} seconds before {thing}ing your {animal} again')
    print(echance)
    if echance == 1:
        await message.reply(embed = e)
        return	
    if echance == 2:
        whatthingchance = random.randint(1, 4)
        if whatthingchance in [1, 2, 3]:
            randomra = random.randint(1, 2)
            if "undeadwool" in db["members"][str(message.author.id)]["merch"]:
                return
            if amount > 11:
                death = random.choice(list(deaths.keys()))

                deadamount = random.randint(1, round(amount / 4))

                if randomra == 1:
                    thingtotype = deaths[death]
                    thingsaid = f"Oh no!{deadamount} of your {animal}s are trying to die {death}! quick, type `{thingtotype}` in the chat now!"

                    await message.reply(thingsaid, embed = e)

                    channel = message.channel

                    reply = None

                    def check(m):
                        return (
                            m.content.lower() == thingtotype.lower()
                            and m.author.id == message.author.id
                        )

                    try:
                        reply = await client.wait_for(
                            "message", timeout=10.0, check=check
                        )
                    except asyncio.TimeoutError:
                        await channel.send("idiot your animals died")
                        a = db["members"]
                        a[str(message.author.id)]["animals"][animal][
                            "amount"
                        ] -= deadamount
                        if a[str(message.author.id)]["animals"][animal]["amount"] == 0:
                            del a[str(message.author.id)]["animals"][animal]
                        db["members"] = a
                        return
                    else:

                        newamount = int(round(deadamount*0.2))
                        await channel.send(f"you managed to save most of the animals, but {newamount} died anyway oof")
                        a = db['members'][str(message.author.id)]
                        a['animals'][animal]['amount'] -= newamount
                        db['members'][str(message.author.id)] = a

                        return
                elif randomra == 2:
                    emojis = ["🐑", "🐔", "🐄"]
                    emoji = random.choice(emojis)
                    thingsaid = f"ahh your {deadamount} {animal}(s) are dying {death}, quick react with {emoji}"

                    await message.reply(thingsaid, embed = e)

                    def check(reaction, user):
                        return user == message.author and str(reaction.emoji) == emoji

                    try:
                        reaction, user = await client.wait_for(
                            "reaction_add", timeout=15.0, check=check
                        )
                    except asyncio.TimeoutError:
                        await message.channel.send(f"bruh your {animal}s died")
                        a = db["members"]
                        a[str(message.author.id)]["animals"][animal][
                            "amount"
                        ] -= deadamount
                        if a[str(message.author.id)]["animals"][animal]["amount"] == 0:
                            del a[str(message.author.id)]["animals"][animal]
                        db["members"] = a
                        return
                    else:
                        await message.channel.send("phew you saved your animals")

        now = int(round(time.time() * 1000))
        if whatthingchance == 4:
            if "lastbred" in db["members"][str(message.author.id)]["animals"][animal]:
                if (
                    db["members"][str(message.author.id)]["animals"][animal]["lastbred"]
                    + 3600000
                    > now
                ):
                    return
            if amount < 8:
                await message.reply(embed = e)
                return

            randomrar = random.randint(1, 2)
            if randomrar == 1:
                thingtotype = random.choice(births)
                thingsaid = f"{message.author.mention} ar ur animals are trying to breed, better type `{thingtotype}` or else they won't"

                await message.reply(thingsaid, embed = e)

                channel = message.channel

                reply = None

                def check(m):
                    return (
                        m.content.lower() == thingtotype.lower()
                        and m.author.id == message.author.id
                    )

                try:
                    reply = await client.wait_for("message", timeout=10.0, check=check)
                except asyncio.TimeoutError:
                    await channel.send("idiot your animals didn't breed")
                    return
                else:
                    bornedamount = random.randint(1, round(amount / 5))
                    await channel.send(f"oop {bornedamount} {animal}(s) were born")
                    a = db["members"]
                    a[str(message.author.id)]["animals"][animal][
                        "amount"
                    ] += bornedamount
                    a[str(message.author.id)]["animals"][animal]["lastbred"] = now
                    db["members"] = a
                    return
            elif randomrar == 2:
                thingtotype = random.choice(births)
                animales = [
                    "https://opensanctuary.org/wp-content/uploads/2018/04/Bitsy-sheep.jpg",
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Cow_female_black_white.jpg/1200px-Cow_female_black_white.jpg",
                    "https://4-hontario.ca/wp-content/uploads/2020/09/Poultry_Main-Image-1626x1080.jpeg",
                ]
                animale = random.choice(animales)
                thingsaid = f"{message.author.mention} woah your {animal}s are breeding but they won't unless you say what animal this is\nuse the buttons to choose\n{animale}"

                await message.reply(thingsaid, embed = e,                    components=[
                        Button(style=ButtonStyle.grey, label="Sheep"),
                        Button(style=ButtonStyle.grey, label="Chicken"),
                        Button(style=ButtonStyle.grey, label="Cow"),
                    ],
                )
                res = await client.wait_for("button_click")
                if res.author == message.author:
                    if (
                        res.component.label == "Sheep"
                        and animale
                        == "https://opensanctuary.org/wp-content/uploads/2018/04/Bitsy-sheep.jpg"
                        or res.component.label == "Chicken"
                        and animale
                        == "https://4-hontario.ca/wp-content/uploads/2020/09/Poultry_Main-Image-1626x1080.jpeg"
                        or res.component.label == "Cow"
                        and animale
                        == "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Cow_female_black_white.jpg/1200px-Cow_female_black_white.jpg"
                    ):
                        bornedamount = random.randint(1, round(amount / 5))
                        if amount > 100:
                            bornedamount = random.randint(1, round(amount / 9))
                        if amount > 500:
                            bornedamount = random.randint(1, round(amount / 45))
                        if amount > 1000:
                            bornedamount = random.randint(1, round(amount / 90))
                        if amount > 5000:
                            bornedamount = random.randint(1, round(amount / 5000))
                        await message.channel.send(
                            f"oop {bornedamount} {animal}(s) were born"
                        )
                        a = db["members"]
                        a[str(message.author.id)]["animals"][animal][
                            "amount"
                        ] += bornedamount
                        a[str(message.author.id)]["animals"][animal]["lastbred"] = now
                        db["members"] = a
                        return
                    else:
                        await message.channel.send("bruh ur animals didnt breed")
                        return
