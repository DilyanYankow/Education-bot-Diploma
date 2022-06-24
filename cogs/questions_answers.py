import asyncio, discord
from discord.ext import commands
from datetime import datetime
from bot import is_botchannel, set_info
from cogs.users_data import send_DM
from bot import client

class Questions_Answers(commands.Cog):
    def __init__(self, client):
        self.client=client

    #Events
    @commands.Cog.listener()        #function decorator
    async def on_ready(self):
        print('Q&A cog is ready.')

    #Commands
    @commands.command(aliases=['question'])
    @commands.check(is_botchannel)
    async def start_question(self, ctx, *, question):
        author = ctx.message.author
        channel = discord.utils.get(ctx.guild.text_channels, name="questions")
        try:
            arch_channel = discord.utils.get(ctx.guild.text_channels, name="answer-archives")
            if arch_channel:
                await arch_channel.send(file=discord.File(r'student_answers.txt'))
                file = open("student_answers.txt", "w") #these 2 lines will
                file.close()                            #delete all the text in the file
            if channel:  # If a channel exists with the name
                embed = discord.Embed(color=discord.Color.dark_gold(), timestamp=ctx.message.created_at)
                embed.set_author(name="Question", icon_url=self.client.user.avatar_url)
                embed.add_field(name=f"Sent by {ctx.message.author}", value=str(question), inline=False)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
                await ctx.message.add_reaction(emoji="✅")
                await channel.send(embed=embed)

                user_channel = author.voice.channel
                if user_channel:        # If user is in a channel
                    members = user_channel.members  # finds members connected to the channel
                    attendees = []  # (list)
                    for member in members:
                        if member != author:
                            attendees.append(member.name)
                            await send_DM(member, 'There is a new question in the Questions channel.'
                                            'You can submit an answer via the command !answer\n'
                                            'Example: !answer YourAnswerHere')
                    await ctx.send(f'Sent DM to the students: {attendees}')
                else:
                    await ctx.send("Writer is not in a channel, DM's will not be sent to students")  # If the writer is not in a discord channel
        except Exception as e:
            print(e)

    @commands.command(aliases=['get_answers'])
    @commands.check(is_botchannel)
    async def send_answers_file(self, ctx):
        try:
            answers_channel = discord.utils.get(ctx.guild.text_channels, name="answers")
            if answers_channel:
                await answers_channel.send(file=discord.File(r'student_answers.txt'))
        except Exception as e:
            print(e)



    @commands.command(aliases=['answer'])
    @commands.dm_only()
    async def answer_question(self, ctx, *, answer):
        def check(react, user):
            return user == ctx.message.author and str(react.emoji) in emojis

        msg = await ctx.send(f'Your answer will be recorded as: {answer}. at the current time. Proceed?')
        emojis = ["✅", '❎']
        for emoji in (emojis):
            await msg.add_reaction(emoji)
        try:
            reaction = await client.wait_for("reaction_add", check=check, timeout=15)  # Wait for a reaction
        except asyncio.TimeoutError:
            await ctx.send("Time out")
        else:
            if reaction[0].emoji == '✅':
                try:
                    with open('student_answers.txt', 'a') as f:
                        f.write(f'Time: {datetime.now().strftime("%D:%H:%M:%S")}, User: {ctx.message.author}, Answer: {answer}\n')
                except Exception as e:
                    print(e)
              #  set_answer(ctx.message.author, answer)
                await ctx.send(f'Answer set as: {answer}')



def setup(client):
    client.add_cog(Questions_Answers(client))