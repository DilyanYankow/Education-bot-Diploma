import discord
from discord.ext import commands
import discord.utils

from bot import client


class Set_Roles(commands.Cog):
    def __init__(self, client):
        self.client = client


    # Events
    @commands.Cog.listener()  # function decorator
    async def on_ready(self):
        print('create roles cog is ready.')

    # Commands


    @commands.command(aliases=['setup_roles',])
    async def role_set(self, ctx):
        def check(react, user):
            return user == ctx.message.author and str(react.emoji) in '✅'

        msg = await ctx.send('This command will create roles for the server.\nAre you sure you wish to proceed?')
        await msg.add_reaction(emoji="✅")
        await msg.add_reaction(emoji="❎")
        reaction = await client.wait_for("reaction_add", check=check, timeout=15)  # Wait for a reaction
        if reaction[0].emoji == '✅':
            server = ctx.message.guild
            permStu = discord.Permissions(send_messages=True, read_messages=True, create_instant_invite=False,
                                          use_external_emojis=False)
            await server.create_role(name='Student', permissions=permStu)
            permTeach = discord.Permissions(send_messages=True, read_messages=True, create_instant_invite=True,
                                            kick_members=True, ban_members=True,
                                            manage_messages=True, mute_members=True,
                                            deafen_members=True, move_members=True)
            await server.create_role(name='Teacher', permissions=permTeach)
            await ctx.send("The roles Teacher and Student have been created.")

        else:
            await ctx.send("Roles won't be created")

    # Functions

def setup(client):
    client.add_cog(Set_Roles(client))