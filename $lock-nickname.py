import asyncio
import os

import discord
from discord import Color, Embed
from discord.ext import commands


class Utilities(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='lock-nickname')
    @commands.has_permissions(manage_nicknames=True)
    async def lock-nickname(self, ctx, member: discord.Member=None):
        """Restricts the user from changing their own nickname\nExample usage: `$lock-nickname @SlimShadyIAm#9999`"""
        
        if member is None:
            raise commands.BadArgument("Please supply a member, i.e `$lock-nickname @SlimShadyIAm#9999`")
        role = discord.utils.get(ctx.guild.roles, name="Nickname Restriction")
        if (role is None):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description='Nickname Restriction role not found!'))
            return
        
        await ctx.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Gave <@{member.id}> the Nickname Restriction role. They can no longer change their own nickname. To undo, use $unlock-nickname').set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url))
       
        try:
            await member.send(embed=embed)
            await member.add_roles(role)
        except discord.Forbidden:
            channel = discord.utils.get(ctx.guild.channels, name="general" if os.environ.get('PRODUCTION') == "false" else "off-topic")
            await asyncio.sleep(10)
            await member.add_roles(role)
        
        
        embed=Embed(title="Timeout finished.", color=Color(value=0x37b83b), description='Removed your timeout role. Please behave, or we will have to take further action.').set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        try:
            await member.send(embed=embed)
            await member.remove_roles(role)
        except discord.Forbidden:
            channel = discord.utils.get(ctx.guild.channels, name="general" if os.environ.get('PRODUCTION') == "false" else "off-topic")
            await channel.send(f'<@{member.id}> I tried to DM this to you, but your DMs are closed!', embed=embed)
            await member.remove_roles(role)
    
        await ctx.author.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Removed {member.name}\'s timeout role.').set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url))

    
    @rules.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))
        else:
            print(f'{error}')

def setup(bot):
    bot.add_cog(Utilities(bot))
