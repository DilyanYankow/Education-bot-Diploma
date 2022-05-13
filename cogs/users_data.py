import asyncio
import json

import discord
from discord import guild
from discord.ext import commands

from bot import client


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
        if len(before.roles) < len(after.roles):
            new_role = next(role for role in after.roles if role not in before.roles)
            if new_role.name in ('Student'):
                msg = "Hello there, you now have the Student role.\nYou can use the command: student_number " \
                      "to let your lecturers extract it more easilly" \
                      "\nExample: !student_number 1234567890"
                await send_DM(after, msg)
            elif new_role.name in ('Teacher'):
                pass

    # Commands
    @commands.command(aliases=['student_number'])
    @commands.dm_only()
    async def set_student_number(self, ctx, *, stu_number):
        def check(react, user):
            return user == ctx.message.author and str(react.emoji) in '✅'

        msg = await ctx.send(f'This will be set as your faculty number: {stu_number}. Proceed?')
        await msg.add_reaction(emoji="✅")
        await msg.add_reaction(emoji="❎")
        reaction = await client.wait_for("reaction_add", check=check, timeout=15)  # Wait for a reaction
        await ctx.send(f"You reacted with: {reaction[0]}")  # With [0] we only display the emoji
        # await ctx.send(f'{reaction[0]}, {reaction}')
        if reaction[0].emoji == '✅':
            with open('stu_info.json', 'r') as f:
                stu_num = json.load(f)
            stu_num["Student_num"] = stu_number
            with open('stu_info.json', 'w') as f:
                prefixes = json.load(f)
            await ctx.send(f'Student number changed to: {stu_number}')
        else:
            await ctx.send(f'{reaction[0]}, {reaction}')


def setup(client):
    client.add_cog(Users_Data(client))
