import discord
from discord.ext import commands
import time
import sys
import os
import json
import darealmodule


class Profile(commands.Cog):
    """This module allows you to check your profile data and reletive information."""




    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:Profile:718137089434189825>'
        self.thumbnail = 'https://media.discordapp.net/attachments/714855923621036052/718134838368141452/433917.png'
        self.helping = darealmodule.Helping()

    def has_profile():
        async def predicate(ctx):
            user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM profiles WHERE discord_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)
            if not user:
                embed=discord.Embed(title="You need to create a profile first.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create your profile.', color=0x2f3136)
                embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
                await ctx.send(embed=embed)
                raise discord.ext.commands.CommandNotFound
            else:
                return True
        return commands.check(predicate)


    @commands.command(aliases=['c'], help='Alows you to create a profile binded to your account ID, you need to have a profile if you want to use most of the commands in this bot.')
    async def create(self, ctx):

        """
        Creates a profile binded to your account ID.
        """

        user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM profiles WHERE discord_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if user:
            embed=discord.Embed(title="You already have a profile.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}remove` to delete your profile.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        user = await self.bot.pg_con.execute("INSERT INTO profiles (guild_id, discord_id, money) VALUES ($1, $2, $3)", ctx.guild.id, ctx.author.id, 25.00)

        embed=discord.Embed(title="Account was created successfully.", description=f'<:check:711530148196909126> Use `{ctx.prefix}remove` to delete your profile.', color=0x2f3136)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)
        return


    @commands.command(help='Alows you to remove the profile binded to your account ID, this action can not be undone. Please note that this is guild specific.')
    @has_profile()
    async def remove(self, ctx):

        """
        Removes the profile binded to your account ID.
        """

        user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM profiles WHERE discord_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if not user:
            embed=discord.Embed(title="You don't yet have a profile.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create a new profile.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        user = await self.bot.pg_con.execute("DELETE FROM profiles WHERE guild_id = $1 AND discord_id = $2", ctx.guild.id, ctx.author.id)


        embed=discord.Embed(title="Account was removed successfully.", description=f'<:check:711530148196909126> Use `{ctx.prefix}create` to create a new profile.', color=0x2f3136)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)
        return


def setup(bot):
    bot.add_cog(Profile(bot))
