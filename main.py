import discord
from discord.ext import commands, tasks
import random
import os
import itertools
from cogs.info import EmbedHelpCommand



# class MyHelpCommand(commands.MinimalHelpCommand):
#     def get_command_signature(self, command):
#         return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)
bot = commands.Bot(command_prefix=['sudo.', 'Sudo.'], case_insensetive=True, help_command=EmbedHelpCommand())
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        bot.load_extension(f"events.{filename[:-3]}")

# bot.remove_command("help")





bot.load_extension('jishaku')



bot.run('NTg5MDc1MjE4NjA2MTk0Njk5.XslBpg.3kv-hEVyHvMwh2S9hlXgGWSB2Nk')
