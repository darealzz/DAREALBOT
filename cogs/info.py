import discord
from discord.ext import commands
import time
import sys
import os
import datetime

class EmbedHelpCommand(commands.HelpCommand):

    COLOUR = 0x36393E

    def get_ending_note(self):
        now = datetime.datetime.now()
        return f'[-] Use {0}{1} [command] for more info on a command.\n[-] Icons made by Freepik, www.flaticon.com\nInvoked by {self.context.author} @ {now.hour}:{now.minute}'.format(self.clean_prefix, self.invoked_with)

    def get_opening_note(self):
        return f"""```diff
- [] = optional argument
- <> = required argument
- Do NOT type these when using commands!
+ Type {self.clean_prefix}{self.invoked_with} [command | module] for more help on a command or module
```
        """

    def get_command_signature(self, command):
        return '{0.qualified_name} {0.signature}'.format(command)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='HELP PANNEL', description=self.get_opening_note(), colour=self.COLOUR)
        description = self.context.bot.description
        if description:
            embed.description = description
        cogs = ""
        for cog in self.context.bot.cogs.values():
            # if cog == 'OwnerOnly':
            #     cog=''
            try:
                # cogs += '• '
                cogs += f'• {cog.icon}'
                cogs += ' '
                cogs += cog.qualified_name
                cogs += '\n'
            except AttributeError:
                pass

        cogs += '\n\n'
            # name = 'No Category' if cog is None else cog.qualified_name
            # filtered = await self.filter_commands(commands, sort=True)
            # if filtered:
            #     value = '\u2002'.join(f'`{c.name}`' for c in commands)
            #     if cog:
            #         value = '{0}'.format(value)


        embed.add_field(name='Enabled Modules', value=cogs, inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):

        embed = discord.Embed(title='{0.qualified_name} Commands'.format(cog), colour=self.COLOUR)
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name, colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)


    send_command_help = send_group_help

class Info(commands.Cog):

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = EmbedHelpCommand()
        bot.help_command.cog = self
        self.bot = bot
        self.icon = "<:info:712000699600339015>"

    @commands.command(description="Displays the average webstock latency.")
    async def ping(self, ctx):
        """
        test
        """
        lst=[]
        for i in range(3):
            lst.append(round(self.bot.latency*1000))


        embed=discord.Embed(title="PONG", color=0x14cfa0)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url_as(format="png"))
        embed.add_field(name=f"Average websocket latency", value=f":ping_pong: | `{lst[0]}ms`", inline=False)
        embed.set_footer()
        await ctx.send(embed=embed)

    # def cog_unload(self):
    #     self.bot.help_command = self._original_help_command
def setup(bot):
    bot.add_cog(Info(bot))
