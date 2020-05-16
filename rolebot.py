import discord
import json
from discord.ext import commands
from reddit import grab_good_post
from xkcd import get_url, get_random_url

# Contains tokens and stuff
with open("secrets.json") as f:
    secrets = json.loads(f.read())


admin = (709561120070959205, )
client = commands.Bot(command_prefix='!')

role1 = 709873263525757060
role2 = 709878333067755530
role3 = 709880222383603803
role4 = 709880475635679263
role5 = 709880891341799505
roles_table = (role1, role2, role3, role4, role5)

roles_channel_id = 709800728008327238
roles_post_id = 709827022800683038
readme_channel_id = 709580982688153621
readme_post_id = 709897964771999816
starter_role_id = 709873263525757060

distro_role_ids = {"arch": 709562148342202368,
                   "gentoo": 709599034486292482,
                   "debian": 709572442858848256,
                   "fedora": 709572559280275548,
                   "manjaro": 709572766596202597,
                   "mint": 709572667560165458,
                   "pop": 709829747089211402,
                   "ubuntu": 709568934600507553,
                   "windoze": 709608463399125033,
                   "vim": 709572199488684134,
                   "emacs": 709572338009767977,
                   "nano": 710984955299233793}


def get_guild(inp) -> discord.Guild:
    if type(inp) is commands.Context:
        return inp.guild
    if type(inp) is discord.Reaction:  # More to be added!
        return client.get_guild(inp.guild_id)
    raise TypeError(f"get_guild is not (yet) implemented for {type(inp)}")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Searching for !help'))
    print('We have logged in as {0.user}'.format(client))


# Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        # If user has insufficent perms for that command, tell them so
        await ctx.send('```Missing required role```')


# Moderation commands.
@client.command()
async def ping(ctx):
    await ctx.send(f'```Bot Latency: {round(client.latency * 1000)}ms```')


@client.command(hidden=True)
@commands.has_any_role(*admin)
async def purge(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@client.command(hidden=True)
@commands.has_any_role(*admin)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'```Kicked {member.name}#{member.discriminator}```')


@client.command(hidden=True)
@commands.has_any_role(*admin)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'```Banned {member.name}#{member.discriminator}```')


@client.command(hidden=True)
@commands.has_any_role(*admin)
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

@client.command()
async def level(ctx):
    """Command to get level"""
    with open('users.json', 'r') as f:
        users = json.load(f)
    user = ctx.message.author
    level = users[str(user.id)]["level"]
    await ctx.send(f'```You are level {level}```')


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
    await level_up(users, message.author, message)

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


async def level_up(users, user: discord.member.Member, message: discord.Message):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_end > lvl_start:
        channel = client.get_channel(710264223523012648)
        # if users[str(user.id)]["level"] != :
        if lvl_end in (5, 10, 15, 20):
            await channel.send(f"Congratulations {user.mention} for reaching level {lvl_end} and gaining perks!")
        else:
            await channel.send(f'{user.mention} has reached level {lvl_end}')

        guild = get_guild(message)

        def get_role(role_id): return discord.utils.get(guild.roles, id=role_id)

        converted = list(map(get_role, roles_table))

        users[str(user.id)]['level'] = lvl_end
        if lvl_end in (5, 10, 15, 20):
            remove = converted[:lvl_end // 5]
            await user.remove_roles(remove)
            await user.add_roles(converted[lvl_end // 5])


# END OF LEVELING SYSTEM

# Start of Evil Hacker's Code

@client.command()
async def reddit(ctx, subreddit):
    """Grabs one of the top media-containing posts from the specified subreddit"""
    post = grab_good_post(subreddit)
    if post is None:
        await ctx.send("No media posts were found in the top 20 :(")
    else:
        await ctx.send(post[0] + " | " + post[1])


@client.command()
async def xkcd(ctx, number=None):
    """Grabs an XKCD comic, random if no number is supplied"""
    try:
        if number is not None:
            int(number)
    except:
        await ctx.send("Please give a vailid number")
        return
    post = get_url(number) if number else get_random_url()
    await ctx.send(post)


@client.event
async def on_raw_reaction_add(reaction):
    guild = get_guild(reaction)
    readme: discord.TextChannel = guild.get_channel(readme_channel_id)
    readme_message: discord.Message = await readme.fetch_message(readme_post_id)
    if not reaction.message_id == roles_post_id:
        reactions = readme_message.reactions
        for i in reactions:
            if i.emoji == "✅":  # There IS a char there, but my IDE doesn't display it.
                if len(reaction.member.roles) < 2:
                    await reaction.member.add_roles(discord.utils.get(guild.roles, id=starter_role_id))
            else:
                await readme_message.remove_reaction(reaction.emoji, reaction.member)

    role: str = reaction.emoji.name
    msg = await client.get_channel(roles_channel_id).fetch_message(roles_post_id)
    if role not in distro_role_ids.keys():
        await msg.remove_reaction(reaction.emoji, reaction.member)
        return

    reactions = readme_message.reactions
    check_box = None
    for i in reactions:
        if i.emoji == "✅":  # There IS a char there, but my IDE doesn't display it.  It's
            check_box = i
    if not check_box:
        return
    users_who_reacted = await check_box.users().flatten()
    if reaction.member.name in list(map(lambda x: x.name, users_who_reacted)):
        role = discord.utils.get(guild.roles, id=distro_role_ids[role])
        await reaction.member.add_roles(role)
    else:
        await msg.remove_reaction(reaction.emoji, reaction.member)
        await reaction.member.send("Please react with the checkbox in #readme")


client.run(secrets["rolebot"]["token"])
