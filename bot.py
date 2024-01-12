# stuff the bot needs to run, you may need to install the dependencies with pip
# normally u can install them by running installer.bat if ur on windows

import discord, time, asyncio, subprocess, os, json, logging
from discord.ext import commands
from discord.ext.commands import has_permissions, TextChannelConverter

def load_config(file_path):
  with open(file_path, 'r') as config_file:
    config = json.load(config_file)
  return config

config = load_config('config.json')  # you may need to change "config.json" on this line to the path of your json file

TOKEN = config['token']
PREFIX = config['prefix']
OWNER = config['owner']

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=False,
                   intents=discord.Intents.all())
bot.remove_command("help") # removes prebuilt help command

@bot.command(aliases=['p'])
async def ping(ctx):
   await ctx.send(f'pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def credits(ctx): # PLEASE leave wawa and i in the "credits" command, if you don't want to have the command, its okay but like 😭
  credits_msg = (
     f'-credits page\n\n'
     f'soda, dumbass and owner\n'
     f'*"i learned a bit thanks to wawer, that also just shows how much of a loser i am"*\n'
     f'wawa - co-owner of big rat, he also showed me a cool ass rat!\n'
     f'*"you should make biggie cheese as the <@1186799032899743835> profile pcitur"* followed by a image of the rat mentioned\n'
     f'dem one thousand one hundred and eleven - inspiring me to make ballde clon\n'
     f'*"<:youweresaying:1193297299040911420>"*'
  )

  await ctx.send(credits_msg)

@bot.command(aliases=['sinfo', 'si'], description='Displays information about the server')
@commands.guild_only()
async def serverinfo(ctx):
    try:
        server = ctx.guild

        msg = (
            f'``` - srvr info - {server.name}\n'
            f'- srvr creation date: {server.created_at}\n'
            f'- owner: {server.owner} (ID: {server.owner_id})\n'
            f'- guild id: {server.id}\n'
            f'- mmbr count: {server.member_count}\n'
            f'- cjannel count: {len(server.channels)}\n'
            f'- emoji(s): {len(server.emojis)}\n'
            f'- roles: {len(server.roles)}\n'
        )

        bot_count = sum(1 for member in server.members if member.bot)
        msg += f'- bots: {bot_count}```\n'

        await ctx.send(msg)

    except Exception as e:
        print(f"error: {e}")
        await ctx.send("eerererer eerer occured")
        
# for running this command you need the "waybackurls" package from blackarch linux, this bot may be mostly ran by windows users so i think it's better to leave it disabled (if you want, and have the enough time, you can remake it and make it not use waybackurls!)
# @bot.command()
# async def waybackurls(ctx, url: str):
#  try:
#      result = subprocess.check_output(['waybackurls', url], universal_newlines=True)
#      with open('output.txt', 'w') as f:
#          f.write(result)
#      await ctx.send(file=discord.File('output.txt'))
#  except Exception as e:
#      await ctx.send(str(e))
#  finally:
#      if os.path.exists('output.txt'):
#          os.remove('output.txt')

@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
   await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

@bot.command()
async def h(ctx):
  help_msg = (
      f'``` - help page\n\n'
      f'ping, p - shows the bot latency\n'
      f'say - make the bot say something\n'
      f'kk, kick - kick someone in the nuts\n'
      f'serverinfo, si, sinfo - serverinfo, made by wawer\n'
      f'bn, ban - ban someone in the head\n'
      f'snipe, s - snipes last deleted message\n'
      f'credits - credits for commands n shit \n'
      f'grole - givs a role to specified user (requires manage_roles)\n'
#      f'waybackurls - returns wayback urls from the url provided\n'
      f'lock - locks channel, requires manage_channels\n'
      f'kill - shut downs the bot 😭 (turns into idle as waning)\n'
      f'clear - deletes specified number of messages (requires manage_messages)\n'
      f'userinfo - name explains itself```'
  )
  await ctx.send(help_msg)

@bot.command()
@commands.guild_only()
async def userinfo(ctx, member: discord.Member = None):
  if not member:
      member = ctx.author
  msg = (
    f'``` - usr info for {member}\n'
    f'usrnm - {member.display_name}\n'
    f'id - {member.id}\n'
    f'joined srvr - {member.joined_at.strftime("%Y-%m-%d %H:%M:%S")}\n' # probably bugged if not in server so we use @commands.guild_only()
    f'joined ds -{member.created_at.strftime("%Y-%m-%d %H:%M:%S")}```\n'

    )

  await ctx.send(msg)

@bot.command()
@commands.guild_only()
@has_permissions(manage_roles=True)
async def grole(ctx, member: discord.Member, role: discord.Role):
   await member.add_roles(role)
   await ctx.send(f'{member} was given role {role}')

@bot.command()
@commands.guild_only()
@has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
  await ctx.channel.purge(limit=amount+1)
  await ctx.send(f'deleted {amount} msgs for u king', delete_after=5)

@bot.command()
async def say(ctx, *, content):
  await ctx.message.delete()
  await ctx.send(content)

@bot.command(name="playing", description="Changes the playing status of the bot")
async def playing(ctx, *, status: str):
    if str(ctx.author.id) == OWNER:
        await bot.change_presence(activity=discord.Game(name=f"{status}"))
    await ctx.send("set th playing status to " + status)

@bot.command(name="streaming", description="Changes the streaming status of the bot")
async def streaming(ctx, *, status: str):
    if str(ctx.author.id) == OWNER:
        await bot.change_presence(activity=discord.Streaming(name=f"{status}", url="https://www.twitch.tv/settings"))
    await ctx.send("set th streaming status to " + status)

@bot.command(name="listening", description="Changes the listening status of the bot")
async def listening(ctx, *, status: str):
    if str(ctx.author.id) == OWNER:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
    await ctx.send("set th listening status to " + status)

@bot.command(name="watching", description="Changes the watching status of the bot")
async def watching(ctx, *, status: str):
    if str(ctx.author.id) == OWNER:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
    await ctx.send("set th watching status to " + status)

@bot.command(name="stopstatus", description="Stops the status")
async def stopstatus(ctx):
    if str(ctx.author.id) == OWNER:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=""))
    await ctx.send("stopped the status lol!")

@bot.command()
async def kill(ctx):
    """Shuts down the bot with a 3-second delay if the author is the owner."""
    if str(ctx.author.id) != OWNER:
        return

    await ctx.send('shutting down in 3 seconds... 😭') # messGGAE that bot saays before dying
    await bot.change_presence(status=discord.Status.idle) # changes status to idle as warning
    await asyncio.sleep(3) # change the number for how much time for it to turn off
    await bot.close() # kills the bot!
  
@bot.command(aliases=['kk'])
@commands.guild_only()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
   await member.kick(reason=reason)
   await ctx.send(f"`{member}` has been kick(ed)")

@bot.command(aliases=['bn'])
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
   await member.ban(reason=reason)
   await ctx.send(f"`{member}` has been ban(ned)")

last_messages = {}

@bot.event
async def on_message_delete(message):
 last_messages[message.channel.id] = {'content': message.content, 'author': message.author.name} # logs message deleted, not shared on terminal

@bot.command(aliases=['s'])
@commands.guild_only()
async def snipe(ctx):
 if ctx.channel.id in last_messages:
     last_message = last_messages[ctx.channel.id]
     await ctx.send(f' `{last_message["author"]}` said: "{last_message["content"]}"')
 else:
     await ctx.send('no msgs to snipe (yet)')

@bot.event
async def on_guild_join(guild):
   for channel in guild.text_channels:
       if channel.permissions_for(guild.me).send_messages:
           await channel.send('thanks for inviting the biggest rat in town, for a list of commands use `,h`') # message that (should) appear once you invite it to your server
           break

@bot.event
async def on_guild_join(guild):
  print(f'rat joined guild: {guild.id}')

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(f'cooldown! {round(error.retry_after, 2)} seconds left') # used to be for the "global message" command, now removed as it sucked ass

@bot.event
async def on_command_error(ctx, error):
    logging.exception("exception errored during command! lol:", exc_info=error)

@bot.event
async def on_ready():
  print(f'logged in! {bot.user.id}')

if config is not None and 'token' in config: # checks the json for the token and runs it
    TOKEN = config['token']
else:
    exit()

if TOKEN:
    bot.run(TOKEN)
else:
    print("no token added in the config.json file grrrr")
