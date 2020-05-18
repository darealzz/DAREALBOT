import discord
from discord.ext import commands
import time
import sys
import os


class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("<:rcross:711530086251364373> **You don't have permissions to run this command!.**")
            return
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("<:rcross:711530086251364373> **You did not give all peramiters for that command!.**")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("<:rcross:711530086251364373> **You did not give valid peramiters for that command!.**")
            return
        if isinstance(error, commands.NotOwner):
            await ctx.send("<:rcross:711530086251364373> **You must own this bot to use that command!.**")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("<:rcross:711530086251364373> **Please provide all aurguments!.**")
            return



def setup(bot):
    bot.add_cog(Errors(bot))
