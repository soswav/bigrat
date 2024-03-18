import dimscord, asyncdispatch, times, options

var
    token: string = "token" # the token to turn the bot on (duh)
    prefix: string = ">_" # the prefix the bot will use

let discord = newDiscordClient(token)

proc onReady(s: Shard, r: Ready) {.event(discord).} =
    echo "ready as " & $r.user & "! current prefix is \"" & prefix & "\" now, enjoy ur bot!"

proc messageCreate(s: Shard, m: Message) {.event(discord).} =
  if m.content == prefix & "about":  # if the message content is ">_about" then:
    discard await discord.api.sendMessage(m.channel_id, "```\nthis bot was coded with nim 👑!\nthis bot used to be coded with python, i discontinued it cuz i rlly wanted to learn something that isn't python!\ni'm also currently learning nim 👑, so expect errors!\n\ncurrent commands:\nprefix = \"" & prefix & "\"\nping  - shows response time\nabout - this page\nhelp  - shows commands\n```")
  elif m.content == prefix & "help": # if the message content is ">_help" then:
    discard await discord.api.sendMessage(m.channel_id, "```\ncurrent commands:\nprefix = \"" & prefix & "\"\nping  - shows response time\nabout - general information\nhelp  - this page\n```")
  elif m.content == prefix & "ping": # if the message content is ">_ping" then:
    let
        before = epochTime() * 1000
        msg = await discord.api.sendMessage(m.channel_id, "ping?")
        after = epochTime() * 1000
    discard await discord.api.editMessage(
        m.channel_id,
        msg.id, 
        "pong! took " & $int(after - before) & "ms and then " & $s.latency() & "ms"
    )

  await s.updateStatus(activity = some ActivityStatus( # another example thing found in Dimscord repo...
        name: "with rats",
        kind: atPlaying
    ), status = "idle")

#[
   like the original bot, most of the cool-looking stuff are in the text commands, somehow
   make sure to:
   elif m.content == prefix & "command name":
   if you want a new command
   "elif" means elseif which means that if the "elif" or "if" before it are invalid then it will do X thing
   the "m.content" stands for message content, the "==" means equals
   "prefix & "command name":" uses the variable "prefix" which contains the prefix so if the user (for example) runs ">_about" then it
   will show the "about" command stuff! the two dots are the "then" (e.g.: if X thing true then | if X == true: )
   in a simplified way, it's essentially:
   "ok, if the content of the message is ">_command name" then do this:"

   i think i explained the best i could
]#

# connects to discord and start bot
waitFor discord.startSession()
