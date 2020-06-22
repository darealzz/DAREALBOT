import discord
from discord.ext import commands, tasks
import random
import os
import itertools
import darealmodule
import os
import asyncpg
from cogs.info import EmbedHelpCommand

try:
    bot = commands.Bot(command_prefix=commands.when_mentioned_or(os.environ.get('DAREALBOT_DEFAULT_PREFIX')), case_insensetive=True, help_command=EmbedHelpCommand(command_attrs = {'help': 'asd'}), case_insensitive=True)
except:
    bot = commands.Bot(command_prefix=commands.when_mentioned_or('-'), case_insensetive=True, help_command=EmbedHelpCommand(command_attrs = {'help': 'asd'}), case_insensitive=True)

bot.blacklist_cache = []
bot.memes_cache = {}
bot.cute_dog_cache = []
bot.prefix_cache = {}

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        bot.load_extension(f"events.{filename[:-3]}")


async def create_db_pool():
    try:
        bot.pg_con = await asyncpg.create_pool(host="35.222.202.229", database="darealbot", user="postgres", password="Bestmate69")
    except asyncpg.exceptions.InvalidAuthorizationSpecificationError:
        bot.pg_con = await asyncpg.create_pool(host="localhost", database="darealbot", user="postgres", password="Bestmate69")



bot.loop.run_until_complete(create_db_pool())

bot.load_extension('jishaku')

try:
    bot.run(f"{os.environ.get('DAREAL_TOKEN')}")
except:
    bot.run(f"NTg5MDc1MjE4NjA2MTk0Njk5.Xu4mtg.bJCUx29OUqfSgQhNcA6wT3qMsR0")
