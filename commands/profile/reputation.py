from replit import db


async def reputation(message, client):
    if str(message.author.id) not in db["members"]:
        return "have a farm with `i start` before you get rep"

    rep = db["members"][str(message.author.id)]["reputation"]
    e = "get 700 rep to gamble"
    if rep > 700:
        e = "you can gamble, but you need 750 rep to trade"
    if rep > 750:
        e = "you can gamble and trade, at 1000 rep you can switch locations"
    if rep > 1000:
        e = "you can now gamble, trade, and move locations!"
    return f"you have {rep} reputation, {e}"
