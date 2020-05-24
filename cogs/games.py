import discord
from discord.ext import commands
import time
import sys
import os
import json
from classes.helping import Helping


class Games(commands.Cog):
    """
    This module allows you to play games and earn money.
    """


    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:games:713878668836995073>'
        self.thumbnail = 'https://cdn.discordapp.com/attachments/711529920349732909/713879222648832070/emoji.png'
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
    @commands.is_owner()
    @commands.check(has_profile)
    async def turtle(self, ctx):
        one=['$', '$', '$', '$', '$', '$']
        two=['$', '$', '$', '$', '$', '$']
        three=['$', '$', '$', '$', '$', '$']
        four=['$', '$', '$', '$', '$', '$']
        five=['$', '$', '$', '$', '$', '$']
        six=['#', '#', '#', '#', '#', '#']
        board_one=""
        board_two=""
        board_three=""
        board_four=""
        board_five=""
        board_six=""
        for i in one:
            board_one += f'{i}      '
        for i in two:
            board_two += f'{i}      '
        for i in three:
            board_three += f'{i}      '
        for i in four:
            board_four += f'{i}      '
        for i in five:
            board_five += f'{i}      '
        for i in six:
            board_six += f'{i}      '

        embed=discord.Embed(title="The turtle game.", description=f"""
{board_one}
{board_two}
{board_three}
{board_four}
{board_five}
{board_six}
        """, color=0x36393E)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Games(bot))
