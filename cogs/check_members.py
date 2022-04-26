import discord
from discord import client
from discord.ext import commands


class Check_Members(commands.Cog):
    def __init__(self, client):
        self.client=client

    #Events
    @commands.Cog.listener()        #function decorator
    async def on_ready(self):
        print('Check members cog is loaded.')

    #Commands
    @commands.command(aliases=['attendees'])
    # async def check_members(self, ctx):
    async def attendees_list(self, ctx):
        author = ctx.message.author
        try:
            user_channel = author.voice.channel
            members = user_channel.members  # finds members connected to the channel
            if user_channel:  # If user is in a channel
                attendees = []  # (list)
                for member in members:
                    attendees.append(member.name)
                await ctx.send(f'{attendees}')
            else:
                await ctx.send("Writer is not in a channel")  # If the writer is not in a discord channel
        except AttributeError:
            return await ctx.send("User must be in the channel.")  # Error message



def setup(client):
    client.add_cog(Check_Members(client))
