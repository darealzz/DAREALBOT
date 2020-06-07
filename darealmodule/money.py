import discord
from discord.ext import commands
import time
import sys
import os
import datetime
import random


class Money():

    async def get_money(self, ctx, author_id):
        return await ctx.cog.bot.pg_con.fetchval("SELECT money FROM profiles WHERE discord_id = $1", author_id)

    async def calculate_random_remove(self, ctx, author_id, min, max):
        user_money = await Money().get_money(ctx, author_id)
        nums = range(min, max)

        percent = random.choice(nums)
        percent = int(percent)
        
        return round(((user_money / 100) * percent))

    async def remove_ammount(self, ctx, author_id, ammount):
        user_money = await Money().get_money(ctx, author_id)
        ammount = user_money - ammount
        await ctx.cog.bot.pg_con.execute("UPDATE profiles SET money = $1 WHERE discord_id = $2", ammount, author_id)