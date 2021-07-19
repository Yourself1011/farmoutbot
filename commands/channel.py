from replit import db
import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

async def channel(message, client):
    name = message.guild.name
    channel = db["server"][str(message.guild.id)]["channel"]
    args = message.content.split(' ')
    if len(args) == 2:
      return 'please use a subcommand: \n\n-show\n-set'
    if args[2].lower() == 'show':
      if channel == None:
        await message.channel.send(f"`{name}` has not set a system messages channel.")
        return
      await message.channel.send(
    f"The system messages channel for `{name}` is <#{channel}>."
   )
    if args[2].lower() == 'set':
      if not message.author.guild_permissions.manage_guild:
        await message.channel.send(f"gotta have `Manage Server` perms for that")
        print(f"{message.author.name} tried to set channel with no perms")
      else:
        args = message.content.split(" ")
        if len(args) == 2:
          await message.channel.send("gotta specify a channel dummy")
          return
        if not args[2].startswith("<#") and args[2].endswith(">") and not args[2].lower() == 'none':
          await message.channel.send("mention a channel for this to work, or say none")
          return
        if args[2].lower() == 'none':
          a = db['server']
          a[str(message.guild.id)]['server'] = None
          return 'ok there isnt a system messages channel anymore'
        with open("farmoutIcon.png", "rb") as image:
          f = image.read()
          b = bytearray(f)

        channel = args[2].strip("<#")
        channel = channel.strip(">")
        try:
          webhook = await message.guild.get_channel(int(channel)).create_webhook(
            name="Farmout", avatar=b
          )
        except discord.Forbidden:
          await message.channel.send(
            "I don't have enough permissions! Make sure I can create webhooks in that channel"
          )
          return

        msg = await message.reply(
          f"are you sure you want to change the system messages channel to <#{channel}>?",
          components=[
            Button(style=ButtonStyle.green, label="Yes"),
            Button(style=ButtonStyle.red, label="No"),
          ],
        )

        res = await client.wait_for("button_click")
        if res.author == message.author:
          if res.component.label == "No":
            await message.reply("alr looks like we're not changing today")
            msg.components = []
            return
          else:
            a = db["server"]
            a[str(message.guild.id)]["channel"] = int(channel)
            a[str(message.guild.id)]["webhookUrl"] = webhook.url
            db["server"] = a
            server = message.guild.name
            channel = db["server"][str(message.guild.id)]["channel"]
            await message.reply(
              f"The system messages channel for `{server}` is now <#{channel}>."
            )
            msg.components = []
        return
