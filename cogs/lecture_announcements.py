import discord
from discord.ext import commands
import discord.utils

from bot import client


class Lecture_Announcements(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(aliases=['lecture', 'announce'])
    async def announce_lecture(self, ctx, *, message):
        def check(react, user):
            return user == ctx.message.author and str(react.emoji) in '✅'

        msg = await ctx.send('Are you sure you wish to make an announcement?')
        await msg.add_reaction(emoji="✅")
        await msg.add_reaction(emoji="❎")
        reaction = await client.wait_for("reaction_add", check=check, timeout=15)  # Wait for a reaction
        await ctx.send(f"You reacted with: {reaction[0]}")  # With [0] we only display the emoji
        # await ctx.send(f'{reaction[0]}, {reaction}')
        if reaction[0].emoji == '✅':
            await ctx.send("reaction.emoji == '✅' true")
            # Find a channel from the guilds `text channels` (Rather then voice channels)
            # with the name announcements
            channel = discord.utils.get(ctx.guild.text_channels, name="announcements")
            if channel:  # If a channel exists with the name
                embed = discord.Embed(color=discord.Color.dark_gold(), timestamp=ctx.message.created_at)
                embed.set_author(name="Announcement", icon_url=self.client.user.avatar_url)
                embed.add_field(name=f"Sent by {ctx.message.author}", value=str(message), inline=False)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
                await ctx.message.add_reaction(emoji="✅")
                await channel.send(embed=embed)
        else:
            await ctx.send(f'{reaction[0]}, {reaction}')

    # @announce_lecture.error
    # async def echo_error(self, ctx, error):
       # if isinstance(error, commands.MissingRequiredArgument):
         #   await ctx.send('The command takes 1 argument')
       # if isinstance(error, commands.MissingPermissions):
        #    await ctx.send('You do not have the permissions to use this command.')

    # Events
    @commands.Cog.listener()  # function decorator
    async def on_ready(self):
        print('Lecture announcements cog is loaded.')



def setup(client):
    client.add_cog(Lecture_Announcements(client))
