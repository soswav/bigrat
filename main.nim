import dimscord, asyncdispatch, times, options

var
    token: string = "token"
    prefix: string = ","

let discord = newDiscordClient(token)

# Handle event for on_ready.
proc onReady(s: Shard, r: Ready) {.event(discord).} =
    echo "Ready as " & $r.user & ". Current prefix is \"" & prefix & "\" Now, enjoy!"

# informal
proc messageCreate(s: Shard, m: Message) {.event(discord).} =
  if m.content == prefix & "about":
    discard await discord.api.sendMessage(m.channel_id, "```\nthis bot was coded with nim 👑!\nthis bot used to be coded with python, i discontinued it cuz i rlly wanted to learn something that isn't python!\ni'm also currently learning nim 👑, so expect errors!\n\ncurrent commands:\nprefix = \",\"\nping  - shows response time\nabout - this page\nhelp  - shows commands\n```")
  elif m.content == prefix & "help":
    discard await discord.api.sendMessage(m.channel_id, "```\ncurrent commands:\nprefix = \",\"\nping  - shows response time\nabout - general information\nhelp  - this page\n```")
  elif m.content == prefix & "ping":
    let
        before = epochTime() * 1000
        msg = await discord.api.sendMessage(m.channel_id, "ping?")
        after = epochTime() * 1000
    discard await discord.api.editMessage(
        m.channel_id,
        msg.id, 
        "pong! took " & $int(after - before) & "ms and then " & $s.latency() & "ms"
    )

  await s.updateStatus(activity = some ActivityStatus(
        name: "with rats",
        kind: atPlaying
    ), status = "donotdisturb")

# Connect to Discord and run the bot.
waitFor discord.startSession()
