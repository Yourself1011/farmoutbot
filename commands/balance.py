from replit import db
import random
from zstats import getMember

async def balance(message, client):
	args = message.content.split(' ')
	if len(args) == 2 and str(message.author.id) not in db['members']:
		await message.channel.send('Make an account first to get money idiot')
		return
	if len(args) == 3 and not args[2].startswith('<@') and args[2].endswith('>'):
		await message.channel.send('Mention someone to see their account')
		return
	if len(args) == 2:
		user = str(message.author.id)
	if len(args) >= 3:
		searched = getMember(args[2:], message.guild.id, client)
		user = str(searched.id) if searched else False

	if not bool(user):
		return ("I couldn't find anybody")
	if user not in db['members']:
		return (f'Get {searched.name}#{searched.discriminator} to make an account')
		return
	money = db['members'][user]['money']
	things = ['better grind for more before you can compare with me idiot', 'POOR', 'you stinky little sewage rat', 'u big dumdum', 'you dumb diaperwearer', 'you big fat fart', 'you boogerfarter', 'you babbonhater', 'you baconwearer', 'fat', 'NERD', 'oversimplification', 'nerds are nerds, go eat some useless stone-filled birds', 'ryanbutt', 'still less than me, gotta grind for more first dumum', 'omg ur so fat go exercise ewww', 'bung bung bung bung bung bung bung bung bung', 'cOW', '( ͡° ͜ʖ ͡°)', 'yogogiddap', '!@#$%#%&*(&)*', '`-`', '~_~', '[][][][][]', 'dee dee doo doo der dee doo', 'fafart', 'kekw', 'mall tycoon roblox player', ':notes: elevator music plays :notes:', 'https://www.youtube.com/watch?v=AXrHbrMrun0', 'you gambler mambler', 'mar mar marino papido appeal', '<< MONEY MONEY GO ROB', 'babbons', '(cents)', 'buttsmeller', 'cow seeer', 'ungbridge', 'ocker', 'step on a crack', 'cameldung', "Yourself was here", "https://www.youtube.com/watch?v=o_LskiXQ73c"]	
	thing = random.choice(things)
	name = await client.fetch_user(user)
	return (f'{name} has `{money}` coins, {thing}', True)