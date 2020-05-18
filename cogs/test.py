import discord
from discord.ext import commands
import time
import sys
import os


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:info:712000699600339015>'

    @commands.command(description="Displays the average webstock latency.")
    async def testerthing(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Info(bot))
