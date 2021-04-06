from random import shuffle

async def gibberish(message, client):
	wordList = message.content.replace("\n", " \n").split(" ")
	wordList.pop(0)
	wordList.pop(0)
	if wordList == []:
		await message.channel.send('mar mar marnio papido appeal')
		return
	out = []
	for i in wordList:
		if len(i) > 3:
			end = -2 if i.endswith((".", ",", "!", "?", ":")) else -1
			shuffled = list(i[1:end])
			shuffle(shuffled)
			out.append(i[0] + "".join(shuffled) + i[end:])
		else:
			out.append(i)

	await message.channel.send(" ".join(out))
	#whatcha doin yes