import discord
from discord.ext import commands
import time
import sys
import os
import json
import darealmodule
import random

class Games(commands.Cog):
    """This module allows you to play games and earn money."""


    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:Games:718138175792480286>'
        self.thumbnail = 'https://media.discordapp.net/attachments/714855923621036052/718137951401410641/433916.png'
        self.helping = darealmodule.Helping()

    def has_profile():
        async def predicate(ctx):
            user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM profiles WHERE discord_id = $1", ctx.author.id)
            if not user:
                embed=discord.Embed(title="You need to create a profile first.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create your profile.', color=0x2f3136)
                embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
                await ctx.send(embed=embed)
                raise discord.ext.commands.CommandNotFound
            else:
                return True
        return commands.check(predicate)

    @commands.command(help='Flips a coin, if your choice is the same as what the flip returns, you will earn money calculated from the currant ammount of money you have, if you get it wrong you will lose money based on the ammount of money you have. You need at least $25 to be able to run this command.')
    @has_profile()
    @commands.is_owner()
    async def flip(self, ctx, choice):
        """
        Flips a coin for money.
        """
        choice = choice.upper()
        if choice not in ('HEADS', 'TAILS', 'HEAD', 'TAIL'):
            await ctx.send('bro enter a valid ting')
            return
        if choice[-1] != 'S': choice += 'S'

        flip = random.choice(['HEADS', 'TAILS'])
        if flip == choice:
            await ctx.send(helping.get_money())
        else:
            await ctx.send('no')

def setup(bot):
    bot.add_cog(Games(bot))
