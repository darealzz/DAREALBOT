import discord
from discord.ext import commands
import time
import sys
import os


class OwnerOnly(commands.Cog):
    """
    These commands has been reserved for the ownership team to streamline development.
    """
    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:owner:712000766826774568>'
        self.thumbnail = 'https://cdn.discordapp.com/attachments/711529920349732909/712343777590902875/feelings_1.png'

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def load(self, ctx, extension):
        """
        Loads cogs.
        """
        try:
            self.bot.load_extension(f"cogs.{extension}")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog already loaded: `{extension}`**")
        else:
            await ctx.send(f"<:check:711530148196909126> | **Loaded Cog: `{extension}`**")

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def reload(self, ctx, extension):
        """
        Reloads specific cog.
        """
        try:
            self.bot.unload_extension(f"cogs.{filename[:-3]}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{extension}`**")
        else:
            self.bot.load_extension(f"cogs.{filename[:-3]}")
            await ctx.send(f"<:check:711530148196909126> | **Realoded Cog: `{extension}`**")

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """
        Unloads specific cog.
        """
        try:
            self.bot.unload_extension(f"cogs.{extension}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{extension}`**")
        else:
            await ctx.send(f"<:check:711530148196909126> | **Unloaded Cog: `{extension}`**")

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def r(self, ctx):
        """
        Reloads all cogs.
        """
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.unload_extension(f"cogs.{filename[:-3]}")
                except commands.errors.ExtensionNotLoaded:
                    await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{filename[:-3]}`**")
                else:
                    self.bot.load_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(f"<:check:711530148196909126> | **Realoded Cog: `{filename[:-3]}`**")
        #await ctx.send(f"<:check:711530148196909126> | `Reloaded the cogs`")

    @commands.command(description="Owner only.")
    @commands.is_owner()
    async def cogs(self, ctx):
        """
        Shows all cogs.
        """
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.send(f"`{filename[:-3]}`")


    @commands.group()
    @commands.is_owner()
    async def debugmode(self, ctx):

        self.bot.unload_extension(f"events.errors")

        await ctx.send(f"<:check:711530148196909126> | **Bot has been changed to debuging mode.**")

def setup(bot):
    bot.add_cog(OwnerOnly(bot))
