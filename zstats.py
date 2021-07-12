from random import uniform
from numpy.random import choice
from math import floor, ceil
import collections.abc
from copy import deepcopy
import discord
from discord_components import Button
from asyncio import TimeoutError
import random

def choosecolour():
	colours = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold()]
	colour = random.choice(colours)
	return colour

def getMember(search, guildId, client):
    if type(search) is list:
        search = " ".join(search)
    id = search.translate({ord(x): "" for x in ["<", "@", "!", ">"]})
    guild = client.get_guild(guildId)
    out = guild.get_member(int(id)) if id.isnumeric() else False

    if not bool(out):
        possibilities = [
            i
            for i in guild.members
            if search.lower() in f"{i.name.lower()}#{i.discriminator}"
            or (bool(i.nick) and search.lower() in i.nick)
        ]
        if not bool(possibilities):
            out = False
        else:
            out = min(possibilities, key=lambda x: len(x.name))

    return out


def softSearch(list, search, ignore=[]):
    """Returns the smallest string that has the search in the list. Will ignore all values in list ignore. Returns None if none exist. List can be any iterable, including objects"""
    possibilities = [i for i in list if search.lower() in i.lower() and i not in ignore]
    if not bool(possibilities):
        return None
    return min(possibilities, key=len)


def convertInt(string):
    try:

        out = string.lower().translate({ord(x): "" for x in [",", " "]})

        if "e" in out:
            arr = out.split("e")
            out = float(arr[0]) * (10 ** float(arr[1]))
        elif out[-1] == "k":
            out = float(out[:-1]) * 1000
        elif out[-1] == "m":
            out = float(out[:-1]) * 1000000
        elif out[-1] == "b":
            out = float(out[:-1]) * 1000000000
        elif out[-1] == "t":
            out = float(out[:-1]) * 1000000000000

        return int(out)

    except:
        return None


# Chooses k unique random elements from a population sequence or set.

# Returns a new list containing elements from the population while
# leaving the original population unchanged.  The resulting list is
# in selection order so that all sub-slices will also be valid random
# samples.  This allows raffle winners (the sample) to be partitioned
# into grand prize and second place winners (the subslices).

# Members of the population need not be hashable or unique.  If the
# population contains repeats, then each occurrence is a possible
# selection in the sample.

# To choose a sample in a range of integers, use range as an argument.
# This is especially fast and space efficient for sampling from a
# large population:   sample(range(10000000), 60)


def gatheringCmd(msg, loottable, amount=[1, 1, 1]):
    """
    Returns an array of the item gathered and the amount, or an array with. Loottable should be an object with keys as the item name, and values as an array of chance (out of total chances), maximum amount, minimum amount (optional, defaults to 1), and weight (defaults to 1).
    """

    repeat = floor(amount[0] + (amount[1] - amount[0]) * (uniform(0, 1) ** amount[2]))
    out = []

    length = len(loottable.keys())
    total = sum([i[0] for i in loottable.values()])

    if repeat > length:
        for i, j in loottable.items():
            out.append(
                [
                    i,
                    floor(
                        # Average amount of times to get this item, plus or minus a little
                        (
                            (j[0] / total)
                            + ((j[0] / total) * uniform(0, 0.10) * choice([-1, 1], 1))
                        )
                        * repeat
                        *
                        # average amounts per land
                        (j[2] + (j[1] - j[2]) * (uniform(0, 1) ** j[3]))
                    ),
                ]
            )
        return out
    print(total)
    print([i[0] / total for i in loottable.values()])
    
    # Gets all the items
    sample = choice(
        list(loottable.keys()),
        repeat,
        p=[i[0] / total for i in loottable.values()],
        replace=False,
    )

    for i in range(repeat):

        item = loottable[sample[i]]

        # Gets the amount
        p = item[3] if len(item) >= 4 else 1
        minimum = item[2] if len(item) >= 3 else 1
        maximum = item[1]
        amt = floor(minimum + (maximum - minimum) * (uniform(0, 1) ** p))

        if amount == [1, 1, 1]:
            return [sample[i], amt]
        else:
            out.append([sample[i], amt])

    return out


def updateDict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = updateDict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def getShop(shops, location):
    for i, j in zip(
        [animals, tools, seeds, merch], ["animals", "tools", "seeds", "merch"]
    ):
        update = {k: v for k, v in locations[location]["shop"].items() if k in i}
        shops[j] = updateDict(deepcopy(i), update)


# Paste in commands that use these shops (and import getShop)

# obj = {"animals": {}, "tools": {}, "seeds": {}, "merch": {}}
# getShop(obj, db["members"][str(message.author.id)]["location"])
# animals, tools, seeds, merch = obj["animals"], obj["tools"], obj["seeds"], obj["merch"]

async def pages(message, client, items, displayAmount, startPage = 1, baseEmbed = discord.Embed(), newField = True):
    """
    Button pagination

    Parameters:
    ----------
    message: discord.Message - the message where the command was run
    client: discord.Client - the discord client
    items: dictionary - a array containing a dictionary with a name and a value for each item, or an array of values if newField is false
    displayAmount: int - the amount of items displayed per page
    startPage: int - the page to start on (starts at 1)
    baseEmbed: discord.Embed() - defaults to an empty embed, the base embed to use
    newField: bool - whether each item gets placed in a new field or not
    """
    
    page = int(startPage) - 1
    maxPages = ceil(len(items) / displayAmount)
    msg = None
    loop = True

    while loop:
        embed = baseEmbed.copy()
        displayItems = items[page * displayAmount:page * displayAmount + displayAmount]

        if newField:
            for i in displayItems:
                embed.add_field(
                    name = i["name"],
                    value = i["value"]
                )
        else:
            embed.description = embed.description + "\n".join(displayItems)
        
        embed.set_footer(text = f"Page {page + 1}/{maxPages}")

        if not bool(msg):
            msg = await message.channel.send(
                embed = embed,
                components = [[
                    Button(emoji = "⏮️", style = 1, disabled = True if page == 0 else False),
                    Button(emoji = "◀️", style = 1, disabled = True if page == 0 else False),
                    Button(emoji = "✖️", style = 4),
                    Button(emoji = "▶️", style = 1, disabled = True if page == maxPages - 1 else False),
                    Button(emoji = "⏭️", style = 1, disabled = True if page == maxPages - 1 else False),
                ]]
            )
        
        else:
            await msg.edit(
                embed = embed,
                components = [[
                    Button(emoji = "⏮️", style = 1, disabled = True if page == 0 else False),
                    Button(emoji = "◀️", style = 1, disabled = True if page == 0 else False),
                    Button(emoji = "✖️", style = 4),
                    Button(emoji = "▶️", style = 1, disabled = True if page == maxPages - 1 else False),
                    Button(emoji = "⏭️", style = 1, disabled = True if page == maxPages - 1 else False),
                ]]
            )

        try:
            res = await client.wait_for(
                "button_click", 
                timeout = 100.0,
                check = lambda x: x.author.id == message.author.id and msg.id == x.message.id
            )
        except TimeoutError:
            await msg.edit(components = [])
            loop = False
        else:
            if res.component.emoji.name == "⏮️":
                page = 0

            elif res.component.emoji.name == "◀️":
                page = max(0, page - 1)

            elif res.component.emoji.name == "✖️":
                print('adit')
                await msg.edit(components = [])
                loop = False

            elif res.component.emoji.name == "▶️":
                page = min(maxPages - 1, page + 1)

            elif res.component.emoji.name == "⏭️":
                page = maxPages - 1
            
            await res.respond(type = 6)

#sellcost is exactly half of cost
#tv is 25, 50, or 100 less than sellcost
animals = {
    "name": "animals",
    "sheep": {
        "name": "sheep :sheep:",
        "cost": 250,
        "sellcost": 175,
        "tool": "shears",
        "result": "wool",
        "cooldown": 70000,
        "thing": "shear",
        "tradevalue": 150,
    },
    "cow": {
        "name": "cow :cow:",
        "cost": 775,
        "sellcost": 387,
        "tool": "bucket",
        "result": "milk",
        "cooldown": 60000,
        "thing": "milk",
        "tradevalue": 330,
    },
    "chicken": {
        "name": "chicken :chicken:",
        "cost": 75,
        "sellcost": 38,
        "tool": "nest",
        "result": "egg",
        "cooldown": 50000,
        "tradevalue": 35,
        "thing": "collect",
    },
    "goat": {
        "name": "goat :goat:",
        "cost": 275,
        "sellcost": 138,
        "tool": "bucket",
        "result": "goatsmilk",
        "cooldown": 50000,
        "tradevalue": 100,
        "thing": "milk",
    },
    "horse": {
        "name": "horse :horse:",
        "cost": 1250,
        "sellcost": 625,
        "tool": "saddle",
        "result": "horsehair",
        "cooldown": 60000,
        "tradevalue": 600,
        "thing": "haired",
    },
    # Exotic animals
    "camel": {
        "name": "camel :dromedary_camel:",
        "cost": "Only obtainable through trading",
        "sellcost": 500,
        "tool": "toilet",
        "result": "cameldung",
        "cooldown": 50000,
        "thing": "milk",
        "tradevalue": 350,
        "give": True,
    },
    "snake": {
        "name": "snake :snake:",
        "cost": "Only obtainable through trading",
        "sellcost": 350,
        "tool": "venomextractor",
        "result": "snakevenom",
        "cooldown": 70000,
        "thing": "extract venom",
        "tradevalue": 200,
        "give": True,
    },
    "babbon": {
        "name": "babbon :monkey: ",
        "cost": "trade only",
        "sellcost": 400,
        "tool": "babboner",
        "result": "kidney",

        "cooldown": 50000,
        "thing": "babbon",
        "tradevalue": 250,
    },
    "peacock": {
        "name": "peacock :peacock:",
        "cost": "trade only",
        "sellcost": 300,
        "tool": "feathergetter",
        "result": "peacockfeather",
        "cooldown": 45000,
        "thing": "get",
        "tradevalue": 200,
    },
		'walrus': {
			'name': 'walrus :seal: ',
			'cost': 'trade only',
			'sellcost': 600,
			'tool': 'toothbrush',
			'result': 'walrustusk',
			'cooldown': 50000,
			'thing': 'brush',
			'tradevalue': 350
		}

}

#durability is cost
#sellcost is 1/2 cost
tools = {
    "name": "tools",
    "shears": {
        "name": "shears",
        "cost": 50,
        "durability": 50,
        "sellcost": 25,
        "animal": "sheep",
        "tradevalue": 25,
    },
    "sandals": {
        "name": "sandals",
        "cost": 15,
        "sellcost": 8,
        "durability": 15,
        "animal": "beach",
        "tradevalue": 8,
    },
    "steelshears": {
        "name": "steelshears",
        "cost": 150,
        "sellcost": 75,
        "durability": 150,
        "animal": "sheep",
        "tradevalue": 70,
    },
    "shaver": {
        "name": "shaver",
        "cost": 400,
        "sellcost": 200,
        "durability": 400,
        "animal": "sheep",
        "tradevalue": 175,
    },
    "wateringcan": {
        "name": "wateringcan",
        "cost": 125,
        "durability": 125,
        "sellcost": 62,
        "animal": "seed",
        "tradevalue": 60,
    },
    "babboner": {
        "name": "babboner",
        "cost": 125,
        "durability": 125,
        "sellcost": 62,
        "animal": "babbon",
        "tradevalue": 60,
    },
    "bettercan": {
        "name": "bettercan",
        "cost": 250,
        "durability": 250,
        "sellcost": 125,
        "animal": "seed",
        "tradevalue": 120,
    },
    "hose": {
        "name": "hose",
        "cost": 1000,
        "durability": 1000,
        "sellcost": 500,
        "animal": "seed",
        "tradevalue": 450,
    },
    "sprinkler": {
        "name": "sprinkler",
        "cost": 2500,
        "durability": 2500,
        "sellcost": 1250,
        "animal": "seed",
        "tradevalue": 1000,
    },
    "bucket": {
        "name": "bucket",
        "cost": 250,
        "durability": 250,
        "sellcost": 125,
        "animal": "cow",
        "tradevalue": 120,
    },
    "saddle": {
        "name": "saddle",
        "cost": 150,
        "durability": 150,
        "sellcost": 75,
        "animal": "horse",
        "tradevalue": 70,
    },
    "steelbucket": {
        "name": "steelbucket",
        "cost": 650,
        "durability": 650,
        "sellcost": 135,
        "animal": "cow",
        "tradevalue": 130,
    },
    "toilet": {
        "name": "toilet",
        "cost": 250,
        "durability": 250,
        "sellcost": 125,
        "animal": "camel",
        "tradevalue": 115,
    },
    "megacoop": {
        "name": "megacoop",
        "cost": 500,
        "durability": 500,
        "sellcost": 250,
        "animal": "chicken",
        "tradevalue": 200,
    },
    "venomextractor": {
        "name": "venomextractor",
        "cost": 150,
        "durability": 150,
        "sellcost": 75,
        "animal": "snake",
        "tradevalue": 75,
    },
    "nest": {
        "name": "nest",
        "cost": 50,
        "durability": 50,
        "sellcost": 25,
        "animal": "chicken",
        "tradevalue": 25,
    },
    "chickenhouse": {
        "name": "chickenhouse",
        "cost": 150,
        "durability": 150,
        "sellcost": 75,
        "animal": "chicken",
        "tradevalue": 70,
    },
    "hikingboots": {
        "name": "hikingboots",
        "cost": 50,
        "durability": 25,
        "sellcost": 27,
        "animal": "forest",
        "tradevalue": 9,
    },
    "shoes": {
        "name": "shoes",
        "cost": 75,
        "durability": 40,
        "sellcost": 40,
        "animal": "jungle",
        "tradevalue": 15,
    },

    "feathergetter": {
        "name": "feathergetter",
        "cost": 150,
        "durability": 150,
        "sellcost": 75,
        "animal": "peacock",
        "tradevalue": 70,
    },
		'wintercoat' :{
			'name': 'wintercoat',
			'cost': 45,
			'durability': 40,
			'sellcost': 25,
			'animal': 'arctic',
			'tradevalue': 29
		},
		'toothbrush': {
			'name': 'toothbrush',
			'cost': 50,
			'sellcost': 25,
			'durability': 50,
			'animal': 'walrus',
			'tradevalue': 25
		}

}

seeds = {
    "name": "seeds",
    # Normal seeds
    "grassseeds": {
        "name": "grassseeds",
        "cost": 5,
        "sellcost": 4,
        "growtime": 40000,
        "result": "grass",
        "tradevalue": 1,
    },
    "cornseeds": {
        "name": "cornseeds",
        "cost": 13,
        "sellcost": 12,
        "growtime": 43000,
        "result": "corn",
        "tradevalue": 2,
    },
    "strawberryseeds": {
        "name": "strawberryseeds",
        "cost": 15,
        "sellcost": 14,
        "growtime": 39000,
        "result": "strawberry",
        "tradevalue": 2,
    },
    "mangoseeds": {
        "name": "mangoseeds",
        "cost": 25,
        "sellcost": 22,
        "growtime": 45000,
        "result": "mango",
        "tradevalue": 5,
    },
    "appleseeds": {
        "name": "appleseeds",
        "cost": 13,
        "sellcost": 12,
        "stages": [1800000, 3600000, 86400000],
        "result": "apple",
        "tradevalue": 2,
        "amount": [10, 15],
    },
    "cactusseeds": {
        "name": "cactusseeds",
        "cost": 30,
        "sellcost": 25,
        "growtime": 30000,
        "result": "cactus",
        "tradevalue": 5,
    },
    # Seasonal seeds
    "pumpkinseeds": {
        "name": "pumpkinseeds",
        "cost": "Only available during fall",  # 20,
        "sellcost": 19,
        "growtime": 40000,
        "result": "pumpkin",
        "tradevalue": 5,
        "get": True,
        "give": True,
    },
    "tulipseeds": {
        "name": "tulipseeds",
        "cost": 15,  # "Only available during spring",
        "sellcost": 13,
        "growtime": 40000,
        "result": "tulip",
        "tradevalue": 5,
        "get": False,
        "give": False,
    },
    "sunflowerseeds": {
        "name": "sunflowerseeds",
        "cost": "Only available during summer",  # 20,
        "sellcost": 19,
        "growtime": 40000,
        "result": "sunflower",
        "tradevalue": 5,
        "get": True,
        "give": True,
    },
    "pinetreeseeds": {
        "name": "pinetreeseeds",
        "cost": "Only available during winter",  # 100,
        "sellcost": 19,
        "growtime": 3600000,
        "result": "pinetree",
        "tradevalue": 5,
        "get": True,
        "give": True,
    },
    # exotic seeds
    "ginsengseeds": {
        "name": "ginsengseeds",
        "cost": "Not buyable",
        "sellcost": "not sellable",
        "result": "ginseng",
        "tradevalue": 50,
        "growtime": 1000000,
        "get": True,
        "give": True,
    },
    "pridewatermelonseeds": {
        "name": "pridewatermelonseeds",
        "cost": 'Only available in pride month, even though you should always be pround', #100
        "sellcost": 90,
        "result": "pridewatermelon",
        "tradevalue": 10,
        "growtime": 60000,
        "get": False,
        "give": False,
    },
}

merch = {
    "name": "merch",
    # Misc merch
    "gem": {
        "name": "gem :gem:",
        "description": "collectible, shiny, trade it with people",
        "cost": 750,
        "sellcost": "Not sellable",
        "tradevalue": 750,
    },
    "fish": {
        "name": "fish :fish:",
        "description": "it's a fish man how much more do i have to tell you",
        "cost": 7,
        "sellcost": 6,
        "tradevalue": 6,
    },
    "fart": {
        "name": "fart :dash:",
        "description": "mm",
        "cost": 65,
        "sellcost": 50,
        "tradevalue": 50,
    },
    "rarepainting": {
        "name": "rarepainting :frame_photo: ",
        "description": "rare painting, looks kinda ugly but could sell for a lot\ncollectible and tradeable",
        "cost": 175,
        "sellcost": "Not sellable",
        "tradevalue": 175,
    },
    "dragonegg": {
        "name": "dragonegg :dragon_face: :egg: ",
        "cost": 1500,
        "description": "the egg of a fat dragon, can it hatch a new dragon?\ncollectible, found in the forest",
        "sellcost": "Not sellable",
        "tradevalue": 1000,
    },
    "computer": {
        "name": "computer :computer:",
        "cost": 1000,
        "description": "it can compute, but only when it wants to\ncollectible, trade it with people",
        "sellcost": "Not sellable",
        "tradevalue": 875,
    },
    "rarecoin": {
        "name": "rarecoin :coin: ",
        "description": "a coin that's pretty rare\ncollectible, tradeable",
        "cost": 175,
        "sellcost": "Not sellable",
        "tradevalue": 165,
    },
    "pebble": {
        "name": "pebble :rock:",
        "description": "mm, found in the forest",
        "cost": 5,
        "sellcost": 3,
        "tradevalue": 5,
    },
		'shirt': {
			'name': 'shirt :shirt: ',
			'description': 'not wearable (yet)',
			'cost': 15,
			'sellcost': 13,
			'tradevalue': 15
		},
    "voldysnose": {
        "name": "voldysnose :nose:",
        "description": "collectible, tradeable",
        "cost": 20,
        "sellcost": "Not sellable",
        "tradevalue": 20,
    },
    "croissant": {
        "name": "croissant :croissant: ",
        "description": "not eatable, tradeable",
        "cost": 20,
        "sellcost": "Not sellable",
        "tradevalue": 20,
    },
    "gamingpc": {
        "name": "gamingpc :video_game:",
        "description": "game on it or smth but you can't actually\nnot sellable",
        "cost": 5000,
        "sellcost": "Not sellable",
        "tradevalue": 4500,
    },
    "glasses": {
        "name": "glasses :eyeglasses:",
        "cost": 20,
        "description": "tradeable, sellable",
        "sellcost": 18,
        "tradevalue": 18,
    },
    "clock": {
        "name": "clock :clock1: ",
        "description": "what's the time?\ncollectible",
        "cost": 30,
        "sellcost": 25,
        "tradevalue": 25,
    },
    "applepie": {
        "name": "applepie :apple: :pie:",
        "description": "eatable, might taste good idk",
        "cost": 25,
        "sellcost": 19,
        "tradevalue": 19,
    },
    "bread": {
        "name": "bread :bread:",
        "description": "not eatable but it probably should be lmao\ntradeable",
        "cost": 20,
        "sellcost": 16,
        "tradevalue": 15,
    },
    "keyboard": {
        "name": "keyboard :keyboard:",
        "cost": 20,
        "description": "can't actually type\ntradeable",
        "sellcost": 18,
        "tradevalue": 17,
    },
    "flatbread": {
        "name": "flatbread :flatbread:",
        "description": "can't eat this either, pretty cool to look at tho\nbuyable, tradeable",
        "cost": 10,
        "sellcost": 8,
        "tradevalue": 5,
    },
    "xlorx": {
        "name": "xlorx :grey_question:",
        "cost": "unbuyable",
        "description": "it is so obvious what this is that it shouldn't even need a description like what who doesn't know what a xlorx is",
        "sellcost": "unsellable",
        "tradevalue": 999999999999,
        "give": True,
        "get": True,
    },
    # Animal merch
    "wool": {
        "name": "wool :cloud:",
        "description": "its from sheep, keep it away from dirt cuz it can get dirty easily",
        "cost": "Not buyable",
        "sellcost": 15,
        "tradevalue": 14,
        "get": True,
    },
    "goatsmilk": {
        "name": "goatsmilk :goat: :milk:",
        "description": "the milk of a goat, it doesn't taste as good as regular cow milk tho apparently",
        "cost": "Not buyable",
        "sellcost": 19,
        "tradevalue": 18,
        "get": True,
    },
    "horsehair": {
        "name": "horsehair :horse: :person_bald:",
        "cost": "Not buyable",
        "description": "hair of horse, hard to acquire",
        "sellcost": 20,
        "tradevalue": 19,
        "get": True,
    },
    "milk": {
        "name": "milk :milk:",
        "description": "milk, you can sell it or trade it",
        "cost": "Not buyable",
        "sellcost": 21,
        "tradevalue": 20,
        "get": True,
    },
    "cheese": {
        "name": "cheese :cheese:",
        "cost": 11,
        "description": "cheese, collectible",
        "sellcost": 9,
        "tradevalue": 8,
    },
    "egg": {
        "name": "egg :egg:",
        "description": "eggs from chickens, sellable",
        "cost": "Not buyable",
        "sellcost": 13,
        "tradevalue": 12,
        "get": True,
    },
    "kidney": {
        "name": "kidney :potato:",
        "cost": "Not buyable",
        "sellcost": 19,
        "tradevalue": 18,
        "description": "babbon your babbons for kidneys, usually sell for a lot but these are defective",
    },

    "peacockfeather": {
        "name": "peacockfeather :feather:",
        "cost": 19,
        "sellcost": 16,
        "tradevalue": 15,
        "description": "the feather of a peacock, commonly used to make pens",
    },
		'walrustusk': {
			'name': 'walrustusk :seal: :tooth:',
			'cost': 50,
			'sellcost': 35,
			'tradevalue': 30,
			'description': 'the tooth of a walrus. very nice'
		},

    # Plant merch
    "grass": {
        "name": "grass :seedling:",
        "description": "its grass, just sell it",
        "cost": 6,
        "sellcost": 5,
        "tradevalue": 4,
        "get": True,
    },
    "mango": {
        "name": "mango :mango:",
        "description": "the fruit of the mango plant",
        "cost": 29,
        "sellcost": 26,
        "tradevalue": 24,
        "get": True,
    },
    "apple": {
        "name": "apple :apple:",
        "description": "apples from the apple tree, sell it",
        "cost": 19,
        "sellcost": 17,
        "tradevalue": 16,
        "get": True,
    },
    "corn": {
        "name": "corn :corn:",
        "description": "good ol' corn on the cob",
        "cost": 19,
        "sellcost": 17,
        "tradevalue": 16,
        "get": True,
    },
    "strawberry": {
        "name": "strawberry :strawberry:",
        "cost": 21,
        "description": "strawberry fruit from the strawberry plant",
        "sellcost": 19,
        "tradevalue": 18,
        "get": True,
    },
    "ginseng": {
        "name": "ginseng :herb:",
        "cost": "not buyable",
        "description": "super rare, super expensive",
        "sellcost": "not sellable",
        "tradevalue": 100,
        "give": True,
        "get": True,
    },
    "cactus": {
        "name": "cactus :cactus:",
        "description": "a cactus that you can only get from the shop in the desert",
        "cost": 35,
        "sellcost": 32,
        "tradevalue": 20,
    },
    "pridewatermelon": {
				"name": "pridewatermelon :watermelon: :rainbow_flag:",
				"description": "happy pride month! only available in june, found in the jungle",
				"cost": 'only available in pride month', #180
				"sellcost": 150,
        "tradevalue": 65,
				'get': False,
				'give': False
    },
    # Gather only merch
    "mushroom": {
        "name": "mushroom :mushroom:",
        "cost": "Cannot be bought",
        "description": "you can eat it, but you probably shouldn't\nfound from gathering in the forest",
        "sellcost": 15,
        "tradevalue": 13,
    },
    "umbrella": {
        "name": "umbrella :beach_umbrella: ",
        "description": "strawberry fruit from the strawberry plant",
        "cost": "gather only",
        "sellcost": 44,
        "tradevalue": 43,
    },
    # Contract only merch
    "cake": {
        "name": "cake :cake:",
        "cost": "Cannot be bought",
        "description": "eatable, only available from completing contracts",
        "sellcost": 10,
        "tradevalue": 5,
        "get": False,
        "give": True,
    },
    "undeadwool": {
        "name": "undeadwool :skull_crossbones: :cloud: ",
        "cost": "cannot be bought, protects you and all your animals and plants from death",
        "description": "prevents death, lasts forever",
        "sellcost": "cant sell",
        "tradevalue": "not tradeable",
        "get": True,
        "give": True,
    },
    # Seasonal merch
    "pumpkin": {
        "name": "pumpkin :jack_o_lantern:",
        "cost": "Only available during fall",  # 50
        "description": "its a pumpkin\nsellable",
        "sellcost": 45,
        "tradevalue": 4,
        "get": True,
        "give": True,
    },
    "tulip": {
        "name": "tulip :tulip:",
        "cost": 'Only available during spring',  #25
        "description": "tulip, looks nice\nsellable",
        "sellcost": 20,
        "tradevalue": 16,
        "get": False,
        "give": False,
    },
    "sunflower": {
        "name": "sunflower :sunflower:",
        "cost": 50,  # Only available during summer
        "description": "a flower of the sun",
        "sellcost": 45,
        "tradevalue": 4,
        "get": True,
        "give": True,
    },
    "pinetree": {
        "name": "pinetree :evergreen_tree:",
        "cost": "Only available during winter",  # 150
        "description": "basically a christmas tree\nnice",
        "sellcost": 45,
        "tradevalue": 4,
        "get": True,
        "give": True,
    },
    "clover": {
        "name": "clover :four_leaf_clover: ",
        "cost": "Only available on St. Patrick's day",  # 10
        "description": "collectible, doesn't do anything",
        "sellcost": 9,
        "tradevalue": 20,
        "get": True,
        "give": True,
    },
    "easteregg": {
        "name": "easteregg :egg: :rabbit: ",
        "description": "collectible",
        "cost": "Only available from good friday to easter monday",  # 10
        "sellcost": 9,
        "tradevalue": 15,
        "get": True,
        "give": True,
    },
    # Exotic merch
    "cameldung": {
        "name": "cameldung :camel: :poop:",
        "description": "dung of camel\nsellable",
        "cost": "Not purchasable",
        "sellcost": 50,
        "tradevalue": 100,
        "get": True,
        "give": True,
    },
    "snakevenom": {
        "name": "snakevenom :snake: :skull: ",
        "description": "venom of snake\nsellable",
        "cost": "Not purchasable",
        "sellcost": 35,
        "tradevalue": 65,
        "get": True,
        "give": True,
    },
    "anktoken": {
        "name": "anktoken :crab:",
        "cost": "Not purchasable",
        "sellcost": "Not sellable",
        "description": " ¯\_(ツ)_/¯",
        "tradevalue": 100,
        "get": True,
        "give": True,
    },
    "yogotrophy": {
        "name": "yogotrophy :trophy:",
        "cost": "not buyable",
        "sellcost": "not sellable",
        "description": " ¯\_(ツ)_/¯",
        "tradevalue": 100,
        "get": True,
        "give": True,
    },
    "yourselfcoin": {
        "name": "yourselfcoin :cow2: ",
        "cost": "cant buy",
        "sellcost": "cant sell",
        "description": " ¯\_(ツ)_/¯",
        "tradevalue": 100,
        "get": True,
        "give": True,
    },
    # Lootboxes
    "smallbox": {
        "name": "smallbox :package:",
        "description": "eat this box for items",
        "cost": "can't buy",
        "sellcost": 25,
        "tradevalue": 50,
        "loottable": {
            "pebble": [50, 1, 10, 2],
            "grass": [50, 1, 10, 2],
            "gem": [2, 1, 2, 2],
            "rarecoin": [5, 1, 5, 3],
            "cheese": [35, 1, 10, 3],
            "cactus": [35, 1, 10, 3],
            "grassseeds": [50, 1, 10, 2],
            "fart": [10, 1, 5, 3],
            "cornseeds": [50, 1, 10, 2],
            "uncommonbox": [15, 1, 1, 1],
        },
        "amount": [1, 3, 2],
        "money": [5, 15, 2],
        "give": True,
    },
    "uncommonbox": {
        "name": "uncommonbox <:uncommon:836784385307050014>",
        "cost": "can't buy",
        "description": "eat this box for good items",
        "sellcost": 100,
        "tradevalue": 50,
        "loottable": {
            "pebble": [50, 1, 10, 2],
            "grass": [50, 1, 10, 2],
            "gem": [5, 1, 2, 2],
            "rarecoin": [8, 1, 5, 3],
            "cheese": [40, 1, 10, 2],
            "cactus": [40, 1, 10, 2],
            "grassseeds": [50, 1, 10, 2],
            "fart": [15, 1, 5, 3],
            "cornseeds": [50, 1, 10, 2],
            "smallbox": [25, 1, 2, 2],
            "epicbox": [10, 1, 1, 1],
            "dragonegg": [2, 1, 1, 1],
            "cow": [40, 1, 5, 3],
        },
        "amount": [1, 5, 2],
        "money": [50, 100, 2],
        "give": True,
    },
    "epicbox": {
        "name": "epicbox <:epic:839130060509937704>",
        "cost": "can't buy",
        "description": "eat this box for op items",
        "sellcost": 500,
        "tradevalue": 250,
        "loottable": {
            "gem": [8, 1, 5, 4],
            "rarecoin": [10, 1, 5, 3],
            "cheese": [40, 1, 10, 3],
            "cactus": [40, 1, 10, 3],
            "fart": [15, 1, 5, 3],
            "smallbox": [15, 2, 3, 3],
            "uncommonbox": [25, 1, 2, 3],
            "dragonegg": [5, 1, 2, 2],
            "gamingpc": [2, 1, 1, 1],
        },
        "amount": [2, 5, 2],
        "money": [100, 250, 2],
        "give": True,
    },
    # Unobtainable withut dev
    "bug": {
        "name": "bug :bug:",
        "cost": "can't buy",
        "description": "Given to people who reported a somewhat bad bug",
        "give": True,
        "get": True,
        "sellcost": "not sellable",
        "tradevalue": 100,
    },
}

locations = {
    "default": {
        "name": "default ",
        "desc": "You start here.",
        "baseMulti": 1,
        "shop": {},
        "cost": 1000000,
        "multis": {},
        "defaultLife": True,
        "lifeOverrides": {},
        "deathRate": 0,
    },
    "desert": {
        "name": "desert :desert:",

        "desc": "A hot tundra without much, home to camels and cacti and sand",
        "baseMulti": 1.05,

        "shop": {
            "camel": {"cost": 775, "give": False},
            "cameldung": {"cost": 75, "give": False, "get": False},
            "cactusseeds": {"cost": 20, "sellcost": 19},
            "cactus": {"cost": 27, "sellcost": 24},
        },

        "cost": 500000,
        "multis": {"camel": 1.5, "sunflower": 1.1, "snake": 1.5, "cactus": 2, 'sheep': 0.9, 'cow': 0.9},

        "defaultLife": False,
        "lifeOverrides": {
            "camel": True,
            "sunflower": True,
            "snake": True,
            "cactus": True,
        },

        "deathRate": 0.75,
    },
    "jungle": {
        "name": "jungle :coconut:",
        "desc": "A thick, rainy forest",
        "baseMulti": 1.2,
        "shop": {
					'peacock': {'cost': 350}
				},
        "cost": 850000,
        "multis": {
            "mango": 1.75,
						'peacock': 1.25
        },
        "defaultLife": True,
        "lifeOverrides": {"cactus": False, "camel": False},
        "deathRate": 0.85,
    },
    'arctic': {
        'name': 'arctic :snowflake: ',
        'desc': 'A cold, dumb, cold, snow, cold place where walruses and stuff live',
        'baseMulti': 1.25,
				'shop' :{
					'walrus': {'cost': 700}
				},
				'cost': 1500000,
				'multis': {
					'sheep': 1.1,
					'chicken': 0.9,
					'sunflower': 0.9,
					'mango': 0.9,
					'walrus': 1.25
				},
				'defaultLife': True,
				'lifeOverrides': {},
				'deathrate': 0.8
    },
    "devlocation": {
        "name": "devlocation :test_tube:",
        "desc": "Only for the devs",
        "baseMulti": 69,
        "shop": {"xlorx": {"cost": 1, "sellcost": 9999999999}},
        "cost": "unbuyable",
        "multis": {},
        "defaultLife": True,
        "lifeOverrides": {},
        "deathRate": 0,
    },
}
# "": { # Location name, self-explanatory

# 	"name": "", # displayed name
# 	"desc": "", #description
# 	"baseMulti": 1, # the multi for everything that isn't in the multis key
# 	"shop": {}, # differences in the shop
# 	"cost": 0, # cost to buy
# 	"multis": {}, # multiplier overrides
# 	"defaultLife": True, # whether or not this location will keep animals/plants alive by default
# 	"lifeOverrides": {}, # life overrides
# 	"deathRate": 0 # amount that will die if stated in lifeOverrides or if defaultLife is False. deadAmount = userAmount * deathRate

# },

tradeexclusive = {}

eatable = [i for i, j in merch.items() if "loottable" in j]

eatable.extend(["applepie", "mango", "ginseng", "mushroom", "cake", "pridewatermelon"])

bal = [
	"better grind for more before you can compare with me idiot",
	"POOR",
	"you stinky little sewage rat",
	"u big dumdum",
	"you dumb diaperwearer",
	"you big fat fart",
	"you boogerfarter",
	"you babbonhater",
	"you baconwearer",
	'you baboonseer',
	'you birdwatcher',
	'you toileter',
	'you pant farter'
	"fat",
	'cacar',
	'ehee',
	'BONG BONG BONG THIS IS MY SONG',
	'DANG it MAN, i didnt even ANTICIPATE that move',
	'friday night in the sunlight bing bang bong',
	'saturday morning in the moonlight ning nang nong',
	"NERD",
	"oversimplification",
	"nerds are nerds, go eat some useless stone-filled birds",
	"ryanbutt",
	"still less than me, gotta grind for more first dumum",
	"omg ur so fat go exercise ewww",
	"bung bung bung bung bung bung bung bung bung",
	"cOW",
	"( ͡° ͜ʖ ͡°)",
	"yogogiddap",
	"!@#$%#%&*(&)*",
	"`-`",
	"~_~",
	"[][][][][]",
	"dee dee doo doo der dee doo",
	"fafart",
	"kekw",
	"mall tycoon roblox player",
	":notes: elevator music plays :notes:",
	"https://www.youtube.com/watch?v=AXrHbrMrun0",
	"you gambler mambler",
	"mar mar marino papido appeal",
	"<< MONEY MONEY GO ROB",
	"babbons",
	"(cents)",
	"buttsmeller",
	"cow seeer",
	"ungbridge",
	"ocker",
	"step on a crack",
	"cameldung",
	"Yourself was here",
	"https://www.youtube.com/watch?v=o_LskiXQ73c",
	'ima call u hua'
]

tips = [
    "Admins, use `setchannel` to set a system messages channel for your server.",
    "Do `donate` to get rep fast",
    "You can use `profile` to see things like when your farm started, and how many commands you've used.",
    "come join our support server at `discord.gg/tvCmtkBAkc`",
    "encounter a bug while playing? use `report` to report it directly to our support server.",

    "do `suggest` to suggest anything from new animals to new tips!",

    "`showtrades` can show currently available trades.",
    "You may be tempted to sell all your merchandise right away, but you should save some to do trades.",
    "`crops` is a handy command to show all the things currently planted and how long they've been growing.",
    "mar mar marino papido appeal",
    "do `trade (trade number)` to do trades.",
    "use the name of the animal for its command, ie. `sheep` and `cow`",
    "`help (command)` to get help about a specific command",
    "trades update every 6 hours",
    "we have a lottery!??!",
    "farmout used to be really really really bad",
    "the creator of farmout made some really weird things like heavenheck bot, which is on display in the support server, before he made farmout",
    "`contracts show` will show you some contracts that you can sign for items",
    "eating your ginseng fruit can give you items",
]

dailys = [
    "from going outside and smelling stuff",
    "by farting 2 times in a row",
    "by begging yogogiddap for money",
    "by working at macdunnerds",
    "by working as a cop",
    "by working as a garbage smeller",
    "by robbing old ladies",
    "by gambling",
    "by watching ads for 2 hours",
    "by sniffing",
    "by tasting concrete",
    "by testing pepper spray",
    "by *deception*",
    "from farting",
    "from perparra",
    "from HACKS",
    "from working as a doctor",
    "from pretending to be a doctor",
    "from working as a dentist",
    "from stealing people's teeth",
    "from asdfhbjlkasfd",
    "from rewriting the alphabet",
    "from joining the nhl",
    "from farming pumpkins for 48 years straight",
    "from streaming video games",
    "from scamming people",
    "from working as a teacher",
    "from working as a chef",
    "from working as a rhino watcher",
    "from working as a potato man",
    "from working as a music artist",
    "from stealing the neighbour's wallet",
    "from having big farts at the big fat mart",
    "by taking care of babbons for a day",
    "by dumming",
    "by sitting in elevators humming music to people because the speakers broke",
    "by working as a janitor at bear's waterpark",
    "by being a statbot",
    "for counting blades of grass",
    "for washing the road",
    "for smelling flowers",
    "for wiping grease off of cars",
    "for seeing a cow",
    "for using double quotation marks instead of single quotation marks",
]

deaths = {
    "from a wildfire": "water",
    "from starvation": "food",
    "from farting twice in a row": "unfart",
    "from gambling and getting negative coins": "moneymoney",
    "from hypothermia": "hothothot",
    "from dehydration": "driiink",
    "from old age": "boing",
    "by getting eaten by dinos": "shoo!",
    "from falling on slippery ice": "unslip",
    "from smelling smelly smells": "noseplug",
    "from suffocation": "mask",
    "from drowning": "airairair",
    "from eating too much": "digestion",
    "by snorkeling on land": "water",
    "from trying to code javascript": "python",
    "from watching bad ytbers": "unsee",
    "because they didn't join farmout support": "joinjoin",
    "from playing fortnite": "minecraft",
    "from the E": "a",
    "from playing hide-and-seek in the scp containment place": "runnnnn",
    "from perparra": "derdarra",
    "from trying to plot against yogogiddap": "join the yogo cult. if not, donations please",
    "using single quotation marks": '""""',
    "from not having ++": "js > py",
}

market = [
    "in the bathroom",
    "eating lunch",
    "too busy watching yt",
    "farting",
    "robbing the monkey men",
    "playing chess",
    "pooping",
    "gone",
    "gone",
    "gambling",
    "trying to run to Mars and back in a day",
    "trying to code",
    "in school",
    "away ig idk",
    "too busy marsjssjgadfni",
    "playing fortnite",
    "trying to lose weight",
]

births = ["baby", "breed", "yes", "shoo!", "fart", "babbon", "push"]

emojis = [
    ":money_with_wings:",
    ":dollar:",
    ":euro:",
    ":yen:",
    ":pound:",
    ":coin:",
    ":moneybag:",
    ":credit_card:",
    ":gem:",
]

def newUser(datemade):
    newuser = {
        "animals": {},
        "tools": {"wateringcan": tools["wateringcan"]["durability"]},
        "merch": {},
        "seeds": {"grassseeds": {"amount": 5}},
        "plantcooldowns": {},
        "plants": {},
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
        "settings": {"votedm": True, "tips": True, "replypings": True},
    }

    return newuser

builtintrades = {
	'1': [
		{
		'give': [
			[
				{
        "name": "wool :cloud:",
        "description": "its from sheep, keep it away from dirt cuz it can get dirty easily",
        "cost": "Not buyable",
        "sellcost": 15,
        "tradevalue": 14,
        "get": True,
    		},
				1,
				'wool'
			]
		],
		'get': [
			[
				{
				'name': 'shirt :shirt: ',
				'description': 'not wearable (yet)',
				'cost': 15,
				'sellcost': 13,
				'tradevalue': 15
				},
				1,
				'shirt'
			]
		]
	},
	{
		'give': [
			[
				{
					"name": "apple :apple:",
					"description": "apples from the apple tree, sell it",
					"cost": 19,
					"sellcost": 17,
					"tradevalue": 16,
					"get": True,
				},
				3,
				'apple'
			],
			[
				{
					"name": "apple :apple:",
					"description": "apples from the apple tree, sell it",
					"cost": 19,
					"sellcost": 17,
					"tradevalue": 16,
					"get": True,
				},
				1,
				'flatbread'
			]
		],
		'get': [
			[
				{
					"name": "applepie :apple: :pie:",
					"description": "eatable, might taste good idk",
					"cost": 25,
					"sellcost": 19,
					"tradevalue": 19,
				},
				1,
				'applepie'
			]
		]
	}
	],
	'2': {
		'give': [
			[
				{
        "name": "milk :milk:",
        "description": "milk, you can sell it or trade it",
        "cost": "Not buyable",
        "sellcost": 21,
        "tradevalue": 20,
        "get": True,
				},
				5,
				'milk'
			]
		],
		'get': [
			[
				{
        "name": "cheese :cheese:",
        "cost": 11,
        "description": "cheese, collectible",
        "sellcost": 9,
        "tradevalue": 8,
				},
				8,
				'cheese'
			]
		]
	},
	'3': {
		'give': [
			[
				{
					"name": "computer :computer:",
					"cost": 1000,
					"description": "it can compute, but only when it wants to\ncollectible, trade it with people",
					"sellcost": "Not sellable",
					"tradevalue": 875,
				},
				1,
				'computer',
			],
			[
				{
					"name": "keyboard :keyboard:",
					"cost": 20,
					"description": "can't actually type\ntradeable",
					"sellcost": 18,
					"tradevalue": 17,
				},
				1,
				'keyboard'
			],
		],
		'get': [
			[
				{
					"name": "gamingpc :video_game:",
					"description": "game on it or smth but you can't actually\nnot sellable",
					"cost": 5000,
					"sellcost": "Not sellable",
					"tradevalue": 4500,
				},
				1,
				'gamingpc'
			]
		]
	}
}