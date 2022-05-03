import discord
from discord.ext import commands

class Create_Channels(commands.Cog):
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

    # Functions
    async def create_announcements_channel(self, ctx, channel_name):
        guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, write_messages=False),
            guild.me: discord.PermissionOverwrite(write_messages=True)
        }
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)


def setup(client):
    client.add_cog(Create_Channels(client))