import discord, json, time, asyncio, subprocess, os, logging
from discord.ext import commands
from discord.ext.commands import has_permissions, TextChannelConverter
logging.basicConfig(level=logging.INFO)

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

config = load_config('config.json') # NOTE! the "config.json" isnide the curvy things must be edited to the file location! e.g: C:/path/to/json.json (idfk, i don't use windows anymore)

TOKEN = config['token']
PREFIX = config['prefix']

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=False,
                   intents=discord.Intents.all())
bot.remove_command("help")

@bot.command(aliases=['p'])
async def ping(ctx):
   await ctx.send(f'pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def credits(ctx):
  credits_msg = (
     f'-credits page\n\n'
     f'soda, main dumbass and owner\n'
     f'*"i learned a bit thanks to ai, that also just shows how much of a loser i am"*\n'
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

@bot.command()
async def waybackurls(ctx, url: str):
  try:
      result = subprocess.check_output(['waybackurls', url], universal_newlines=True)
      with open('output.txt', 'w') as f:
          f.write(result)
      await ctx.send(file=discord.File('output.txt'))
  except Exception as e:
      await ctx.send(str(e))
  finally:
      if os.path.exists('output.txt'):
          os.remove('output.txt')

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
      f'waybackurls - returns wayback urls from the url provided\n'
      f'lock - locks channel, requires manage_channels\n'
      f'kill - shut downs the bot 😭 (turns into idle as waning)\n'
      f'clear - deletes specified number of messages (requires manage_messages)\n'
      f'userinfo - name explains itself```'
#      f'||**please note that im still a WIP and is made of shit code <:love:1193180918165274706><:love:1193180918165274706> kk thanks**||'
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

@bot.command()
async def kill(ctx):
 if ctx.author.id == 968952481281368184:
     await ctx.send('killing myself in 3 seconds 😭😭')
     await bot.change_presence(status=discord.Status.idle)
     await asyncio.sleep(3)
     await bot.close()

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
 last_messages[message.channel.id] = {'content': message.content, 'author': message.author.name}

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
           await channel.send('thanks for inviting the biggest rat in town, for a list of commands use `,h`\n hi')
           break

@bot.event
async def on_guild_join(guild):
  print(f'rat joined guild: {guild.id}')

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(f'cooldown! {round(error.retry_after, 2)} seconds left')

@bot.event
async def on_command_error(ctx, error):
   logging.exception("exception occurred during command")
   await ctx.send("error occurred while running command (may be missing argument, or it doesn't exist, *who knows?*)")


@bot.event
async def on_ready():
  print(f'logged in! {bot.user.id}')

if config is not None and 'token' in config:
    TOKEN = config['token']
else:
    exit()

if TOKEN:
    bot.run(TOKEN)
else:
    print("no token added in the config.json file grrrr")
