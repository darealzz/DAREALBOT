import discord
from discord.ext import commands
import time
import sys
import os
import json
import darealmodule
import random
import operator



class Profile(commands.Cog):
    """This module allows you to check your profile data and reletive information."""




    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:Profile:718137089434189825>'
        self.thumbnail = 'https://media.discordapp.net/attachments/714855923621036052/718134838368141452/433917.png'

    def has_profile():
        async def predicate(ctx):
            user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM profiles WHERE discord_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)
            if not user:
                embed=discord.Embed(title="You need to create a profile first.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create your profile.', color=0x2f3136)
                embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(ctx.cog, ctx))
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
        await ctx.message.add_reaction('<a:loading:716280480579715103>')

        user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM profiles WHERE discord_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if user:
            embed=discord.Embed(title="You already have a profile.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}remove` to delete your profile.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return

        user = await self.bot.pg_con.execute("INSERT INTO profiles (guild_id, discord_id, money) VALUES ($1, $2, $3)", ctx.guild.id, ctx.author.id, 25.00)

        embed=discord.Embed(title="Account was created successfully.", description=f'<:check:711530148196909126> Use `{ctx.prefix}remove` to delete your profile.', color=0x2f3136)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)
        await ctx.send(embed=embed)
        return


    @commands.command(help='Alows you to remove the profile binded to your account ID, this action can not be undone. Please note that this is guild specific.')
    @has_profile()
    async def remove(self, ctx):
        """
        Removes the profile binded to your account ID.
        """
        await ctx.message.add_reaction('<a:loading:716280480579715103>')

        user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM profiles WHERE discord_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if not user:
            embed=discord.Embed(title="You don't yet have a profile.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create a new profile.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return

        user = await self.bot.pg_con.execute("DELETE FROM profiles WHERE guild_id = $1 AND discord_id = $2", ctx.guild.id, ctx.author.id)


        embed=discord.Embed(title="Account was removed successfully.", description=f'<:check:711530148196909126> Use `{ctx.prefix}create` to create a new profile.', color=0x2f3136)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['profile', 'cash'], help='Shows all of the reletive data binded to your profile such as your balance, more comming soon.')
    @has_profile()
    async def ball(self, ctx):

        """
        Shows profile info.
        """
        await ctx.message.add_reaction('<a:loading:716280480579715103>')
        money = await darealmodule.Money.get_money(self, ctx, ctx.author.id)

        async def gen_random():
            return random.choice(["Oh hey, I found your profile and uh a cat?",
            "Hey, I've missed you, dw I got your profile down here."])

        embed=discord.Embed(title=f"{await gen_random()}", description=f'<:catbox:719527304476491858> You have **`${money}`** in your account.\nUse `{ctx.prefix}help Games` to view a list of commands to earn money.', color=0x2f3136)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=['lb'], help='Place Holder')
    @has_profile()
    async def leaderboard(self, ctx):
        """
        Place Holder
        """
        await ctx.message.add_reaction('<a:loading:716280480579715103>')
        user = await ctx.cog.bot.pg_con.fetch("SELECT discord_id, money FROM profiles WHERE guild_id = $1", ctx.guild.id)
        users_money = {}
        for i in user:
            users_money[int(i['discord_id'])] = int(i['money'])
        
        dicts = dict(sorted(users_money.items(), key=operator.itemgetter(1),reverse=True))

        embed=discord.Embed(title=":tada: TOP 3 MEMBERS :tada:.", color=0x2f3136)

        user_index = list(dicts.keys()).index(ctx.author.id)

        num = 1
        for i in dicts:
            if num == 5:
                break
            user = ctx.guild.get_member(i)
            # await ctx.send(f'{user}, {i[1]}')
            if num == 1:
                embed.add_field(name=f'**1ST PLACE**', value=f'*{user.mention}**:** `${dicts[i]}`*', inline=False)
            if num == 2:
                embed.add_field(name=f'**2ND PLACE**', value=f'*{user.mention}**:** `${dicts[i]}`*', inline=False)
            if num == 3:
                embed.add_field(name=f'**3RD PLACE**', value=f'*{user.mention}**:** `${dicts[i]}`*', inline=False)
            if num == 4 and user_index not in [0, 1, 2, 3]:
                embed.add_field(name=f'**YOUR POSITION ({user_index}TH PLACE)**', value=f'*{ctx.author.mention}**:** `${dicts[i]}`*', inline=False)
            num += 1

        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(ctx.cog, ctx))
        await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
