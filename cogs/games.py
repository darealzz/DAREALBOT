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
            user = await ctx.cog.bot.pg_con.fetchval("SELECT money FROM profiles WHERE discord_id = $1 and guild_id = $2", ctx.author.id, ctx.guild.id)
            if not user:
                embed=discord.Embed(title="You need to create a profile first.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create your profile.', color=0x2f3136)
                embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(ctx.cog, ctx))
                await ctx.send(embed=embed)
                raise discord.ext.commands.CommandNotFound
            else:
                return True
        return commands.check(predicate)

    # @commands.cooldown(1, per=30, type=discord.ext.commands.BucketType.guild)
    @commands.command(help='`<choice>` - Heads, Tails\n`<bet>` - How much you want to bet\nFlips a coin, if your choice is the same as what the flip returns, you will earn double your bet, if you get it wrong you will lose the ammount of money that you placed as a bet. You need at least $25 to be able to run this command.')
    @has_profile()
    async def flip(self, ctx, choice, bet: int):
        """Flips a coin for money."""
        min_ammount = 25
        if await darealmodule.Money.has_money(self, ctx, ctx.author.id, min_ammount) == True:
            pass
        else:
            embed=discord.Embed(title="You don't have enough money to run that command.", description=f'<:warningerrors:713782413381075536> `{ctx.prefix}{ctx.command}` Requires a minimum of `${min_ammount}` to be run.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(ctx.cog, ctx))
            await ctx.send(embed=embed)
            return

        await ctx.message.add_reaction('<a:loading:716280480579715103>')

        async def random_roast_title():
            return random.choice(['Lol noob, you failed at life',
            'Oh look, you tried something and it failed...',
            'Lmao, it would suck being you right now'])

        async def random_roast(lost):
            return random.choice([f'You chose **`{choice}`** and **`{flip}`** was flipped, you lost **`${lost}`**',
            f'You lost **`${lost}`** cuz I flipped **`{flip}`** but you chose **`{choice}`** lol'])

        async def random_compliment_title():
            return random.choice(['Hmmm... looks like you got it right :confused:',
            'You.. You beat me...',
            'Looks like you chose correctly...'])

        async def random_compliment(gained):
            return random.choice([f'I flipped **`{flip}`**, just as you predicted. You earned **`${gained}`**.',
            f'My man your going to make me broke, I flipped **`{flip}`** just like you said... I gave you **`${gained}`**'])

        choice = choice.upper()

        if choice not in ('HEADS', 'TAILS', 'HEAD', 'TAIL'):
            await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)
            embed=discord.Embed(title="You did not enter a valid aurgument.", description=f'<:warningerrors:713782413381075536> See `{ctx.prefix}help {ctx.command}` for more information.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return

        if choice[-1] != 'S': choice += 'S'

        flip = random.choice(['HEADS', 'TAILS'])

        if flip == choice:
            embed=discord.Embed(title="", description=f'<:warningerrors:713782413381075536> See `{ctx.prefix}help {ctx.command}` for more information.', color=0x2f3136)
            # if ctx.author.id == 644648271901622283:
            #     gained = await darealmodule.Money.calculate_random_add(self, ctx, ctx.author.id, 0, 2)
            # else:
            gained = await darealmodule.Money.add_ammount(self, ctx, ctx.author.id, bet*2)
            await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)

            embed=discord.Embed(title=f"{await random_compliment_title()}", description=f'<:check:711530148196909126> {await random_compliment(gained)}', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return
        else:
            lost = await darealmodule.Money.remove_ammount(self, ctx, ctx.author.id, bet)
            await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)

            embed=discord.Embed(title=f"{await random_roast_title()}", description=f'<:rcross:711530086251364373> {await random_roast(lost)}', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return


def setup(bot):
    bot.add_cog(Games(bot))
