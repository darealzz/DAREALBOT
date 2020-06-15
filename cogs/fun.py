import discord
from discord.ext import commands
import time
import sys
import os
import darealmodule

class Fun(commands.Cog):

    """This Module allows give you reletive data about this bot."""

    def __init__(self, bot):
        self.bot = bot
        self.icon = "<:Fun:722199115680710687>"
        self.thumbnail = 'https://media.discordapp.net/attachments/714791190926458901/722198928254304415/maps-and-location.png'

    
def setup(bot):
    bot.add_cog(Fun(bot))