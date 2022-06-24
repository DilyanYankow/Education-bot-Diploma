import asyncio, json, discord, os
from itertools import cycle
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions


def get_prefix(client, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            return prefixes[str(message.guild.id)]

    except KeyError:  # if the guild's prefix cannot be found in 'prefixes.json'
        with open('prefixes.json', 'r') as k:
            prefixes = json.load(k)
        prefixes[str(message.guild.id)] = 'bl!'

        with open('prefixes.json', 'w') as j:
            json.dump(prefixes, j, indent=4)

        with open('prefixes.json', 'r') as t:
            prefixes = json.load(t)
            return prefixes[str(message.guild.id)]

    except:  # I added this when I started getting dm error messages
        return '!'  # This will return "." as a prefix. You can change it to any default prefix.


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=get_prefix, intents=intents)
status = cycle(["Status 1", "Status 2"])

async def is_botchannel(ctx, chname='bot-commands'):
    return ctx.channel.name == chname

async def isTeacher(ctx):
    if ('Teacher' in ctx.message.author.roles or ctx.message.author.guild_permissions.administrator):
        return True
    return False

async def isAdmin(ctx):
    if ctx.message.author.guild_permissions.administrator:
        return True
    return False

# Commands
@client.command()
@commands.check(isAdmin)
async def load(ctx, extension):
    client.load_extension(f'cog.{extension}')


@client.command()
@commands.check(isAdmin)
async def unload(ctx, extension):
    client.unload_extension(f'cog.{extension}')


@client.command()
@commands.check(isAdmin)
async def reload(ctx, extension):
    client.unload_extension(f'cog.{extension}')
    client.load_extension(f'cog.{extension}')


@client.command()
@commands.check(isTeacher)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm']:
            return (int(amount), unit)

        raise commands.BadArgument(message="Not a valid duration")



@client.command(name='kick')
@has_permissions(kick_members=True)
async def kick(ctx, member: commands.MemberConverter, *, reason=None):
    await member.kick(reason=reason)


@kick.error
async def kick_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        print('1')
        await ctx.send('You have no permissions to use this command')
    if isinstance(error, commands.MemberNotFound):
        print('2')
        await ctx.send('Member not found')


@client.command()
async def ban(ctx, member: commands.MemberConverter, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.name}#{member.discord}')


@client.command()
@has_permissions(ban_members=True)
async def bantemp(ctx, member: commands.MemberConverter, duration: DurationConverter):
    multiplier = {'s': '1', 'm': 60}
    amount, unit = duration

    await ctx.guild.ban(member)
    await ctx.send(f'{member} has been banned for {amount}{unit}.')
    await asyncio.sleep(amount * multiplier[unit])
    await ctx.guild.unban(member)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Enter the number of messages you want to delete.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permissions to use this command.')


@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member.name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@client.command()
@commands.check(isAdmin)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'Prefix changed to: {prefix}')

    # Events


def set_info(member, fac_num):
    try:
        with open('stu_info.json', 'r') as f:
            stu_info = json.load(f)
        stu_info[str(member)] = str(fac_num)
        with open('stu_info.json', 'w') as f:
            json.dump(stu_info, f, indent=4)
    except Exception as e:
        print(e)

def get_info(member):
    try:
        with open('stu_info.json', 'r') as f:
            data = json.load(f)
        return data[str(member)]
    except Exception as e:
        print(e)


@client.event
async def on_member_join(member):
    set_info(member, member.guild.name)
    print(f'{member} has joined the server.')


@client.event
async def on_member_remove(member):
    #can pop his information from the json file but its more convenient not to make
    #people reenter their information upon rejoining
    print(f'member has left the server.')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("!help for commands"))
    change_status.start()

    print('bot is ready.')


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Tasks
@tasks.loop(seconds=10)  # preferably more than 5-10 sec
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))




for filename in os.listdir('./cogs'):  # for each file in /cogs folder
    if filename.endswith('.py'):
        client.load_extension((f'cogs.{filename[:-3]}'))

client.run('OTU4Mjg4MDAwNzc1NzYxOTUw.YkLJPw.w1eInjK2VFEYgUWoMb7Fjw-477A')
