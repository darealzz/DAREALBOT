import discord
from discord.ext import commands
import time
import sys
import os
import darealmodule
import requests
import json
import aiohttp
import random

class Reddit(commands.Cog):
    """Shows random images from subreddits pulled from hot, top, new & rising reletive to the command."""

    def __init__(self, bot):
        self.bot = bot
        self.icon = "<:Reddit:722784504049172540>"
        self.thumbnail = 'https://media.discordapp.net/attachments/714855923621036052/722785426871681044/stars_1.png?width=499&height=499'

    @commands.command(help='Generates a meme.')
    async def meme(self, ctx):
        """
        Generates a meme.
        """

        meme_lst = list(self.bot.memes_cache.items())
        meme = random.choice(meme_lst)

        embed=discord.Embed(title=f'{meme[1][1]}', description=f'{meme[0]}', color=0x2f3136)
        embed.set_image(url=f'{meme[1][0]}')
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.send(embed=embed)

    @commands.command(aliases = ['cutedog', 'dogo'], help='Generates you a cute cute dogo.')
    @commands.is_owner()
    async def dog(self, ctx):
        """
        Generates a cute dog.
        """

        dog_lst = list(self.bot.cute_dog_cache.items())
        dog= random.choice(dog_lst)

        embed=discord.Embed(title=f'{dog[1][1]}', description=f'{dog[0]}', color=0x2f3136)
        embed.set_image(url=f'{dog[1][0]}')
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Reddit(bot))
