from replit import db
import discord
import time
from zstats import animals, pages, choosecolour


async def pens(message, client): #pens more like peni-
    args = message.content.split(" ")
    if str(message.author.id) not in db["members"]:
        await message.channel.send("make an account first strumfum")
        return
    if db["members"][str(message.author.id)]["land"]["animals"] == {}:
        await message.channel.send("no pens here")
        return

    pens1324 = list(db["members"][str(message.author.id)]["land"]["animals"].values()) 
    pen = pens1324[0]
    feld = 0
    if len(args) >= 3 and args[2].lower() == "rename":
        if len(args) == 3:
            return "which pen u renaming lol"
        if int(args[3]) > len(pens1324):
            return "that's not a pen"

        pens1324 = db["members"][str(message.author.id)]["land"]["animals"]
        pen = list(pens1324)[int(args[3]) - 1]
        print(pen)

        newname = args[4]
        a = db["members"]
        a[str(message.author.id)]["land"]["animals"][pen]["name"] = newname
        db["members"] = a

        return f"you renamed `{pen}` to `{args[4]}`"

    if (
        len(args) == 3
        and args[2].isnumeric()
        and int(args[2]) <= len(pens)
        and int(args[2]) > 0
    ):
        feld = max(min(int(int(args[2]) - 1), len(pens)), 0)
        pen = pens[feld]
    e = discord.Embed(title=f"", colour=choosecolour())
    e.set_author(
        name=f"{message.author.name}'s farm", icon_url=message.author.avatar_url
    )

    now = int(round(time.time() * 1000))
    await pages(
        message,
        client,
        [{
            "name": f"{i['name']}",  #no name is name of pen
            "value": '\n'.join(
              [
             f'**- {animals[k]["name"]}:**\nAmount: **{j["amount"]}** | Status: **{str(round((j["lastused"] + animals[k]["cooldown"]-now)/1000))+" secs" if j["lastused"] + animals[k]["cooldown"] > now else "Ready!"}**'
                for k, j in i["animals"].items() 
              ]
            )
            if i["animals"] != {}
            else "***cricket noises***",
          }
          for i in pens1324 #tf lmao
        ],
        1,
        startPage=feld + 1,
        baseEmbed=e,
    )