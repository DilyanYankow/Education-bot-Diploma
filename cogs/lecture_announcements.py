import discord
from discord import client
from discord.ext import commands


class Lecture_Announcements(commands.Cog):
    def __init__(self, client):
        self.client = client



    #Commands
    @commands.command(aliases=['lecture'])
    @commands.has_permissions(manage_messages=True)
    async def define_new_lecture(self, ctx):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        await ctx.send('Check on which day of the week is your lecture')
        for item in days_of_week:
            msg = await ctx.send(item)
            await msg.add_reaction(emoji="✅")

    @define_new_lecture.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('The command does not take any arguments')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Invalid number of parameters')

    #Events
    @commands.Cog.listener()  # function decorator
    async def on_ready(self):
        print('Lecture announcements cog is loaded.')


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user != client.user:
            if str(reaction.emoji) == "✅":
                return
     #   if any(reaction.emoji == emoji for reaction in message.reactions):




#Functions
#     async def create_announcements_channel(self, ctx, channel_name):
#        guild = ctx.guild
 #       overwrites = {
  #          guild.default_role: discord.PermissionOverwrite(read_messages=True, write_messages=False),
   #         guild.me: discord.PermissionOverwrite(write_messages=True)
   #     }
   #     channel = await guild.create_text_channel(channel_name, overwrites=overwrites)

def setup(client):
    client.add_cog(Lecture_Announcements(client))