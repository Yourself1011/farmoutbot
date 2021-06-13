commands = {
	'help': {
		'name': 'help',
		'usage': '<help> shows all commands | <help (command)> shows help about that command',
		'description': 'Helps you about a command or shows all commands',
		'aliases': ['commands', 'hp'],
		'category': 'misc'
	},
	'ping': {
		'name': 'ping',
		'usage': '<ping>',
		'description': 'Shows bot latency or ping',
		'aliases': ['latency', 'pi'],
		'category': 'misc'
	},
	'prefix': {
		'name': 'prefix',
		'usage': '<prefix>',
		'description': 'Shows prefix for current server',
		'aliases': ['px'],
		'category': 'misc'
	},
	'changeprefix': {
		'name': 'changeprefix',
		'usage': '<changeprefix (new prefix)>',
		'description': 'Changes prefix for current server',
		'aliases': ['cpx'],
		'category': 'utility'
	},
	'fart': {
		'name': 'fart',
		'usage': '<fart>',
		'description': 'farts',
		'aliases': ['flatulence', 'farts', 'poop'],
		'category': 'other'
	},
	'start': {
		'name': 'start',
		'usage': '<start>',
		'description': 'Starts your journey in Farmout',
		'aliases': ['create', 'createaccount'],
		'category': 'game'
	},
	'inventory': {
		'name': 'inventory',
		'usage': '<inventory> <@user>',
		'description': 'Shows the inventory of you or the person you mentioned',
		'aliases': ['inv', 'iv'],
		'category': 'profile'
	},
	'balance': {
		'name': 'balance',
		'usage': '<balance> <@user>',
		'description': 'Shows the balance (or coins) of you or the person you mentioned',
		'aliases': ['money', 'coins', 'wallet', 'bal', 'bl', 'bank'],
		'category': 'profile'
	},
	'profile': {
		'name': 'profile',
		'usage': '<profile> <@user>',
		'description': 'Shows your profile of you or the person you mentioned',
		'aliases': ['prof', 'pf'],
		'category': 'profile'
	},
	'end': {
		'name': 'end',
		'usage': '<end>',
		'description': 'Ends, duh',
		'aliases': [],
		'category': 'game'
	},
	'shop': {
		'name': 'shop',
		'usage': '<shop> <animals | tools | seeds | merch>',
		'description': 'Shows shop, duh',
		'aliases': ['sp'],
		'category': 'market'
	},
	'dank': {
		'name': 'dank',
		'usage': '<dank>',
		'description': 'Dank',
		'aliases': ['dk'],
		'category': 'other'
	},
	'daily': {
		'name': 'daily',
		'usage': '<daily>',
		'desciption': 'Gives you your daily coins if the market likes you',
		'aliases': ['day'],
		'category': 'game'
	},
	'hourly': {
		'name': 'hourly',
		'usage': '<hourly>',
		'description': 'Gives you your hourly coins if the market likes you',
		'aliases': ['hour'],
		'category': 'game'
	},
	'buy': {
		'name': 'buy',
		'usage': '<buy> <thingbought> <amount(integer) | all | a | max>',
		'description': 'Buys something from the market if you have sufficient funds and rep',
		'aliases': [],
		'category': 'market'
	},
	'air' :{
		'name': 'air',
		'usage': '<air>',
		'description': 'Air',
		'aliases': ['air'],
		'category': 'other',
	},
	'sell': {
		'name': 'sell',
		'usage': '<sell> <thingsold> <amount(integer) | all | a | max>',
		'description': 'Sells something you own to the market if they like you enough',
		'aliases': [],
		'category': 'market'
	},
	'donate': {
		'name': 'donate',
		'usage': '<donate> <amount(integer)>',	
		'description': 'Donates coins to the marketplace while increasing your reputation',
		'aliases': ['dt'],
		'category': 'market'
	},
	'credits': {
		'name': 'credits',
		'usage': '<credits>',
		'description': 'Shows bot credits',
		'aliases': ['cr'],
		'category': 'other'
	},
	'invite': {
		'name': 'invite',
		'usage': '<invite>',
		'description': 'Invites the bot to your server',
		'aliases': ['it'],
		'category': 'misc'
	},
	'slots': {
		'name': 'slots',
		'usage': '<slots> <amount(integer) | a | all | max>',
		'description': 'Bet your money with this slots game',
		'aliases': ['sl'],
		'category': 'gamble',
	},
	'reputation': {
		'name': 'reputation',
		'usage': '<reputation>',
		'description': "Shows your reputation and info about rep",
		'aliases': ['rep'],
		'category': 'market'
	},
	'share': {
		'name': "share",
		'usage': '<share> <amount(integer) | all | a | max> <@user>',
		'description': 'Gives coins to people',
		'aliases': ['give'],
		'category': 'game'
	},
	'plant': {
		'name': 'plant',
		'usage': '<plant> <thingplanted> <amount(integer) | a | all | max>',
		'description': 'Plants stuff idk',
		'aliases': ['pl'],
		'category': 'farming'
	},
	'collect': {
		'name': 'collect',
		'usage': '<collect> <thingcollected>',
		'description': 'Collects planted plants',
		'aliases': ['col'],
		'category': 'farming'
	}, 
	'suggest': {
		'name': 'suggest',
		'usage': '<suggest> <suggestion>',
		'description': 'Suggests stuff for Farmout, no joke suggestions',
		'aliases': ['suggestion'],
		'category': 'utility'
	},
	'reply': {
		'name': 'reply',
		'usage': '<reply>',
		'description': 'Replies',
		'aliases': [],
		'category': 'other'
	},
	'report': {
		'name': 'report',
		'usage': "<report> <description> <image link>",
		'description': 'Report bugs',
		'aliases': [],
		'category': 'utility'
	},
	'trade': {
		'name': 'trade',
		'usage': '<trade> <trade number>',
		'description': 'trades stuff',
		'aliases': ['td'],
		'category': 'market'
	},
	'listtrades': {
		'name': 'listtrades',
		'description': 'Shows trades',
		'usage': '<listtrades>',
		'aliases': ['showtrades', 'tradeoffers', 'st', "lt"],
		'category': 'market'
	},
	'channel': {
		'name': 'channel',
		'usage': "<channel>",
		'description': 'Shows the current system messages channel',
		'aliases': ['cl'],
		'category': 'misc'
	},
	'setchannel': {
		'name': 'setchannel',
		'usage': '<setchannel> <new channel>',
		'description': 'Sets the current system messages channel to a new one',
		'aliases': ['scl'],
		'category': 'utility'
	},
	'gift': {
		'name': 'gift',
		'usage': '<gift> <@user> <item> <amount>',
		'description': 'Gifts stuff',
		'aliases': ['gf'],
		'category': 'game'
	},
	'dice': {
		'name': 'dice',
		'usage': '<dice> <amount(integer) | a | all | max>',
		'description': 'Gamble your coins in this dice game!',
		'aliases': ['gamble', 'bet'],
		'category': 'gamble'
	},
	'randomnumber': {
		'name': 'randomnumber',
		'usage': '<randomnumber> <number>',
		'description': 'Pick a random number from 1-20 and have a chance to win some coins.', 
		'aliases': ['rn'],
		'category': 'gamble'
	},
	'crops': {
		'name': 'crops',
		'usage': '<crops>',
		'description': 'Shows currently planted crops',
		'aliases': ['field', 'garden', 'cs'],
		'category': 'farming'
	},
	'beg': {
		'name': 'beg',
		'usage': '<beg>',
		'description': 'Begs for money, while taking away your rep',
		'aliases': [],
		'category': 'game'
	},
	"blackjack": {
		"name": "blackjack",
		"usage": "blackjack",
		"description": "An authentic blackjack experience",
		"aliases": ["bj"],
		"category": "gamble"
	},
	"devmode": {
		"name": "devmode",
		"usage": "devmode <update|toggle|on|off|check>",
		"description": "Only for the dev to get infinite everything for testing purposes",
		"aliases": [],
		"category": "misc"
	},
	"top": {
		"name": "top",
		"usage": "top",
		"description": "Shows the richest users in a server",
		"aliases": ["leaderboard", "lb"],
		"category": "profile"
	},
	"gibberish": {
		"name": "gibberish",
		"usage": "gibberish <sentence>",
		"description": "makes a sentence gibberish, yet readable",
		"aliases": ["gibberize", "gibber", "scramble"],
		"category": "other"
	},
	"forest": {
		"name": "forest",
		"usage": "forest",
		"description": "What will you find in the forest?",
		"aliases": ["ft"],
		"category": "gather"
	},
	'rules': {
		'name': 'rules',
		'usage': 'rules',
		'description': 'Shows farmout rules',
		'aliases': ['rs'],
		'category': 'misc'
	},
	'lottery': {
		'name': 'lottery',
		'usage': 'lottery <view>',
		'description': 'Enter in the farmout lottery, winners every 6 hours or smth',
		'aliases': ['lo'],
		'category': 'game'
	},
	'contract': {
		'name': 'contract',
		'usage': '<contract> <show, sign (contract number), complete, current>',
		'description': 'Sign some contracts or quests with other farms and the marketplace.\nShow: shows all contracts\nSign: signs a contract\nComplete: completes your currently signed contract\nCurrent: view your currently signed contract',
		'aliases':['co'],
		'category': 'market'
	},
	'eat': {
		'name': 'eat',
		'usage': 'eat some stuff',
		'aliases': [],
		'category': 'game'
	},
	"location": {
		"name": "location",
		"usage": "location <my|view [page]|buy <location> ['liquidate']|transfer [animals] <location>>",
		"description": "Looks at locations",
		"aliases": ["lc", "loc", "locations"],
		"category": "game"
	},
	'beach': {
		'name': 'beach',
		'usage': '<beach>',
		'description': 'go look in the beach for some cool stuff',
		'aliases': ['bea'],
		'category': 'gather'
	},
	"settings": {
		"name": "settings",
		"usage": "settings [setting [value]]",
		"description": "Look at your current settings or change a setting.",
		"aliases": ["set", "config"],
		"category": "utility"
	},
	'sitdown':{
		'name':'sitdown',
		'usage': '<sitdown>',
		'description': 'SIDDOWN',
		'aliases': [],
		'category': 'other'
	},
	'zoo': {
		'name': 'zoo',
		'usage': '<zoo>',
		'description': 'what weird and unusual events will occur at the zoo?',
		'aliases':[],
		'category': 'other'
	},
	'vote': {
		'name': 'vote',
		'usage': '<vote>',
		'description': 'pls vote so i can get more players',
		'aliases':[],
		'category': 'misc'
	},
	'sigh': {
		'name': 'sigh',
		'usage': '<sigh>',
		'description': 'what will happen when you sigh?',
		'aliases':['sighuh', 'sihg'],
		'category': 'other'
	},
	'onthefence': {
		'name': 'onthefence',
		'usage': '<otf (bet)>',
		'description': 'On the fence is a gambling game. In it, you have a "score". The higher the score, the more likely you win coins. The lower the score, the less likely. If you lose, your score is more likely to go up. If you win, your score is more likely to go down. The trick is to bet more when you have a higher score, and bet less when you have a lower score. If your score is 0, you are "on the fence", and have a 50/50 chance of winning coins.',
		'aliases': ['otf'],
		'category': 'gamble'
	},
	'beetlerace': {
		'name': 'beetlerace',
		'usage': '<beetlerace (beetlenumber 1-5) (bet)',
		'description': 'Bet on a beetle to win the beetle race. There are 5 total beetles. If your beetle gets 1st, you win 3 times the amount. If it gets 2nd, you win twice the amount. If it gets 3rd, nothing happens, and if it gets 4th or 5th, you lose all of your coins.',
		'aliases': ['br'],
		'category': 'gamble'
	},
	'jungle': {
		'name': 'jungle',
		'usage': '<jungle>',
		'description': 'go gather some valuables in the jungle',
		'aliases': ['jg'],
		'category': 'gather'
	},
	'guide': {
		'name': 'guide',
		'usage': '<guide> <thingguided>',
		'description': 'Get a more in-depth tutorial on the features of farmout',
		'aliases': ['gd', 'tutorial'],
		'category': 'misc'
	}
}

# "": {
# 	"name": "",
# 	"usage": "",
# 	"description": "",
# 	"aliases": [],
# 	"category": ""
# },