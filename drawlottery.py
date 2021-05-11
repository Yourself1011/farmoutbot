from replit import db
import random
from requests import post, exceptions

async def drawlottery(client):
	person = random.choice(db['lottery'])
	person = client.get_user(person)
	people = len(db['lottery'])
	if people == 1:
		return
	print(f'{person.name} won a {people} entry lottery')
	await person.send(f'lmao you won the lottery, there were {people} entries so you won {people*200} coins') #only 100 eh? uhh /shrug
	a = db['members']
	a[str(person.id)]['money'] += people*100
	db['members'] = a
	a = db['lottery']
	a = []
	db['lottery'] = a
	data = {
		"username": "Lottery winner!",
		"content": f'{person.name} won the lottery, there were {people} entries so they won {people*200} coins'
	}
	for i in db['server']:
		if db['server'][i]['channel'] != None and "webhookUrl" in db["server"][i]:
			result = post(db['server'][i]["webhookUrl"], json = data)
			try:
				result.raise_for_status()
			except exceptions.HTTPError as err:
				print(err)