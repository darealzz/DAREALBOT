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

    async def get_badges(self, ctx, author_id):
        if not await ctx.cog.bot.pg_con.fetchval("SELECT * FROM badges WHERE discord_id = $1", author_id):
            return None

        badges = ""
        developer = await ctx.cog.bot.pg_con.fetchval("SELECT developer_badge FROM badges WHERE discord_id = $1", author_id)
        if developer == True:
            badges += '<:dev:730490030375829665> DArealBot Developer\n'
        staff = await ctx.cog.bot.pg_con.fetchval("SELECT staff_badge FROM badges WHERE discord_id = $1", author_id)
        if staff == True:
            badges += '<:staff:730489979058257951> DArealBot Staff\n'
        partner = await ctx.cog.bot.pg_con.fetchval("SELECT partner_badge FROM badges WHERE discord_id = $1", author_id)
        if partner == True:
            badges += '<:partner:730490002366005288> DArealBot Partner'
        if len(badges) == 0:
            return None
        else:
            return badges

