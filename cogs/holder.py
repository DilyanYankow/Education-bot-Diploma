import discord
from discord.ext import commands

class Holder(commands.Cog):
    def __init__(self, client):
        self.client=client

    #Events
    @commands.Cog.listener()        #function decorator
    async def on_ready(self):
        print('Bot is online.')

    #Commands



def setup(client):
    client.add_cog(Holder(client))