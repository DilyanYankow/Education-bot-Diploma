import discord
from discord.ext import commands
from bot import client

class Create_Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()  # function decorator
    async def on_ready(self):
        print('create roles cog is ready.')

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(aliases=['setup', 'setup_server'])
    async def setup_server(self, ctx):
        def check(react, user):
            return user == ctx.message.author and str(react.emoji) in '✅'

        msg = await ctx.send('This command will create roles for the server.\nAre you sure you wish to proceed?')
        await msg.add_reaction(emoji="✅")
        await msg.add_reaction(emoji="❎")
        reaction = await client.wait_for("reaction_add", check=check, timeout=15)  # Wait for a reaction
        if reaction[0].emoji == '✅':
            setup_roles()
        else:
                #else nothing
            true=True
    # Functions
    async def setup_roles(self, ctx):
        server = ctx.message.server
        permStu = discord.Permissions(send_messages=True, read_messages=True, create_invite=False, use_external_emoji=False, use_external_stickers=False, allowed_mentions=None)
        await client.create_role(server, name='Student', permissions=permStu)
        permTeach = discord.Permissions(send_messages=True, read_messages=True, create_invite=True, manage_nicknames=True, kick_members=True, ban_members=True, timeout_members=True, manage_messages=True, mute_members=True, deafen_members=True, move_members=True, manage_events=True)
        await client.create_role(server, name='Teacher', permissions=permTeach)

def setup(client):
    client.add_cog(Create_Roles(client))