# stuff the bot needs to run, you may need to install the dependencies with pip
# normally u can install them by running installer.bat if ur on windows, for linux use "linuxinstall.sh"
import discord, time, asyncio, os, json, logging, requests, yaml, sys, datetime, random
from googletrans import Translator
from discord.ext import commands
from discord.ext.commands import has_permissions, TextChannelConverter, CommandNotFound

def load_config(file_path):
 with open(file_path, 'r') as config_file:
   config = yaml.safe_load(config_file)
 return config

config = load_config('config.yml') # you may need to change "config.yml" to the path of your yml file

TOKEN = config['token']
PREFIX = config['prefix']
OWNER = config['owner']
IPINFO_TOKEN = config['ipinfo_token']

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=False,
                   intents=discord.Intents.all())
bot.remove_command("help") # removes prebuilt help command

startTime = time.time()

@bot.command(aliases=['p'])
async def ping(ctx):
   await ctx.send(f'pong! {round(bot.latency * 1000)}ms')

def restart_bot(): 
   os.execv(sys.executable, ['python'] + sys.argv)

@bot.command(aliases=['cc', 'restart'])
async def check(ctx):
 if str(ctx.author.id) in OWNER:
   await ctx.send("checking for updates in bot.py..")
   await bot.change_presence(status=discord.Status.idle) # changes status to idle as a warning
   await asyncio.sleep(3) # change the number for how much time for it to turn off
   restart_bot()
 else:
    await ctx.send("currently, you do NOT have permissions!")

translator = Translator()

@bot.command()
async def badtranslate(ctx, *, text):
    target_language = random.choice(['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish', 'kyrgyz', 'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)', 'nepali', 'norwegian', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhalese', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu'])

    translated = translator.translate(text, dest=target_language)

    bad_translated = translator.translate(translated.text, dest='english')

    await ctx.send(f"result: `{bad_translated.text}`")

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
    everyone = ctx.guild.default_role
    overwrite = discord.PermissionOverwrite()

    if not ctx.channel.permissions_for(everyone).send_messages:
        overwrite.send_messages = True
        await ctx.channel.set_permissions(everyone, overwrite=overwrite)
        await ctx.send("channel unlolccked!")
    else:
        overwrite.send_messages = False
        await ctx.channel.set_permissions(everyone, overwrite=overwrite)
        await ctx.send("channel LOLCJEKD!!!")

@bot.command(aliases=['help'])
async def h(ctx):
 uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
 help_msg = (
      f'```'
      f'- help page\n\n'
      f'     ownercmds, oh\n'
      f'       owner commands page\n'
      f'     help, h ($)\n'
      f'       help page\n\n'
      f'ping, p - shows the bot latency\n'
      f'kk, kick - kick someone in the nuts\n'
      f'serverinfo, si - serverinfo, made by wawer\n'
      f'bn, ban - ban someone in the head\n'
      f'snipe, s - snipes last deleted message\n'
      f'quickremove, qr - deletes replied message (requires manage_messages)\n'
      f'grole - givs a role to specified user (requires manage_roles)\n'
      f'lock - locks channel (requires manage_channels)\n'
      f'clear - deletes specified number of messages (requires manage_messages)\n'
      f'cat - sends cat pic for u\n'
      f'avatar - returns avatar of mentioned user\n'
      f'banner - returns banner of mentioned user\n'
      f'ipinfo - shows info from specified ip adress\n'
      f'''badtranslate - bad translate, tribute to Assyst's badtranslate cmd\n''' 
      f'userinfo - name explains itself\n\nuptime: {uptime}'
      f'```'
  )
 await ctx.send(help_msg)

@bot.command(aliases=["oh"])
async def ownercmds(ctx):
 if str(ctx.author.id) in OWNER:
  uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
  owner = (
      f'```'
      f'- owner commands page\n\n'
      f'     ownercmds, oh ($)\n'
      f'       shows this page\n\n'
      f'status - use ",status" to see how its used\n'
      f'kill - shuts down the bot, used for restarting\n'
      f'dm - dms user mentioned, do NOT use for bad stuff!\n'
      f'check, cc, restart - checks for changes in bot.py, restarts bot\n\nuptime: {uptime}'
      f'```'
  )
  await ctx.send(owner)
 else:
    await ctx.send("currently, your id does NOT appear in the config!")

@bot.command(aliases=["qr"])
@commands.guild_only()
@has_permissions(manage_messages=True)
async def quickremove(ctx):
    if ctx.message.reference is not None:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        await referenced_message.delete()
        await ctx.send(f'deleted replied msg', delete_after=3)
    else:
        await ctx.send(f'you didnt mention anyone, silly!', delete_after=5)

@quickremove.error
async def quickremove_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Silly, you're missing the manage_messages permission!")

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
      await ctx.send(f'{member} was given role {role}')
      await ctx.send("yuo cabnot give a role higher tyhan yours!")
     return

     if ctx.guild.me.top_role <= role:
        await ctx.send("i cccanot giv a role equal or higher than my top role")
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
    try:
        if str(ctx.author.id) in OWNER:
            await member.send(content)
            await ctx.send(f'{member} was given dm with content: {content}')
        else:
            await ctx.send('currently, your id does NOT appear in the config!')
    except discord.Forbidden:
        await ctx.send(f"currently i CANNOT send a message to {member.display_name} :sob:")

@bot.command(name='cat')
async def cat(ctx):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()

    cat_image_url = data[0]['url']

    await ctx.send(f'heres ur cat! {cat_image_url}')

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
        await ctx.send(f'{user.display_name} does not have bannr')

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

@bot.command()
async def status(ctx, status_type=None, status_text=None):
    if status_type is None:
        await ctx.send("""```err: no status specified!\n\nusage: \n\nstatus (playing|streaming|watching|listening|stop) (arguement)```""")
        return

    if str(ctx.author.id) in OWNER:
        if status_type.lower() == "playing":
            await bot.change_presence(activity=discord.Game(name=status_text))
            await ctx.send(f"activity upd to `playing {status_text}`")
        elif status_type.lower() == "streaming":
            await bot.change_presence(activity=discord.Streaming(name=status_text, url="https://twitch.tv/settings"))
            await ctx.send(f"activity upd to `streaming {status_text}`")
        elif status_type.lower() == "listening":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_text))
            await ctx.send(f"activity upd to `listening to {status_text}`")
        elif status_type.lower() == "watching":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_text))
            await ctx.send(f"activity upd to `watching {status_text}`")
        elif status_type.lower() == "stop":
            await bot.change_presence(activity=None)
            await ctx.send("actikskvity cleared!!")
        else:
            await ctx.send("""```err: status doesn't exist!\n\nusage: \n\nstatus (playing|streaming|watching|listening|stop) (arguement)```""")
    if str(ctx.author.id) not in OWNER:
        await ctx.send("you don't have permissions to use this command!")

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
    if member == ctx.author:
        await ctx.send("you can't kick yourself, silly.")
        return

    if ctx.author.top_role <= member.top_role:
        await ctx.send("you don't have enough perms to kick user mentioned!")
        return

    if reason is None:
        reason = "no reason provided by user"

    try:
        await member.kick(reason=reason)
        await ctx.send(f"`{member}` has been kick(ed): {reason}")
    except Exception as e:
        await ctx.send(f"error while trying 2 kick `{member}`: {str(e)}")

@bot.command(aliases=['bn'])
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):

    if member == ctx.author:
        await ctx.send("you can't ban yourself, silly.")
        return

    if ctx.author.top_role <= member.top_role:
        await ctx.send("you don't have enough perms to ban user mentioned!")
        return

    if reason is None:
        reason = "no reason provided by user"

    try:
        await member.ban(reason=reason)
        await ctx.send(f"`{member}` has been ban(ned): {reason}")
    except Exception as e:
        await ctx.send(f"error while trying 2 ban `{member}`: {str(e)}")

last_messages = {}

@bot.event
async def on_message_delete(message):
    if message.channel.id not in last_messages:
        last_messages[message.channel.id] = []
    last_messages[message.channel.id].append({'content': message.content, 'author': message.author.name})

@bot.command(aliases=['s'])
@commands.guild_only()
async def snipe(ctx, index: int = 1):
    if ctx.channel.id in last_messages and len(last_messages[ctx.channel.id]) >= index:
        last_message = last_messages[ctx.channel.id][index - 1]
        await ctx.send(f'`{last_message["author"]}` said: "{last_message["content"]}"')
    else:
        await ctx.send('no msgs to snipe (yet)')

@bot.event
async def on_guild_join(guild):
   for channel in guild.text_channels:
       if channel.permissions_for(guild.me).send_messages:
           await channel.send('thanks for inviting the biggest rat in town! for a list of commands use `,h`') # message that (should) appear once you invite it to your server
           break

@bot.event
async def on_command_error(ctx, error):
    logging.exception("exception errored during command! lol:", exc_info=error)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("that command doesn't exist, silly!")
    else:
        raise error

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
    print("no token added in the config.json file")
