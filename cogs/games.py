import discord
from discord.ext import commands
import time
import sys
import os
import json
from classes.helping import Helping
import random

class Games(commands.Cog):
    """This module allows you to play games and earn money."""


    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:games:713878668836995073>'
        self.thumbnail = 'https://cdn.discordapp.com/attachments/711529920349732909/713879222648832070/emoji.png'
        self.helping = Helping()

    def has_profile():
        async def predicate(ctx):
            user = await ctx.cog.bot.pg_con.fetch("SELECT * FROM roblox WHERE discord_id = $1", ctx.author.id)
            if not user:

            # await ctx.send(type(f"{ctx.author.id}"))
            # await ctx.send(data[f"{ctx.author.id}"])
            if f"{ctx.author.id}" not in data:
                embed=discord.Embed(title="You need to create a profile first.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}create` to create your profile.', color=0x36393E)
                embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
                await ctx.send(embed=embed)
                raise discord.ext.commands.CommandNotFound
            else:
                return True
        return commands.check(predicate)


    @commands.command()
    @commands.is_owner()
    @has_profile()
    async def turtle(self, ctx):

        """Command restricted for owner usage until command is finished."""

        board=[
        ['+', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', '\n'],
        ['+', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', '\n'],
        ['+', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', '\n'],
        ['+', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', '\n'],
        ]
        main_board=""
        for i in board:
            for char in i:
                main_board+=f"{char}"

        embed=discord.Embed(title="The Turtle Game.", description=f"""
```diff
{main_board}
```
"""
        , color=0x36393E)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=Helping().get_footer(ctx))
        message = await ctx.send(embed=embed)


        def board_check():
            winner_count=0
            for i in board:
                for char in i:
                    if char == '-':
                        winner_count+=1

                if winner_count != 0:
                    pass
                else:
                    return True
        finished = 'No1'
        async def finish_check():
            if board_check() == True:
                finished = 'Yes'

        while finished != 'Yes':
            row = random.randint(1, 4)
            row -= 1
            old_value = (board[row].index('+'))
            new_value = old_value + 2
            board[row][new_value]='+'
            board[row][old_value]=''
            main_board=""
            for i in board:
                for char in i:
                    main_board+=f"{char}"
            embed.description=f"""
```diff
{main_board}
```
"""
            await message.edit(embed=embed)
            await finish_check()





def setup(bot):
    bot.add_cog(Games(bot))
