from typing import List
import discord
import chatbot
import json
from discord.ext import commands

# Contains tokens and stuff
from reddit import grab_good_post

with open("secrets.json") as f:
    secrets = json.loads(f.read())

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Searching for !help'))
    print('We have logged in as {0.user}'.format(client))


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


async def level_up(users, user: discord.member.Member):
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
        if users[str(user.id)]["level"] != 4:
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
        elif lvl_end == 20 and users[str(user.id)]["level"] != 4:
            remove = [role1, role2, role3, role4]
            await user.add(role5)
            await user.remove(remove)
        # print(type(users[str(user.id)]["level"]))
# END OF LEVELING SYSTEM

# Start of Evil Hacker's Code

@client.command()
async def reddit(ctx, subreddit):
    post = grab_good_post(subreddit)
    await ctx.send(post[0] + " | " + post[1])


@client.event
async def on_raw_reaction_add(reaction):
    if not reaction.message_id == 709827022800683038:
        guild = client.get_guild(reaction.guild_id)
        readme: discord.TextChannel = guild.get_channel(709580982688153621)
        message: discord.Message = await readme.fetch_message(709897964771999816)
        check = message.reactions
        for i in check:
            if i.emoji == "✅":  # There IS a char there, but my IDE doesn't display it.
                if len(reaction.member.roles) < 2:
                    await reaction.member.add_roles(discord.utils.get(guild.roles, id=709873263525757060))
            else:
                await message.remove_reaction(reaction.emoji, reaction.member)

    role: str = reaction.emoji.name
    roles = {"arch": 709562148342202368,
             "gentoo": 709599034486292482,
             "debian": 709572442858848256,
             "fedora": 709572559280275548,
             "manjaro": 709572766596202597,
             "mint": 709572667560165458,
             "pop": 709829747089211402,
             "ubuntu": 709568934600507553,
             "windoze": 709608463399125033,
             "vim": 709572199488684134,
             "emacs": 709572338009767977}
    msg = await client.get_channel(709800728008327238).fetch_message(709827022800683038)
    if role not in roles.keys():
        await msg.remove_reaction(reaction.emoji, reaction.member)
        return

    guild = client.get_guild(reaction.guild_id)

    readme: discord.TextChannel = guild.get_channel(709580982688153621)
    message: discord.Message = await readme.fetch_message(709897964771999816)
    check = message.reactions
    check_box = None
    for i in check:
        if i.emoji == "✅":  # There IS a char there, but my IDE doesn't display it.  It's
            check_box = i
    if not check_box:
        return
    users = await check_box.users().flatten()
    if reaction.member.name in list(map(lambda x: x.name, users)):
        role = discord.utils.get(guild.roles, id=roles[role])
        await reaction.member.add_roles(role)
    else:
        await msg.remove_reaction(reaction.emoji, reaction.member)
        await reaction.member.send("Please react with the checkbox in #readme")


client.run(secrets["rolebot"]["token"])
