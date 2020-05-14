# Discord bot (I use Arch btw) for Linux Galore.
# Will manage some server moderation and pull Arch wiki pages on request.
import discord
from discord.ext import commands
import os
import json

os.chdir(r'/home/mewtastic/Code/Git/ArchBot')

with open("secrets.json") as f:
    secrets = json.loads(f.read())

client = commands.Bot(command_prefix='!')

# Set acticity
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Searching for !help'))
    print('ready')

# Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('```Missing required role```')


# Moderation commands.
@client.command()
async def ping(ctx):
    await ctx.send(f'```Bot Latency: {round(client.latency * 1000)}ms```')


@client.command(hidden=True)
@commands.has_role(709561120070959205)
async def purge(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@client.command(hidden=True)
@commands.has_role(709561120070959205)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'```Kicked {member.name}#{member.discriminator}```')


@client.command(hidden=True)
@commands.has_role(709561120070959205)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'```Banned {member.name}#{member.discriminator}```')


@client.command(hidden=True)
@commands.has_role(709561120070959205)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'```Unbanned {user.name}#{user.discriminator}```')
            return


####################################################
#                LEVELING SYSTEM                   #
####################################################

@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author)

    with open('users.json', 'w') as f:
        json.dump(users, f)
    # Execute additional commands
    await client.process_commands(message)


async def update_data(users, user):
    if str(user.id) not in users:
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1


async def add_experience(users, user, exp):
    users[str(user.id)]['experience'] += exp


async def level_up(users, user):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_end > lvl_start:

        role1 = 709873263525757060
        role2 = 709878333067755530
        role3 = 709880222383603803
        role4 = 709880475635679263
        role5 = 709880891341799505

        channel = client.get_channel(710264223523012648)
        await channel.send('{} has reached level {}'.format(user.mention, lvl_end))

        users[str(user.id)]['level'] = lvl_end
        if lvl_end == 5:
            await user.add_roles(role2)
            await user.remove_roles(role1)
        elif lvl_end == 10:
            remove = [role1, role2]
            await user.add_roles(role3)
            await user.remove_roles(remove)
        elif lvl_end == 15:
            remove = [role1, role2, role3]
            await user.add(role4)
            await user.remove_roles(remove)
        elif lvl_end == 20:
            remove = [role1, role2, role3, role4]
            await user.add(role5)
            await user.remove(remove)


client.run(secrets["archbot"]["token"])