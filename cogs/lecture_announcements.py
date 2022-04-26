from discord.ext import commands

from bot import client


class Lecture_Announcements(commands.Cog):
    def __init__(self, client):
        self.client = client



    #Commands
    @commands.command(aliases=['lecture'])
    async def define_new_lecture(self, ctx):
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in '✅'

        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        await ctx.send('Check on which day of the week is your lecture')
        for item in days_of_week:
            msg = await ctx.send(item)
            await msg.add_reaction(emoji="✅")
        reaction = await client.wait_for("reaction_add", check=check)  # Wait for a reaction
        await ctx.send(f"You reacted with: {reaction[0]}")  # With [0] we only display the emoji

    @define_new_lecture.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('The command does not take any arguments')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')



    #Events
    @commands.Cog.listener()  # function decorator
    async def on_ready(self):
        print('Lecture announcements cog is loaded.')





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