import discord
from discord.ext import commands, tasks
import time
import sys
import os
import json
import pathlib
import aiohttp
import darealmodule
try:
    import dbl
except:
    import dblpy

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU4OTA3NTIxODYwNjE5NDY5OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNTk0MjM2NjAwfQ.6Q5KIJF8EmLoRT-z7cYC-dM3V-AIBZCunhTkY6c0TgM' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='Lolcat101', webhook_port=5000, autopost=True) # Autopost will post your guild count every 30 minutes

    @commands.Cog.listener()
    async def on_guild_post(self):
        channel = await self.bot.fetch_channel(730394760363376670)
        await channel.send('Server count posted successfully to DBL, next post in 30 mins.')

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        channel = await self.bot.fetch_channel(730739315336019998)
        member = self.bot.fetch_user(data["id"])
        badge = 'voter_badge    '
        await channel.send(f'{member.mention} ({member.id}) has just voted! I have asigned the **voter** badge to this user...\nhttps://top.gg/bot/589075218606194699/vote')
        x = await ctx.cog.bot.pg_con.fetchval(f"SELECT discord_id FROM badges WHERE discord_id = $1", member.id)
        if not x:
            await self.bot.pg_con.execute("INSERT INTO badges (discord_id, developer_badge, staff_badge, partner_badge, voter_badge) VALUES ($1, FALSE, FALSE, FALSE, FALSE)", member.id)

        has = await ctx.cog.bot.pg_con.fetchval(f"SELECT {badge} FROM badges WHERE discord_id = $1", member.id)
        if has == True:
            return
        await self.bot.pg_con.execute(f"UPDATE badges SET {badge}=TRUE WHERE discord_id = $1", member.id)

    @tasks.loop(seconds=20)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.users)} Users"))

    @tasks.loop(seconds=40)
    async def change_statuss(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"DArealServers"))

    @tasks.loop(seconds=120)
    async def counter(self):

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

    @tasks.loop(hours=2)
    async def reddit_cache_update(self):

        self.bot.memes_cache = {} # Meme cache block
        subreddits = ['memes', 'dankmemes', 'blackpeopletwitter', 'MemeEconomy', 'wholesomememes']
        categories = ['rising', 'hot', 'top']

        for subreddit in subreddits:
            for category in categories:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f'https://www.reddit.com/r/{subreddit}/{category}.json') as r:
                        data = await r.json()

                        for i in data["data"]["children"]:
                            try:
                                self.bot.memes_cache[i["data"]["title"]] = [i["data"]["url"], f'r/{subreddit}/{category}']
                            except:
                                continue

        self.bot.cute_dog_cache = {} # Cute dog cache block
        subreddits = ['puppies']
        categories = ['rising', 'hot', 'top']

        for subreddit in subreddits:
            for category in categories:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f'https://www.reddit.com/r/{subreddit}/{category}.json') as r:
                        data = await r.json()

                        for i in data["data"]["children"]:
                            try:
                                link = i["data"]["url"]
                                link=link.split('/')
                                link[2] = 'i.imgur.com'
                                x = link[3].split('.')
                                if len(x) == 2:
                                    x.pop(1)
                                if x[0] != link[3]:
                                    link[3] = x[0]
                                link[3] += '.jpg'
                                link = '/'.join(link)
                                self.bot.cute_dog_cache[i["data"]["title"]] = [link, f'r/{subreddit}/{category}']
                            except:
                                continue

    async def testing_bot(self, ctx):
        return ctx.author.id == 433293211436580874 or ctx.author.id == 644648271901622283

    @commands.Cog.listener()
    async def on_ready(self):

        self.change_status.start()
        self.change_statuss.start()
        self.counter.start()
        self.reddit_cache_update.start()

        if self.bot.user.id == 711526390071296020:
            self.bot.add_check(self.testing_bot, call_once=True)
        else:
            pass


        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        x = self.bot.get_guild(699991602126389248)
        channel = x.get_channel(729432679266779186)
        embed = discord.Embed(description=guild.name, color=0x9aeb37)
        embed.add_field(name='\U0001f30f Region', value=guild.region, inline=False)
        embed.add_field(name='\U0001f646 Member Count', value=f'{len(guild.members)}', inline=False)
        embed.add_field(name='\U00002604\U0000fe0f Owner', value=f'{guild.owner.name}', inline=False)
        await channel.send(f'\U0001f424 **We have reached our {len(self.bot.guilds)}th server!** \U0001f424')
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))
