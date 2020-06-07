from __future__ import annotations
import discord
from discord.ext import commands
import time
import sys
import os
import datetime
import darealmodule
class EmbedHelpCommand(commands.HelpCommand):

    COLOUR = 0x2f3136
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verify_checks = False

    def get_ending_note(self):
        now = datetime.datetime.now()
        if len(str(now.minute)  ) == 1:
            x = f"0{now.minute}"
        else:
            x = now.minute
        return f'[-] Invoked by {self.context.author} @ {now.hour}:{x}'.format(self.clean_prefix, self.invoked_with)

    def get_opening_note(self):
        return f"""```md
* All optional aurguments are wrapped with '[]'
* All mandatory aurguments are wrapped with '<>'
* {self.clean_prefix}{self.invoked_with} [command | module] for help on a command/module.
```
        """

    def get_command_signature(self, command):
        return '{0.qualified_name} {0.signature}'.format(command)
    def get_command_signature_name(self, command):
        return '{0.qualified_name}'.format(command)
    def get_author_icon(self):
        return f'{self.context.author.avatar_url_as(format="png")}'
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='<:balloons:714891302763757629> HELP PANNEL <:balloons:714891302763757629>', description=self.get_opening_note(), colour=self.COLOUR)
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
        about=f"""
*Dev*‏‏‎ ‎*-* ‎*`@dareal#2231`, `433293211436580874`*
*Dev* *-* *`@lolkm8#6312`, `644648271901622283`*
*Lib* ‎‏‎*-* ‏‏‏‎ ‎*[discord.py](https://github.com/Rapptz/discord.py)*, ‏‏‎ ‎*[docs](https://discordpy.readthedocs.io/en/latest)*
<:Invite:718152781747453952>__*[Click here to invite the bot to your server!](https://discord.com/api/oauth2/authorize?client_id=589075218606194699&permissions=8&scope=bot)*__
<:Join:718154643095683142>__*[Click here to join the support server!](https://discord.gg/M67zbB)*__
        """
        embed.add_field(name='**Enabled Modules**', value=cogs, inline=True)
        embed.add_field(name='**About**', value=about, inline=True)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed=discord.Embed(title="That command or module was not found.", description=f'<:warningerrors:713782413381075536> Please note that Modules and Commands are **`case sensetive`**.', color=0x2f3136)
        embed.set_footer(icon_url=self.context.author.avatar_url_as(format="png"), text=Helping().get_footer(self.context))
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        verify_checks=False
        cmds=""
        embed = discord.Embed(title=f'{(cog.qualified_name).upper()} MODULE', colour=self.COLOUR)
        # if cog.description:
        #     embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            cmds += f"`{(self.get_command_signature_name(command)).strip()}`"
            cmds += f" - "
            cmds += command.callback.__doc__.strip()
            cmds += '\n'
        embed.add_field(name=f'**{cog.__doc__}**', value=cmds, inline=False)
        embed.set_thumbnail(url=cog.thumbnail)
        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        self.verify_checks=False
        embed = discord.Embed(title=self.get_command_signature(group), colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc, inline=False)

        if len(group.aliases) != 0:
            aliases = ""
            for i in group.aliases:
                aliases+=f'`{i}`'
                aliases+=f'‏‏‎ ‎‏‏‎ ‎'
            embed.add_field(name='**Aliases**', value=aliases, inline=False)

        embed.set_thumbnail(url=group.cog.thumbnail)
        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)


    send_command_help = send_group_help

class Info(commands.Cog):

    """This Module allows give you reletive data about this bot."""

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = EmbedHelpCommand()
        bot.help_command.cog = self
        self.bot = bot
        self.icon = "<:Info:718139261328556032>"
        self.thumbnail = 'https://media.discordapp.net/attachments/714855923621036052/718139093531492392/433944.png?width=499&height=499'
        self.helping = darealmodule.Helping()
        self.global_check = False

    @commands.command(aliases=['p'] ,help="Displays the average webstock latency calculated from 3 requests.")
    async def ping(self, ctx):
        """
        Displays the average webstock latency.
        """
        lst=[]
        for i in range(3):
            lst.append(round(self.bot.latency*1000))


        embed=discord.Embed(title="PONG", color=0x2f3136)
        embed.add_field(name=f"Average websocket latency", value=f"<:Info:718139261328556032> | `{lst[0]}ms`", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=self.helping.get_footer(ctx))
        await ctx.send(embed=embed)

    # def cog_unload(self):
    #     self.bot.help_command = self._original_help_command
def setup(bot):
    bot.add_cog(Info(bot))
