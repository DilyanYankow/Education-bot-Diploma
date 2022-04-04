import random
import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='!')

    #Commands
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cog.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cog.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cog.{extension}')
    client.load_extension(f'cog.{extension}')

@client.command()
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.name}#{member.discord}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member.name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    #Events
@client.event
async def on_member_join(member):
    print(f'member has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'member has left the server.')

@client.event
async def on_ready():
    print('bot is ready.')

for filename in os.listdir('./cogs'):   #for each file in /cogs folder
    if filename.endswith('.py'):
        client.load_extension((f'cogs.{filename[:-3]}'))

client.run('OTU4Mjg4MDAwNzc1NzYxOTUw.YkLJPw.w1eInjK2VFEYgUWoMb7Fjw-477A')
