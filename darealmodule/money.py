import discord
from discord.ext import commands
import time
import sys
import os
import datetime
import random


class Money():

    async def get_money(self, ctx, author_id):
        guild_id = ctx.guild.id
        return await ctx.cog.bot.pg_con.fetchval("SELECT money FROM profiles WHERE discord_id = $1 and guild_id = $2", author_id, guild_id)

    async def calculate_random_remove(self, ctx, author_id, min, max):
        user_money = await Money().get_money(ctx, author_id)
        nums = range(min, max)

        percent = random.choice(nums)
        percent = int(percent)

        return round(((user_money / 100) * percent))

    async def remove_ammount(self, ctx, author_id, ammount):
        guild_id = ctx.guild.id
        user_money = await Money().get_money(ctx, author_id)
        ammount_n = int(user_money) - int(ammount)
        await ctx.cog.bot.pg_con.execute("UPDATE profiles SET money = $1 WHERE discord_id = $2 and guild_id = $3", ammount_n, author_id, guild_id)
        return ammount

    async def calculate_random_add(self, ctx, author_id, min, max):
        user_money = await Money().get_money(ctx, author_id)
        nums = range(min, max)

        percent = random.choice(nums)
        percent = int(percent)

        return round(((user_money / 100) * percent))

    async def add_ammount(self, ctx, author_id, ammount):
        guild_id = ctx.guild.id
        user_money = await Money().get_money(ctx, author_id)
        ammount_n = int(user_money) + int(ammount)
        await ctx.cog.bot.pg_con.execute("UPDATE profiles SET money = $1 WHERE discord_id = $2 and guild_id = $3", ammount_n, author_id, guild_id)
        return ammount

    async def has_money(self, ctx, author_id, ammount):
        if await Money().get_money(ctx, author_id) >= ammount:
            return True
        else:
            return False
