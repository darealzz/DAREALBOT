import discord
from discord.ext import commands, tasks
import time
import sys
import os
import json
import pathlib

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=20)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.users)} Users"))

        for i in await self.bot.pg_con.fetch("SELECT discord_id FROM blacklist"):
            if int(i['discord_id']) in self.bot.blacklist_cache:
                pass
            else:
                self.bot.blacklist_cache.append(int(i['discord_id']))

    @tasks.loop(seconds=40)
    async def change_statuss(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"DArealServers"))

    @tasks.loop(seconds=120)
    async def counter(self):
        guild = await self.bot.fetch_guild(699991602126389248)

        Files_channel = await self.bot.fetch_channel(719546043121008642)
        Lines_channel = await self.bot.fetch_channel(719546162436374628)
        Classes_channel = await self.bot.fetch_channel(719546254937423964)
        Functions_channel = await self.bot.fetch_channel(719546329281593386)
        Coroutines_channel = await self.bot.fetch_channel(719546488082006160)

        p = pathlib.Path('./')
        cm = cr = fn = cl = ls = fc = 0
        for f in p.rglob('*.py'):
            if str(f).startswith("venv"):
                continue
            fc += 1
            with f.open(encoding='utf8') as of:
                for l in of.readlines():
                    l = l.strip()
                    if l.startswith('class'):
                        cl += 1
                    if l.startswith('def'):
                        fn += 1
                    if l.startswith('async def'):
                        cr += 1
                    if '#' in l:
                        cm += 1
                    ls += 1
        await Files_channel.edit(name=f'Files: {fc}')
        await Lines_channel.edit(name=f'Lines: {ls}')
        await Classes_channel.edit(name=f'Classes: {cl}')
        await Functions_channel.edit(name=f'Functions: {fn}')
        await Coroutines_channel.edit(name=f'Coroutines: {cr}')
        # return f"file: {fc}\nline: {ls}\nclass: {cl}\nfunction: {fn}\ncoroutine: {cr}\ncomment: {cm}"

    async def globally_blacklist(self, ctx):
        if ctx.author.id in self.bot.blacklist_cache:
            await ctx.send('ure blacklisted moron')
        else:
            return True


    @commands.Cog.listener()
    async def on_ready(self):

        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')


        self.change_status.start()
        self.change_statuss.start()
        self.counter.start()

        self.bot.add_check(self.globally_blacklist, call_once=True)


def setup(bot):
    bot.add_cog(Events(bot))
