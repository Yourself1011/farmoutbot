import discord
from json import loads
from os import environ

async def fixed(message, client):
	args = message.content.split(' ')
	if len(args) == 2:
		await message.channel.send('what are you fixing lol')
		return
	link = args[2]
	if message.author.id not in [690577156006477875, 690575294674894879,697094970842021969, 764900173431832576, 697089328668737566] and not environ.get("ENV") == "dev": 
		await message.channel.send('be a dev')
		return
	#try:
	link = link.split('/')
	msg_id = int(link[5])
	channel = await client.fetch_channel(806178919409254450)
	msg = await channel.fetch_message(msg_id)
	#except:
	#	await message.channel.send('uhhhh thats not a message????')
	#	return
	
	if msg.author != client.user:
		await message.channel.send("gotta be a message sent by me")
		return
	args2 = message.content.split("has")
	args2[0].replace(" ", '')
	name = args2[0]
	name = name.split("#")
	userid = discord.utils.get(client.get_all_members(), name = name[0], discriminator=name[1]).id
	reason = message.content.split('[Farmout]')[1]
	await userid.send(f'your bug report for \n"{reason}"\n has been fixed.')
	old = msg.content
	await msg.edit(f'~~{old}~~\n**FIXED**')