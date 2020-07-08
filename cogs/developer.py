import discord
from discord.ext import commands
import time
import sys
import os
import darealmodule

class Developer(commands.Cog):
    """These commands has been reserved for the ownership team to streamline development."""
    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:Owner:718138683684945952>'
        self.thumbnail = 'https://media.discordapp.net/attachments/714855923621036052/718138457540657202/433918.png?width=499&height=499'

    @commands.command(description="Owner only.", help='Loads the given cog, if it already loaded it will raise an error.')
    @commands.is_owner()
    async def load(self, ctx, extension):
        """
        Loads specified cog.
        """
        try:
            self.bot.load_extension(f"cogs.{extension}")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog already loaded: `{extension}`**")
        else:
            await ctx.send(f"<:check:711530148196909126> | **Loaded Cog: `{extension}`**")

    @commands.command(description="Owner only.", help='Reloads the given cog, if an error is raised it will not load again.')
    @commands.is_owner()
    async def reload(self, ctx, extension):
        """
        Reloads specified cog.
        """
        try:
            self.bot.unload_extension(f"cogs.{filename[:-3]}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{extension}`**")
        else:
            self.bot.load_extension(f"cogs.{filename[:-3]}")
            await ctx.send(f"<:check:711530148196909126> | **Realoded Cog: `{extension}`**")

    @commands.command(description="Owner only.", help='Unloads the given cog, if it already unloaded it will raise an error.')
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """
        Unloads specified cog.
        """
        try:
            self.bot.unload_extension(f"cogs.{extension}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{extension}`**")
        else:
            await ctx.send(f"<:check:711530148196909126> | **Unloaded Cog: `{extension}`**")

    @commands.command(description="Owner only.", help='Reloads all cogs buy unloading and loading each cog, if an error is raised the cog will not be loaded.')
    @commands.is_owner()
    async def r(self, ctx):
        """
        Reloads all cogs.
        """

        embed=discord.Embed(title="a", color=0x2f3136)
        # embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        # await ctx.send(embed=embed)
        # return
        description=""
        loaded=0
        not_loaded=0
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.unload_extension(f"cogs.{filename[:-3]}")
                except commands.errors.ExtensionNotLoaded:
                    description += f"<:warningerrors:713782413381075536> | **Cog not loaded: `{filename[:-3]}`**\n"
                    not_loaded+=1
                else:
                    self.bot.load_extension(f"cogs.{filename[:-3]}")
                    description += f"<:check:711530148196909126> | **Realoded Cog: `{filename[:-3]}`**\n"
                    loaded+=1

                    # await ctx.send(f"<:check:711530148196909126> | **Realoded Cog: `{filename[:-3]}`**")
        #await ctx.send(f"<:check:711530148196909126> | `Reloaded the cogs`")
        embed.title=f'{loaded} modules where loaded & {not_loaded} modules where not loaded.'
        embed.description=description
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.send(embed=embed)

    @commands.command(description="Owner only.", help='Sends a list of all loaded cogs, events and unloaded cogs will be skipped.')
    @commands.is_owner()
    async def cogs(self, ctx):
        """
        Shows all cogs.
        """
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.send(f"`{filename[:-3]}`")


    @commands.group(aliases=['dm'], help='Unloads/Reloads the error handler file, respective to the subcommand, meaning errors being handled will not be sent.')
    @commands.is_owner()
    async def debugmode(self, ctx):
        """
        Bots mode respective to the subcommand.
        """
        pass
        # self.bot.unload_extension(f"events.errors")
        #
        # await ctx.send(f"<:check:711530148196909126> | **Bot has been changed to debuging mode.**")

    @debugmode.command(name='-on', help='Unloads the error handler file.')
    async def _on(self, ctx):
        """
        Changes bot to debug mode.
        """
        try:
            self.bot.unload_extension(f"events.errors")
            await ctx.send(f"<:check:711530148196909126> | **Bot has been changed to debuging mode.**")
        except:
            await ctx.send(f"<:rcross:711530086251364373> | **The bot is already in debug mode.**")

    @debugmode.command(name='-off', help='Loads the error handler file.')
    async def _off(self, ctx):
        """
        Turns debug mode off.
        """
        try:
            self.bot.load_extension(f"events.errors")
            await ctx.send(f"<:check:711530148196909126> | **Debuging mode has been turned off.**")
        except:
            await ctx.send(f"<:rcross:711530086251364373> | **Debug mode is already off.**")

    @commands.command(help='asd')
    @commands.is_owner()
    async def lad(self, ctx, member: discord.Member, badge):
        """
        Adds a badge to a user.
    `   """

        badges = ['developer_badge', 'staff_badge', 'partner_badge']
        if badge.lower() not in badges:
            embed=discord.Embed(title="Badge not found.", description=f'<:warningerrors:713782413381075536> No badges found with the name of `{badge}`.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)
            await ctx.send(embed=embed)
            return

        x = await ctx.cog.bot.pg_con.fetchval(f"SELECT discord_id FROM badges WHERE discord_id = $1", member.id)
        if not x:
            await self.bot.pg_con.execute("INSERT INTO badges (discord_id, developer_badge, staff_badge, partner_badge) VALUES ($1, FALSE, FALSE, FALSE)", member.id)

        has = await ctx.cog.bot.pg_con.fetchval(f"SELECT {badge} FROM badges WHERE discord_id = $1", member.id)
        if has == True:
            embed=discord.Embed(title="User already has this badge.", description=f'<:warningerrors:713782413381075536> This user already has the `{badge}` badge.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)
            await ctx.send(embed=embed)
            return

        await self.bot.pg_con.execute(f"UPDATE badges SET {badge}=TRUE WHERE discord_id = $1", member.id)

        embed=discord.Embed(title="Badge added successfully.", description=f"<:check:711530148196909126> {badge} was added to {member}'s profile.", color=0x2f3136)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.message.remove_reaction('<a:loading:716280480579715103>', self.bot.user)
        await ctx.send(embed=embed)
        return

def setup(bot):
    bot.add_cog(Developer(bot))
