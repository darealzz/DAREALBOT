import discord
from discord.ext import commands, tasks
import time
import sys
import os
import json

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=20)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.users)} Users"))

    @tasks.loop(seconds=40)
    async def change_statuss(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"DArealServers"))

    @commands.Cog.listener()
    async def on_ready(self):

        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

        self.change_status.start()
        self.change_statuss.start()


def setup(bot):
    bot.add_cog(Events(bot))
