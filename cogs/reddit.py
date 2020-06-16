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

    """This Module allows give you reletive data about this bot."""

    def __init__(self, bot):
        self.bot = bot
        self.icon = "<:Fun:722199115680710687>"
        self.thumbnail = 'https://media.discordapp.net/attachments/714791190926458901/722198928254304415/maps-and-location.png'

    @commands.command(help='Generates a meme..')
    async def meme(self, ctx):
        """
        Generates a meme.
        """

        meme_lst = list(self.bot.memes_cache.items())
        meme = random.choice(meme_lst)
        await ctx.send(meme[1])


def setup(bot):
    bot.add_cog(Reddit(bot))
