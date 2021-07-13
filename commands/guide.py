from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio

async def guide(message, client):
    args = message.content.split(" ")
    if len(args) == 2:
        mess = await message.reply(
            "things you can get guidance on: \n\n- locations\n- contracts\n- reputation\n- marketplace trades\n\nclick one of the buttons to get help about something",
            components=[
                Button(style=ButtonStyle.blue, label="Locations"),
                Button(style=ButtonStyle.blue, label="Contracts"),
                Button(style=ButtonStyle.blue, label="Reputation"),
                Button(style=ButtonStyle.blue, label="Trades"),
								Button(style=ButtonStyle.blue, label="Bot Setup")
            ],
        )
        try:
          res = await client.wait_for("button_click", timeout = 30.0)
        except asyncio.TimeoutError:
          mess.components = []
        else:
          if res.component.label == "Locations":
            msg = await message.channel.send(
									"""**Locations** \n\nLocations are kind of like rebirths. There are 4 subcommands: my, view, buy, and transfer.
	my
	> Shows the locations you own, and your current location

	view
	> Shows the locations available. Put the location id after this to  view more information about the location

	buy
	> You have to options for buying: buy and liquidate, or just buy. If you put liqiudate at the end of the command, everything in your current location will be sold and the new one will be bought. Otherwise, you can keep everything in your old location

	transfer
	> This one is a bit complicated. The command can be broken down into three parts:

	> [command] [animals] [location]

	> Command:
	> The beginning of the command. [prefix] location transfer

	> Animals:
	> A list of animals. Each item goes [amount] [animal]. Separate the items with commas and a space. (eg. 5 cow, 6 sheep, 1 chicken)

	> Location:
	> The name of the location you want to transfer the animals to

	> You can also use [prefix] location transfer [location] to transfer yourself to that location

	Each location has multipliers for different plants and animals, and some plants and animals will die in the wrong location!
	""",
									components=[
											Button(style=ButtonStyle.grey, label="❌"),
									],
							)
            resp = await client.wait_for("button_click")
            if resp.author == message.author:
              print(resp.component.label)
              if resp.component.label == "❌":
                await msg.delete()
                await mess.delete()
                return

          if res.component.label == "Contracts":
              msg = await message.channel.send(
									"**Contracts**\n\nContracts are a soft of side-quest feature in farmout. They're a good way to get some quick cash or items while you're waiting for your crops to grow. Contracts are like quests themselves, with a story behind each one.\nContracts have 4 subcommands: `show, sign, complete`, and `current`.\n\n__`show`__\nShow shows the current contracts that you can sign. You must complete all 3 contracts in 1 part before moving on to the next part.\n\n__`sign`__\nSign is for signing contracts. Once you have completed your current contract, you use this command to sign a new one.\n\n__`complete`__\nComplete is when you have gathered all the things for your current contract, and is ready to complete it and claim your reward.\n\n__`current`__\nCurrent shows the contract that you have signed currently.\n\nThat's about it for contracts. There are 4 parts of 3 contracts, for a total of 12. Also, you get a pretty cool item once you complete all the contracts.",
									components=[
											Button(style=ButtonStyle.grey, label="❌"),
									],
							)
              resp = await client.wait_for("button_click")
              if resp.author == message.author:
                  if resp.component.label == "❌":
                      await msg.delete()
                      await mess.delete()

          if res.component.label == "Reputation":
              msg = await message.channel.send(
									"**Reputation**\n\nReputation is exactly what it sounds like. It is how much the market likes or dislikes you. \n\n__How to gain and lose reputation__\nThere are a few ways to gain or lose rep.	If you do the beg command, there is a chance to lose reputation. If you trade, there is a chance to gain rep. Just playing farmout, buying, selling, and gambling, can help you gain or lose rep with the marketplace.\n\n__What does reputation affect?__\nReputation affects item cost and sellcost, daily and hourly, and some other little things too.\n\nTo see rep caps, do the `i reputation` command.",
									components=[
											Button(style=ButtonStyle.grey, label="❌"),
									],
							)
              resp = await client.wait_for("button_click")
              if resp.author == message.author:
                  if resp.component.label == "❌":
                      await msg.delete()
                      await mess.delete()

          if res.component.label == "Trades":
              msg = await message.channel.send(
              "**Trades**\n\nTrades are a great way to trade your items for profits with the marketplace. Things to know about trades:\n\n- trades update every 6 hours\n- there are 5 trades, from less expensive to more\n- every trade has a stock limit\n- you get rep for trading\n- trades usually give a large profit",
              components=[Button(style=ButtonStyle.grey, label="❌"),],)
              resp = await client.wait_for("button_click")
              if resp.author == message.author:
                if resp.component.label == "❌":
                  await msg.delete()
                  await mess.delete()
          if res.component.label == 'Bot Setup':
            msg = await message.channel.send(
									"**Setting up the bot**\n\nIf you\'re not an admin, this won\'t help you much.\n\n- Prefix\nThe prefix is the phrase that you put at the start of a message to make the bot respond to you (ie. `i help`, where `i` is the prefix). By default, the prefix is `i`. You can change it with `i prefixchange`. If you want to know the current prefix, you can ping the bot and it\'ll tell you.\n\n- System Messages\nYou can have the bot send messages to alert when trades update. You use the `setchannel` command and specify a channel that the bot will alert trade updates to. Make sure that the bot has permissions to talk there first.",
									components=[
											Button(style=ButtonStyle.grey, label="❌"),
									],
							)
            resp = await client.wait_for("button_click")
            if resp.author == message.author:
              if resp.component.label == "❌":
                await msg.delete()
                await mess.delete()