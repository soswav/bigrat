import discord
from discord.ext import commands
import json
import os

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

config = load_config('config.json')

OWNER = config['owner']

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="streaming", description="Sets a streaming status")
    async def streaming(self, ctx, *, name):
        if ctx.author.id != OWNER:
            return

        await self.bot.change_presence(activity=discord.Streaming(name=name, url="https://www.twitch.tv/settings"))

    @commands.command(name="playing", description="Sets a playing status")
    async def playing(self, ctx, *, name):
        if ctx.author.id != OWNER:
            return

        await self.bot.change_presence(activity=discord.Game(name=name))

    @commands.command(name="watching", description="Sets a watching status")
    async def watching(self, ctx, *, name):
        if ctx.author.id != OWNER:
            return

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))

    @commands.command(name="listening", description="Sets a listening status")
    async def listening(self, ctx, *, name):
        if ctx.author.id != OWNER:
            return

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))

    @commands.command(name="stop", description="Stops the bot's status")
    async def stop(self, ctx):
        if ctx.author.id != OWNER:
            return

        await self.bot.change_presence(activity=None)

def setup(bot):
    bot.add_cog(StatusCog(bot))