from replit import db
import random
from zstats import getMember, bal


async def balance(message, client):

    args = message.content.split(" ")

    if len(args) == 2 and str(message.author.id) not in db["members"]:
        responses = [
            "no money, big funny",
            "make an account first",
            "can't have money if you dont exist",
        ]
        return random.choice(responses)

    if len(args) == 3 and not args[2].startswith("<@") and args[2].endswith(">"):
        await message.channel.send("Mention someone to see their account")
        return

    if len(args) == 2:
        user = str(message.author.id)

    if len(args) >= 3:
        searched = getMember(args[2:], message.guild.id, client)
        user = str(searched.id) if searched else False

    if not bool(user):
        return "I couldn't find anybody"

    if user not in db["members"]:
        return f"Get {searched.name}#{searched.discriminator} to make an account"
        return
    money = db["members"][user]["money"]

    thing = random.choice(bal)
    name = await client.fetch_user(user)
    return (f"{name} has `{int(money)}` coins, {thing}", True)
