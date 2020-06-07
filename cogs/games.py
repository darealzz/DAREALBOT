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

    def has_profile():
        async def predicate(ctx):
            user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM profiles WHERE discord_id = $1", ctx.author.id)
            if not user:
                embed=discord.Embed(title="You need to create a profile first.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create your profile.', color=0x2f3136)
                embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
                await ctx.send(embed=embed)
                raise discord.ext.commands.CommandNotFound
            else:
                return True
        return commands.check(predicate)

    @commands.command(help='`<choice>` - Heads, Tails\nFlips a coin, if your choice is the same as what the flip returns, you will earn money calculated from the currant ammount of money you have, if you get it wrong you will lose money based on the ammount of money you have. You need at least $25 to be able to run this command.')
    @has_profile()
    @commands.is_owner()
    async def flip(self, ctx, choice):
        """
        Flips a coin for money.
        """
        async def random_roast(lost):
            return random.choice([f'Hahahah **noob** you failed and fliped `{flip.lower()}` instead but u chose `{choice.lower()}`, u just lost `${lost}`',
            f'LOL U PEASENT, YOU JUST LOST `${lost}`.. my man chose `{choice.lower()}` and flipped a `{flip.lower()}` :rofl:',
            f'**lmao... imagine being you right now** :laughing: u just lost `${lost}` cuz you chose `{choice.lower()}` and rolled `{flip.lower()}` L0L'])
        
        async def random_compliment():
            lost = await darealmodule.Money.calculate_random_remove(self, ctx, ctx.author.id, 5, 10)
            return random.choice([f'Hahahah **noob** you failed and fliped `{flip.lower()}` instead but u chose `{choice.lower()}`, u just lost `${lost}`',
            f'LOL U PEASENT, YOU JUST LOST `${lost}`.. my man chose `{choice.lower()}` and flipped a `{flip.lower()}` :rofl:',
            f'**lmao... imagine being you right now** :laughing: u just lost `${lost}` cuz you chose `{choice.lower()}` and rolled `{flip.lower()}` L0L'])
        
        choice = choice.upper()

        if choice not in ('HEADS', 'TAILS', 'HEAD', 'TAIL'):
            embed=discord.Embed(title="You did not enter a valid aurgument.", description=f'<:warningerrors:713782413381075536> See `{ctx.prefix}help {ctx.command}` for more information.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return

        if choice[-1] != 'S': choice += 'S'

        flip = random.choice(['HEADS', 'TAILS'])

        if flip == choice:
            pass
        
        else:
            lost = await darealmodule.Money.calculate_random_remove(self, ctx, ctx.author.id, 5, 10)
            await darealmodule.Money.remove_ammount(self, ctx, ctx.author.id, lost)
            await ctx.send(f'<:rcross:711530086251364373> {await random_roast(lost)}\n{ctx.author.mention}')

def setup(bot):
    bot.add_cog(Games(bot))
