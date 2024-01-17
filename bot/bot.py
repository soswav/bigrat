# stuff the bot needs to run, you may need to install the dependencies with pip
# normally u can install them by running installer.bat if ur on windows, for linux use "linuxinstall.sh"
import discord, time, asyncio, subprocess, os, json, logging, requests, yaml
from discord.ext import commands
from discord.ext.commands import has_permissions, TextChannelConverter

def load_config(file_path):
 with open(file_path, 'r') as config_file:
   config = yaml.safe_load(config_file)
 return config

config = load_config('config.yml') # you may need to change "config.yml" to the path of your yml file

TOKEN = config['token']
PREFIX = config['prefix']
OWNER = config['owner']
IPINFO_TOKEN = config['ipinfo_token']
SS_TOKEN = config['ss_token']

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=False,
                   intents=discord.Intents.all())
bot.remove_command("help") # removes prebuilt help command

@bot.command(aliases=['p'])
async def ping(ctx):
   await ctx.send(f'pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def credits(ctx): # PLEASE leave wawa and i in the "credits" command, if you don't want to have the command, its okay but like 😭
  credits_msg = (
     f'``` - credits page\n\n'
     f'soda, dumbass and owner\n'
     f'"i learned a bit thanks to wawer"\n'
     f'wawa, co-owner of big rat, has made like 30%~ of the bot\n'
     f'"you should make biggie cheese as the big rat profile pcitur" then a image of the rat mentioned```'
  )

  await ctx.send(credits_msg)

@bot.command(aliases=['si'], description='displays info about server')
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
@commands.guild_only()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
   await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

@bot.command(aliases=['help'])
async def h(ctx):
  help_msg = (
      f'``` - help page\n\n'
      f'ping, p - shows the bot latency\n'
      f'say - make the bot say something\n'
      f'kk, kick - kick someone in the nuts\n'
      f'serverinfo, si - serverinfo, made by wawer\n'
      f'bn, ban - ban someone in the head\n'
      f'snipe, s - snipes last deleted message\n'
      f'credits - credits for commands n shit \n'
      f'help, h - help page\n'
      f'grole - givs a role to specified user (requires manage_roles)\n'
      f'ownercmds, ocmd - commands list for the owner of the bot\n'
      f'lock - locks channel, requires manage_channels\n'
      f'clear - deletes specified number of messages (requires manage_messages)\n'
      f'cat - sends cat pic for u\n'
      f'userinfo - name explains itself```'
  )
  await ctx.send(help_msg)

@bot.command()
async def ownercmds(ctx):
    if str(ctx.author.id) in OWNER:
        await ctx.send('``` - owner commands page\n\nplaying - sets status to playing, requires argument\nstreaming - sets status to streaming, requires argument\nwatching - sets status to watching, requires argument\nlistening - sets status to listeting, requires argument\nstopstatus - selfexplanatory (real)\nkill - shut downs the bot 😭 (turns into idle as warning)\ndm - dms user mentioned```')
    else:
        await ctx.send('currently, your id does NOT appear in the config!')

@bot.command(aliases=['ss'], description='takes a screenshot of the specified webpage')
async def screenshot(ctx, url: str):

    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    access_key = SS_TOKEN
    screenshot_url = f'https://api.screenshotone.com/take?url={url}&access_key={access_key}'

    try:
        embed = discord.Embed(title='big rat', color=discord.Color.blurple())
        embed.set_image(url=screenshot_url)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"a error occurred: {e}")

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
    if ctx.author.top_role <= role:
        await ctx.send("yuo cabnot give a role higher tyhan yours!")
        return

    if ctx.guild.me.top_role <= role:
        await ctx.send("i cccanot giv a role equal or higher than my top role.")
        return
    
    await member.add_roles(role)
    
    await ctx.send(f'{member} was given role {role}')


@bot.command()
@commands.guild_only()
@has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
  await ctx.channel.purge(limit=amount+1)
  await ctx.send(f'deleted {amount} msgs for u king', delete_after=5)

@bot.command(name="dm", description='DMs user mentioned, do NOT use for bad shit!')
@commands.guild_only()
async def dm(ctx, member: discord.Member, *, content):
    if str(ctx.author.id) in OWNER:
        await member.send(content)
        await ctx.send(f'{member} was given dm with content: {content}')
    else:
        await ctx.send('currently, your id does NOT appear in the config!')

@bot.command(name='cat')
async def cat(ctx):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()

    cat_image_url = data[0]['url']

    await ctx.send(f'heres your cat! {cat_image_url}')

@bot.command(name="avatar")
async def avatar(ctx, *, user: discord.Member = None):
    if not user:
        user = ctx.author
    embed = discord.Embed()
    embed.set_image(url=user.avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="banner")
async def banner(ctx, *, user: discord.Member = None):
    if not user:
        user = ctx.author
    if hasattr(user, 'banner') and user.banner:
        embed = discord.Embed()
        embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'{user.display_name} does not have a banner.')

@bot.command(name="ipinfo")
async def ipinfo(ctx, *, ip: str):
    if not ip:
        await ctx.send("specify a ip adress")
        return

    ipinfo_token = IPINFO_TOKEN

    if not ipinfo_token:
        await ctx.send("ipinfo.io token not set (yet)")
        return

    url = f"https://ipinfo.io/{ip}?token={ipinfo_token}"

    try:
        response = requests.get(url)
        data = response.json()

        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        loc = data.get("loc", "N/A")
        org = data.get("org", "N/A")
        timezone = data.get("timezone", "N/A")

        await ctx.send(f"```ip info for {ip}:\ncity: {city}\nregion: {region}\ncountry: {country}\nlocation: {loc}\norganization: {org}\ntimezone: {timezone}\n```")

    except Exception as e:
        await ctx.send(f"error occured: {e}")

@bot.command(name="playing", description="Changes the playing status of the bot")
async def playing(ctx, *, status: str):
    if str(ctx.author.id) in OWNER:
        await bot.change_presence(activity=discord.Game(name=f"{status}"))
        await ctx.send("set the playing status to " + status)
    else:
        await ctx.send("currently, your id does NOT appear in the config!")

@bot.command(name="streaming", description="Changes the streaming status of the bot")
async def streaming(ctx, *, status: str):
    if str(ctx.author.id) in OWNER:
        await bot.change_presence(activity=discord.Streaming(name=f"{status}", url="https://www.twitch.tv/settings"))
        await ctx.send("set th streaming status to " + status)
    else:
        await ctx.send("currently, your id does NOT appear in the config!")

@bot.command(name="listening", description="Changes the listening status of the bot")
async def listening(ctx, *, status: str):
    if str(ctx.author.id) in OWNER:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
        await ctx.send("set th listening status to " + status)
    else:
        await ctx.send("currently, your id does NOT appear in the config!")

@bot.command(name="watching", description="Changes the watching status of the bot")
async def watching(ctx, *, status: str):
    if str(ctx.author.id) in OWNER:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
        await ctx.send("set th watching status to " + status)
    else:
        await ctx.send("currently, your id does NOT appear in the config!")

@bot.command(name="stopstatus", description="Stops the status")
async def stopstatus(ctx):
    if str(ctx.author.id) in OWNER:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=""))
        await ctx.send("stopped the status lol!")
    else:
        await ctx.send("currently, your id does NOT appear in the config!")

@bot.command()
async def kill(ctx):
    """Shuts down the bot with a 3-second delay if the author is the owner."""
    if str(ctx.author.id) not in OWNER:
        await ctx.send("currently, your id does NOT appear in the config!")
        return

    await ctx.send('shutting down in 3 seconds... 😭') # message that bot says before dying
    await bot.change_presence(status=discord.Status.idle) # changes status to idle as a warning
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
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(f'cooldown! {round(error.retry_after, 2)} seconds left') # used to be for the "global message" command, now removed as it sucked ass

@bot.event
async def on_command_error(ctx, error):
    logging.exception("exception errored during command! lol:", exc_info=error)

@bot.event
async def on_ready():
  print(f'logged in! {bot.user.id}')

if config is not None and 'token' in config: # checks the yml for the token and runs it
    TOKEN = config['token']
else:
    exit()

if TOKEN:
    bot.run(TOKEN)
else:
    print("no token added in the config.json file grrrr")
