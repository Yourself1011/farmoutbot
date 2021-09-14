import discord


async def credits(message, client):
    e = discord.Embed(
        title="Farmout Credits: ",
        description="You can find and meet these people in our support server, at  discord.gg/tvCmtkBAkc",
        colour=discord.Colour.blue(),
    )
    e.add_field(
        name="Lead Developer & Owner", value="Larg Ank <<<< stanky", inline=False
    )
    e.add_field(
        name="Debugged, helped, and tested",
        value="yogogiddap, Yourself <<<< not stinky, Cookie's Owner, yogogiddap",
        inline=False,
    )
    await message.channel.send(embed=e)
