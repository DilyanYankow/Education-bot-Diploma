import asyncio

import discord
from discord.ext import commands
from bot import client

class Set_Channels(commands.Cog):
    def __init__(self, client):
        self.client=client

    # Events
    @commands.Cog.listener()        #function decorator
    async def on_ready(self):
        print('Bot is online.')

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


    @commands.command(aliases=['setup_channels'])
    async def create_bot_channels(self, ctx):
        guild = ctx.guild
        def check(react, user):
            return user == ctx.message.author and str(react.emoji) in emojis

        msg = await ctx.send('This command will create roles for the server.\nAre you sure you wish to proceed?')
        emojis = ["✅", '❎']
        for emoji in (emojis):
            await msg.add_reaction(emoji)

        try:
            reaction = await client.wait_for("reaction_add", check=check, timeout=15)  # Wait for a reaction
        except asyncio.TimeoutError:
            await ctx.send("Time out")
        else:
            if reaction[0].emoji == '✅':
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=True, send_messages=False),
                    discord.utils.get(guild.roles, name = "Student"): discord.PermissionOverwrite(view_channel=True, send_messages=False),
                    discord.utils.get(guild.roles, name = "Teacher"): discord.PermissionOverwrite(view_channel=True, send_messages=False)
                }
                channelAnnounce = await guild.create_text_channel('announcements', overwrites=overwrites)
                if channelAnnounce:  # If a channel exists with the name
                    await channelAnnounce.send('Channel is now open!')

                overwritesEduBot = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
                    discord.utils.get(guild.roles, name = "Student"): discord.PermissionOverwrite(view_channel=False, send_messages=False),
                    discord.utils.get(guild.roles, name = "Teacher"): discord.PermissionOverwrite(view_channel=True, send_messages=True)
                }
                channelCommands = await guild.create_text_channel('bot-commands', overwrites=overwritesEduBot)
                if channelCommands:  # If a channel exists with the name
                    await channelCommands.send('Channel is now open!')
            elif reaction[0].emoji == '❎':
                await ctx.send("Channels won't be created")

# Functions
def setup(client):
    client.add_cog(Set_Channels(client))