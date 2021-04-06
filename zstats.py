from random import uniform, randint
from math import floor

def getMember(search, guildId, client):
	if type(search) is list:
		search = " ".join(search)
	id = search.translate({ord(x): "" for x in ["<", "@", "!", ">"]})
	guild = client.get_guild(guildId)
	out = guild.get_member(int(id)) if id.isnumeric() else False

	if not bool(out):
		possibilities = [i for i in guild.members if search.lower() in f"{i.name.lower()}#{i.discriminator}" or (bool(i.nick) and search.lower() in i.nick)]
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
			out = float(arr[0]) * (10**float(arr[1]))
		elif out[-1] == "k":
			out = float(out[:-1])*1000
		elif out[-1] == "m":
			out = float(out[:-1])*1000000
		elif out[-1] == "b":
			out = float(out[:-1])*1000000000
		elif out[-1] == "t":
			out = float(out[:-1])*1000000000000

		return int(out)
	
	except:
		return None

def gatheringCmd(msg, loottable):
	"""
	Returns an array of the item gathered and the amount, or an array with. Loottable should be an object with keys as the item name, and values as an array of chance (out of total chances), maximum amount, minimum amount (optional, defaults to 1), and weight (defaults to 1).
	"""
	# Gets the item itself
	totalChances = 0
	for i in list(loottable.values()):
		totalChances += i[0]
	chosen = randint(0, totalChances)
	newList = {}
	sum = 0
	for k, v in loottable.items():
		newList[k] = [v[0] + sum] + v[1:]
		sum += v[0]

	itemKey = min({k: v for k, v in newList.items() if v[0] >= chosen}.items(), key = lambda x: x[1][0])[0]
	item = loottable[itemKey]

	# Gets the amount
	p = item[3] if len(item) >= 4 else 1
	minimum = item[2] if len(item) >= 3 else 1
	maximum = item[1]
	amount = floor(minimum + (maximum - minimum) * (uniform(0, 1)**p))
	
	return [itemKey, amount]

animals = {
	'name': 'animals',
	'sheep': {'name': 'sheep :sheep:','cost': 250,'sellcost': 225,'tool': 'shears','result': 'wool','cooldown': 45000,'thing':'shear','tradevalue': 150},
	'cow': {'name': 'cow :cow:','cost': 775,'sellcost': 500,'tool': 'bucket','result': 'milk','cooldown': 30000,'thing': 'milk','tradevalue': 375},
	'babbon': {'name': 'babbon :monkey: ','cost':500,'sellcost':400,'tool':'babboner','result':'kidney','cooldown':30000,'thing':'babbon','tradevalue':250},
	'chicken': {
		'name': 'chicken :chicken:',
		'cost': 75,
		'sellcost': 50,
		'tool': 'nest',
		'result': 'egg',
		'cooldown': 30000,
		'tradevalue': 100,
		'thing': 'collect'
	},
	'goat': {
		'name': 'goat :goat:',
		'cost': 275,
		'sellcost': 125,
		'tool': 'bowl',
		'result': 'goatsmilk',
		'cooldown': 40000,
		'tradevalue': 200,
		'thing': 'milk'
	},
	'horse': {
		'name': 'horse :horse:',
		'cost': 1250,
		'sellcost': 650,
		'tool': 'saddle',
		'result': 'horsehair',
		'cooldown': 27000,
		'tradevalue': 400,
		'thing': 'haired'
	},

	# Exotic animals

	'camel': {'name': 'camel :dromedary_camel:','cost': "Only obtainable through trading",'sellcost': 500,'tool': 'toilet','result': 'cameldung','cooldown': 50000,'thing': 'milk','tradevalue': 350, "give": True},
	'snake': {'name': 'snake :snake:','cost':'Only obtainable through trading','sellcost':350,'tool':'venomextractor','result':'snakevenom','cooldown':60000,'thing':'extract venom','tradevalue':200,'give':True}
}

tools = {
	'name': 'tools',
	'shears': {
		'name': 'shears',
		'cost': 10,
		'durability': 10,
		'sellcost': 9,
		'animal': 'sheep',
		'tradevalue': 5 
	},
	'steelshears' :{
		'name': 'steelshears',
		'cost': 30,
		'sellcost': 25,
		'durability': 50,
		'animal': 'sheep',
		'tradevalue': 15
	},
	'wateringcan': {
		'name': 'wateringcan',
		'cost': 25,
		'durability': 35,
		'sellcost': 9,
		'animal': 'seed',
		'tradevalue': 5
	},
	'babboner': {
		'name': 'babboner',
		'cost': 25,
		'durability':30,
		'sellcost':10,
		'animal':'babbon',
		'tradevalue':4
	},
	'bettercan': {
		'name': 'bettercan',
		'cost': 50,
		'durability': 100,
		'sellcost': 45,
		'animal': 'seed',
		'tradevalue': 20
	},
	'hose': {
		'name': 'hose',
		'cost': 200,
		'durability': 375,
		'sellcost': 175,
		'animal': 'seed',
		'tradevalue': 50
	},
	'sprinkler': {
		'name': 'sprinkler',
		'cost': 500,
		'durability': 689,
		'sellcost': 450,
		'animal': 'seed',
		'tradevalue': 85
	},
	'bucket': {
		'name': 'bucket',
		'cost': 50,
		'durability': 50,
		'sellcost': 45,
		'animal': 'cow',
		'tradevalue': 15
	},
	'saddle': {
		'name': 'saddle',
		'cost': 30,
		'durability': 30,
		'sellcost': 20,
		'animal': 'horse',
		'tradevalue': 13
	},
	'steelbucket': {
		'name': 'steelbucket',
		'cost': 150,
		'durability': 150,
		'sellcost': 135,
		'animal': 'cow',
		'tradevalue': 40
	},
	'bowl': {
		'name': 'bowl',
		'cost': 30,
		'durability': 50,
		'sellcost': 27,
		'animal': 'goat',
		'tradevalue': 10
	},
	'toilet': {
		'name': 'toilet',
		'cost':50,
		'durability':50,
		'sellcost':40,
		'animal':'camel',
		'tradevalue':17
	},
	'megacoop': {
		'name': 'megacoop',
		'cost':	100,
		'durability':150,
		'sellcost':75,
		'animal':'chicken',
		'tradevalue':40
	},
	'bigbowl': {
		'name': 'bigbowl',
		'cost':50,
		'durability':75,
		'sellcost':45,
		'animal': 'goat',
		'tradevalue':21
	},
	'venomextractor': {
		'name': 'venomextractor',
		'cost': 30,
		'durability':40,
		'sellcost':25,
		'animal':'snake',
		'tradevalue': 10
	},
	'nest': {
		'name': "nest",
		'cost': 10,
		'durability': 15,
		'sellcost': 9,
		'animal': 'chicken',
		'tradevalue': 5
	},
	'chickenhouse': {
		'name': 'chickenhouse',
		'cost': 30,
		'durability': 48,
		'sellcost': 27,
		'animal': 'chicken',
		'tradevalue': 9
	},
	'hikingboots': {
		'name': 'hikingboots',
		'cost': 50,
		'durability': 25,
		'sellcost': 27,
		'animal': 'forest',
		'tradevalue': 9
	}
}

seeds = {
	'name': 'seeds',

	# Normal seeds

	'grassseeds': {
		'name': 'grassseeds',
		'cost': 5,
		'sellcost': 4,
		'growtime': 30000,
		'result': 'grass',
		'tradevalue': 1
	},
	'cornseeds': {
		'name': 'cornseeds',
		'cost': 13,
		'sellcost': 12,
		'growtime': 33000,
		'result': 'corn',
		'tradevalue': 2
	},
	'strawberryseeds': {
		'name': 'strawberryseeds',
		'cost': 15,
		'sellcost': 14,
		'growtime': 29000,
		'result': 'strawberry',
		'tradevalue': 2
	},
	'mangoseeds': {
		'name': 'mangoseeds',
		'cost': 25,
		'sellcost': 22,
		'growtime': 20000,
		'result': 'mango',
		'tradevalue': 5
	},
	'appleseeds': {
		'name': 'appleseeds',
		'cost': 13,
		'sellcost': 12,
		"stages": [1800000, 3600000, 86400000],
		'result': 'apple',
		'tradevalue': 2,
		"amount": [10, 15]
	 },

	# Seasonal seeds

	'pumpkinseeds': {
		'name': 'pumpkinseeds',
		'cost': "Only available during fall", # 20,
		'sellcost': 19, 
		'growtime': 40000,
		'result': 'pumpkin',
		'tradevalue': 5,
		"get": True,
		"give": True
	},
	'tulipseeds': {
		'name': 'tulipseeds',
		'cost': 15, # "Only available during spring",
		'sellcost': 13,
		'growtime': 40000,
		'result': 'tulip',
		'tradevalue': 5,
		"get": False,
		"give": False
	},
	'sunflowerseeds': {
		'name': 'sunflowerseeds',
		'cost': "Only available during summer", # 20,
		'sellcost': 19,
		'growtime': 40000,
		'result': 'sunflower',
		'tradevalue': 5,
		"get": True,
		"give": True
	},
	'pinetreeseeds': {
		'name': 'pinetreeseeds',
		'cost': "Only available during winter", # 100,
		'sellcost': 19,
		'growtime': 3600000,
		'result': 'pinetree',
		'tradevalue': 5,
		"get": True,
		"give": True
	},
}

merch = {
	'name': 'merch',

	# Misc merch

	'gem': {
		'name': 'gem :gem:',
		'cost': 750,
		'sellcost': 'Not sellable',
		'tradevalue': 400,
	},
	'fish': {
		'name': 'fish :fish:',
		'cost': 7,
		'sellcost': 6,
		'tradevalue': 2,
	},
	'fart': {
		'name': 'fart :dash:',
		'cost': 65,
		'sellcost': 50,
		'tradevalue': 50,
	},
	'rarepainting': {
		'name': 'rarepainting :frame_photo: ',
		'cost': 175,
		'sellcost': 'Not sellable',
		'tradevalue': 150,
	},
	'dragonegg': {
		'name': 'dragonegg :dragon_face: :egg: ',
		'cost': 1500,
		'sellcost': 'Not sellable',
		'tradevalue': 750,
	},
	'computer': {
		'name': 'computer :computer:',
		'cost': 1000,
		'sellcost': 'Not sellable',
		'tradevalue': 200,
	},
	'rarecoin': {
		'name' : 'rarecoin :coin: ',
		'cost': 175,
		'sellcost':'Not sellable',
		'tradevalue': 140
	},
	'pebble': {
		'name' : 'pebble :rock:',
		'cost': 5,
		'sellcost':3,
		'tradevalue': 2
	},
	'voldysnose':{
		'name': 'voldysnose :nose:',
		'cost':20,
		'sellcost':'Not sellable',
		'tradevalue':50,
	},
	'croissant': {
		'name': 'croissant :croissant: ',
		'cost': 20,
		'sellcost':'Not sellable',
		'tradevalue':20,
	},
	'gamingpc': {
		'name': 'gamingpc :video_game:',
		'cost':5000,
		'sellcost': 'Not sellable',
		'tradevalue': 450,
	},
	'glasses': {
		'name': 'glasses :eyeglasses:',
		'cost': 20,
		'sellcost':18,
		'tradevalue':5,
	},
	'clock': {
		'name': 'clock :clock1: ',
		'cost': 30,
		'sellcost': 25,
		'tradevalue': 5,
	},

	# Animal merch

	'wool': {
		'name': 'wool :cloud:',
		'cost': 17,
		'sellcost': 15,
		'tradevalue': 5,
		'get': True
	},
	'goatsmilk': {
		'name': 'goatsmilk :goat: :milk:',
		'cost': 21,
		'sellcost': 19,
		'tradevalue': 6,
		'get': True
	},
	'horsehair': {
		'name': 'horsehair :horse: :person_bald:',
		'cost': 21,
		'sellcost': 20,
		'tradevalue': 5,
		'get': True
	},
	'milk': {
		'name': 'milk :milk:',
		'cost': 23,
		'sellcost': 21,
		'tradevalue': 8,
		'get': True
	},
	'cheese': {
		'name': 'cheese :cheese:',
		'cost': 10,
		'sellcost': 9,
		'tradevalue': 3,
	},
	'egg': {
		'name': 'egg :egg:',
		'cost': 14,
		'sellcost': 13,
		'tradevalue': 5,
		'get': True
	},
	'kidney':{'name':'kidney :potato:', 'cost': 21,'sellcost':19,'tradevalue':15},

	# Plant merch

	'grass': {
		'name': 'grass :seedling:',
		'cost': 6,
		'sellcost': 5,
		'tradevalue': 1,
		'get': True
	},
	'mango': {
		'name': 'mango :mango:',
		'cost': 29,
		'sellcost': 26,
		'tradevalue': 5,
		'get': True
	},
	'apple': {
		'name': 'apple :apple:',
		'cost': 19,
		'sellcost': 17,
		'tradevalue': 2,
		'get': True
	},
	'corn': {
		'name': 'corn :corn:',
		'cost': 19,
		'sellcost': 17,
		'tradevalue': 3,
		'get': True
	},
	'strawberry': {
		'name': 'strawberry :strawberry:',
		'cost': 21,
		'sellcost': 19,
		'tradevalue': 3,
		'get': True
	},

	# Gather only merch
	"mushroom": {
		"name": "mushroom :mushroom:",
		"cost": "Cannot be bought",
		"sellcost": 15,
		"tradevalue": 5
	},

	# Seasonal merch

	'pumpkin': {
		'name': 'pumpkin :jack_o_lantern:',
		'cost': "Only available during fall", # 50
		'sellcost': 45,
		'tradevalue': 4,
		'get': True,
		"give": True
	},
	"tulip": {
		"name": "tulip :tulip:",
		"cost": 25, # "Only available during spring",
		"sellcost": 20,
		"tradevalue": 4,
		"get": False,
		"give": False
	},
	'sunflower': {
		'name': 'sunflower :sunflower:',
		'cost': "Only available during summer", # 50
		'sellcost': 45,
		'tradevalue': 4,
		'get': True,
		"give": True
	},
	'pinetree': {
		'name': 'pinetree :evergreen_tree:',
		'cost': "Only available during winter", # 150
		'sellcost': 45,
		'tradevalue': 4,
		'get': True,
		"give": True
	},
	'clover': {
		'name': 'clover :four_leaf_clover: ',
		'cost': 'Only available on St. Patrick\'s day', #10
		'sellcost': 9,
		'tradevalue': 20,
		'get': True,
		'give': True
	},
	'easteregg':{ 
		'name': 'easteregg :egg: :rabbit: ',
		'cost': 10, #Only available from good friday to easter monday
		'sellcost': 9,
		'tradevalue': 15,
		'get': False,
		'give': False
	},

	# Exotic merch

	"cameldung": {
		"name": "cameldung :camel: :poop:",
		"cost": "Not purchasable",
		"sellcost": 50,
		"tradevalue": 100,
		"get": True,
		"give": True
	},
	'snakevenom': {
		'name':'snakevenom :snake: :skull: ',
		'cost': 'Not purchasable',
		'sellcost': 35,
		'tradevalue': 65,
		'get': True,
		'give': True
	},
}

tradeexclusive = {}

tips = ['Admins, use `setchannel` to set a system messages channel for your server.', 'Do `donate` to get rep fast', 'You can use `profile` to see things like when your farm started, and how many commands you\'ve used.', '`trades` will you show you available trades.', 'come join our support server at `discord.gg/tvCmtkBAkc`', 'encounter a bug while playing? use `report` to report it directly to our support server.', 'do `suggest` to suggest anything from new animals to new tips!', '`showtrades` can show currently available trades.', 'You may be tempted to sell all your merchandise right away, but you should save some to do trades.', '`crops` is a handy command to show all the things currently planted and how long they\'ve been growing.', 'mar mar marino papido appeal', 'do `trade (trade number)` to do trades.', 'use the name of the animal for its command, ie. `sheep` and `cow`', '`help (command)` to get help about a specific command', 'trades update every 6 hours']

dailys = ['from going outside and smelling stuff', 'by farting 2 times in a row', 'by begging yogogiddap for money', 'by working at macdunnerds', 'by working as a cop', 'by working as a garbage smeller', 'by robbing old ladies', 'by gambling', 'by watching ads for 2 hours', 'by sniffing', 'by tasting concrete', 'by testing pepper spray', 'by *deception*', 'from farting', 'from perparra', 'from HACKS', 'from working as a doctor', 'from pretending to be a doctor', 'from working as a dentist', 'from stealing people\'s teeth', 'from asdfhbjlkasfd', 'from rewriting the alphabet', 'from joining the nhl', 'from farming pumpkins for 48 years straight', 'from streaming video games', 'from scamming people', 'from working as a teacher', 'from working as a chef', 'from working as a rhino watcher', 'from working as a potato man', 'from working as a music artist', "from stealing the neighbour's wallet", 'from having big farts at the big fat mart', 'by taking care of babbons for a day', 'by dumming', 'by sitting in elevators humming music to people because the speakers broke', 'by working as a janitor at bear\'s waterpark', 'by being a statbot', 'for counting blades of grass', 'for washing the road', 'for smelling flowers', 'for wiping grease off of cars', 'for seeing a cow', "for using double quotation marks instead of single quotation marks"]

deaths = {'from a wildfire': 'water', 'from starvation': 'food', 'from farting twice in a row': 'unfart', 'from gambling and getting negative coins': 'moneymoney', 'from hypothermia': 'hothothot', 'from dehydration': 'driiink', 'from old age': 'boing', 'by getting eaten by dinos': 'shoo!', 'from falling on slippery ice': 'unslip', 'from smelling smelly smells': 'noseplug', 'from suffocation': 'mask', 'from drowning': 'airairair', 'from eating too much': 'digestion', 'by snorkeling on land': 'water', 'from trying to code javascript': 'python', 'from watching bad ytbers': 'unsee', 'because they didn\'t join farmout support': 'joinjoin', 'from playing fortnite': 'minecraft', 'from the E': 'a', 'from playing hide-and-seek in the scp containment place': 'runnnnn', 'from perparra': 'derdarra', 'from trying to plot against yogogiddap': 'join the yogo cult. if not, donations please', "using single quotation marks": "\"\"\"\"", "from not having ++": "js > py"}

market = ['in the bathroom', 'eating lunch', 'too busy watching yt', 'farting', 'robbing the monkey men', 'playing chess', 'pooping', 'gone', 'gone', 'gambling', 'trying to run to Mars and back in a day', 'trying to code', 'in school', 'away ig idk', 'too busy marsjssjgadfni', 'playing fortnite', 'trying to lose weight']

births = ['baby', 'breed', 'yes', 'shoo!', 'fart', 'babbon', "push"]
emojis = [':money_with_wings:', ':dollar:', ':euro:', ':yen:', ':pound:', ':coin:', ':moneybag:', ':credit_card:', ':gem:']