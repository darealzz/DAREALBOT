import discord
from discord.ext import commands
import time
import sys
import os
import json
from classes.helping import Helping


class Profile(commands.Cog):
    """
    This module allows you to check your profile data and reletive information.
    """




    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:profile:713782643698958458>'
        self.thumbnail = 'https://cdn.discordapp.com/attachments/711529920349732909/713782976944668754/cool_1.png'
        self.helping = Helping()

    async def has_profile(ctx):
        with open('data/users.json', 'r') as f:
            data = json.load(f)
        # await ctx.send(type(f"{ctx.author.id}"))
        # await ctx.send(data[f"{ctx.author.id}"])
        if f"{ctx.author.id}" not in data:
            embed=discord.Embed(title="You need to create a profile first.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create your profile.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            raise discord.ext.commands.CommandNotFound
        else:
            return True


    @commands.command()
    async def create(self, ctx):

        """
        Creates a profile binded to your account ID.
        """

        with open('data/users.json', 'r') as f:
            data=json.load(f)

        if str(ctx.author.id) in data:
            embed=discord.Embed(title="You already have a profile.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}remove` to delete your profile.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        with open('data/users.json', 'w') as f:
            data[ctx.author.id] = {
            "Dollars": 100,
            }
            json.dump(data, f, indent=4)


        embed=discord.Embed(title="Account was created successfully.", description=f'<:check:711530148196909126> Use `{ctx.prefix}remove` to delete your profile.', color=0x36393E)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)
        return


    @commands.command()
    @commands.check(has_profile)
    async def remove(self, ctx):

        """
        Removes the profile binded to your account ID.
        """

        with open('data/users.json', 'r') as f:
            data=json.load(f)

        if str(ctx.author.id) not in data:
            embed=discord.Embed(title="You don't yet have a profile.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create a new profile.', color=0x36393E)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
            await ctx.send(embed=embed)
            return

        with open('data/users.json', 'w') as f:
            del data[f"{ctx.author.id}"]
            json.dump(data, f, indent=4)


        embed=discord.Embed(title="Account was removed successfully.", description=f'<:check:711530148196909126> Use `{ctx.prefix}create` to create a new profile.', color=0x36393E)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)
        return

    @commands.command()
    @commands.check(has_profile)
    async def x(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Profile(bot))
