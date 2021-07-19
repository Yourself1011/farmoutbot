from replit import db

async def prefix(message, client):
    args = message.content.split(' ')

    if len(args) == 2:
      return 'do a subcommand: \n\n-show\n-set'
    
    if args[2].lower() == 'show':
			
      prefix = db["server"][str(message.guild.id)]["prefix"]
      name = message.guild.name
      await message.channel.send(
					f"The prefix for `{name}` is `{prefix}`. use `{prefix} prefix set (new prefix)` to change the prefix."
			)
    if args[2].lower() == 'set':

      if not message.author.guild_permissions.manage_guild:
        return "no no no, gotta have `Manage Server` for that"
      else:
        if len(args) == 3:
          return f'state the new prefix: `{prefix} set (new prefix)`'
        oldprefix = db["server"][str(message.guild.id)]["prefix"]
        a = db["server"]
        a[str(message.guild.id)]["prefix"] = args[3]
        db["server"] = a
        
        newprefix = args[2]
        name = message.guild.name
        return f":white_check_mark: the prefix for `{name}` has been changed from `{oldprefix}` to `{newprefix}` by {message.author.mention}."
