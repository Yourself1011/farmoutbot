from replit import db
import time
from datetime import date
from zstats import tools, seeds


async def start(message, client):
    if str(message.author.id) in db["members"]:
        await message.channel.send("You already made an account dum dum")
    else:
        today = date.today()
        datemade = today.strftime("%B %d, %Y")
        a = db["members"]
        a[str(message.author.id)] = {
            "animals": {},
            "tools": {"wateringcan": tools["wateringcan"]["durability"]},
            "merch": {},
            "seeds": {"grassseeds": {"amount": 5}},
            "plantcooldowns": {},
            "plants": {},
            "dailytimer": 0,
            "hourlytimer": 0,
            "money": 100,
            "reputation": 500,
            "amounts": {
                "shared": 0,
                "gambled": 0,
                "bought": 0,
                "sold": 0,
                "used": 0,
            },
            "prestige": 0,
            "multi": 1.0,
            "commandsused": 0,
            "datemade": datemade,
            "trades": {"lastTradeId": 0, "tradeAmts": [0, 0, 0], "stock": [0, 0, 0]},
            "cooldowns": {
                "daily": 0,
                "hourly": 0,
                "lastdaily": " ¯\_(ツ)_/¯",
                "dailystreak": 0,
            },
            "donecontracts": [{"1": [], "2": [], "3": [], "4": []}],
            "currentcontract": [1, 1],
            "prestige": 0,
            "location": "default",
            "locations": {},
            "settings": {"votedm": True, "tips": True, "emojionlyinv": False},
        }
        db["members"] = a
        prefix = db["server"][str(message.guild.id)]["prefix"]
        await message.channel.send(
            f"{message.author.mention}\nWelcome to the start of your farming career in Farmout! Here, you will plant seeds for crops, take care of animals, and trade for new items. \n\nTo start, you should use some of these commands:\n-`{prefix} help` shows all commands, do `{prefix} help (command)` to get help about a specific command\n-`{prefix} plant grassseeds 5` plants 5 grassseeds. Do `{prefix} crops` to see all the things you've planted, and `{prefix} collect` to collect them once they are ready.\n-`{prefix} daily` claims your daily reward\n-`{prefix} shop` opens the shop, where you can buy and sell items\n`{prefix} guide` gives you more information on various aspects of the game \nIf you need more help, you can join our support server, or use the guide command. Good luck for now!"
        )


"""
from replit import db
a = db["members"]
for i in a: 
    a[i][""] = 


db["members"] = a

"""
