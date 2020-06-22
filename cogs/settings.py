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

class Settings(commands.Cog):
    """Settings to allow for basic configuration & customizability."""

    def __init__(self, bot):
        self.bot = bot
        self.icon = "<:Settings:724611422926930022>"
        self.thumbnail = 'https://media.discordapp.net/attachments/714855923621036052/724610498569699348/maps-and-location.png?width=499&height=499'

    @commands.command(help='Hold')
    async def test(self, ctx):
        """
        Hold
        """
        return

def setup(bot):
    bot.add_cog(Settings(bot))
