from replit import db
from asyncio import TimeoutError


async def end(message, client):
    if str(message.author.id) not in db["members"]:
        await message.channel.send("Gotta start first before you can end")
        return

    await message.channel.send(
        "Oi you're about to delete your account. Type yes if you wanted to in 30 seconds. Otherwise, don't type yes in 30 seconds."
    )

    def check(m):
        return m.content.lower() == "yes" and m.author.id == message.author.id

    try:
        msg = await client.wait_for("message", timeout=30.0, check=check)
    except TimeoutError:
        await message.channel.send("aight guess we're not deleting you today")
    else:
        a = db["members"]
        del a[str(message.author.id)]
        db["members"] = a
        await message.channel.send("Bruh now you gotta start all over again u dumdum")
        return


# Umm you might want a "this will delete your account. are you sure you want to do this? y/n" before deleting their account.
