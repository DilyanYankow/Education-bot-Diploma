import asyncio
import json

import discord
from discord import guild
from discord.ext import commands

from bot import client, set_info, get_info, is_botchannel, isTeacher


async def send_DM(user, content):
    await user.send(f'{content}')


class Users_Data(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()  # function decorator
    async def on_ready(self):
        print('Users data cog is online.')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        set_info(after, after.guild.name)
        if len(before.roles) < len(after.roles):
            new_role = next(role for role in after.roles if role not in before.roles)
            if new_role.name in ('Student'):
                msg = "Hello there, you now have the Student role.\nYou can use the command: student_number " \
                      "to let your lecturers extract it more easilly" \
                      "\nExample: !student_number 1234567890"
                set_info(after, 0)
                await send_DM(after, msg)


    # Commands
    @commands.command(aliases=['student_number'])
    @commands.dm_only()
    async def set_student_number(self, ctx, stu_number):
        def check(react, user):
            return user == ctx.message.author and str(react.emoji) in emojis

        msg = await ctx.send(f'This will be set as your faculty number: {stu_number}. Proceed?')
        emojis = ["✅", '❎']
        for emoji in (emojis):
            await msg.add_reaction(emoji)
        try:
            reaction = await client.wait_for("reaction_add", check=check, timeout=15)  # Wait for a reaction
        except asyncio.TimeoutError:
            await ctx.send("Time out")
        else:
            if reaction[0].emoji == '✅':
                set_info(ctx.message.author, stu_number)
                await ctx.send(f'Student number changed to: {stu_number}')
            else:
                await ctx.send('Student number wont be changed.')


    @commands.command(aliases=['my_student_number', 'my_number'])
    @commands.dm_only()
    async def get_my_student_info(self, ctx):
            my_number = get_info(ctx.message.author)
            await ctx.send(f'Your student number is: {my_number}')

    @commands.command(aliases=['get_student_number'])
    @commands.check(is_botchannel)
    async def get_student_info(self, ctx):
        my_number = get_info(ctx.message.author)
        await ctx.send(f'Student number of the member is: {my_number}')
def setup(client):
    client.add_cog(Users_Data(client))
