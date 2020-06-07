import discord
from discord.ext import commands, tasks
import random
import os
import itertools
import darealmodule
import os
import asyncpg

TOKEN = os.environ.get('DAREAL_BOT_TOKEN')

bot = commands.Bot(command_prefix=['sudo.', 'Sudo.'], case_insensetive=True, help_command=EmbedHelpCommand())
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        bot.load_extension(f"events.{filename[:-3]}")


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(host="35.222.202.229", database="darealbot", user="postgres", password="Bestmate69")




bot.loop.run_until_complete(create_db_pool())

bot.load_extension('jishaku')

bot.run(f'{TOKEN}')
