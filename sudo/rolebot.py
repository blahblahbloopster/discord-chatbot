import re
import duckduckgo
import discord
import json
from discord.ext import commands
import io
import os

print(os.path.abspath("."))
if os.path.abspath(".").split("/")[-1] != "discord_bot":
    os.chdir("../")

from sudo import leveling
from sudo.image import make_image
from sudo.reddit import grab_good_post
from sudo.xkcd import get_url, get_random_url
from sudo.arch import arch_wiki_get
from sudo.valid import validate_number

# Contains tokens and stuff
with open("secrets.json") as f:
    secrets = json.loads(f.read())


admin = (709561120070959205, )  # Roles with admin perms
client = commands.Bot(command_prefix='sudo ')

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

hall_of_fame_id = 716131138468446348


def get_guild(inp) -> discord.Guild:
    # Utility function, gets a Guild object from a variety of different types
    if type(inp) in (commands.Context, discord.message.Message):
        return inp.guild
    if type(inp) in (discord.RawReactionActionEvent,):  # More to be added!
        return client.get_guild(inp.guild_id)
    if type(inp) is int:
        return client.get_guild(inp)
    raise TypeError(f"get_guild is not (yet) implemented for {type(inp)}")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Searching for sudo help'))
    print('We have logged in as {0.user}'.format(client))


# Errors
# TODO: Add more error messages to increase ease of use and help with debuging
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        # If user has insufficient perms for that command, tell them so
        await ctx.send('```Missing required role```')
    else:
        print(error, type(error))


# Moderation commands.
@client.command(help="Returns bot ping")
async def ping(ctx):
    await ctx.send(f'```Bot Latency: {round(client.latency * 1000)}ms```')


@client.command(hidden=True)
@commands.has_any_role(*admin)
async def award(ctx, member: discord.Member, xp: int = 50):
    """Awards a specified user XP"""
    users = leveling.load_users()

    message = ctx.message

    # Validate xp passed
    if xp != 50:
        valid = validate_number(str(xp))

    if valid:
        leveling.update_data(users, member)
        leveling.add_experience(users, member, xp)
        await check_level(users, member, message)
        leveling.save_users(users)

        await ctx.send(f'```Awarded {xp}xp to {member.name}```')
    else:
        await ctx.send('Please enter a valid number')


@client.command(hidden=True)
@commands.has_any_role(*admin)
async def purge(ctx, amount=2):
    """Removes messages from a channel"""
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

# Other commands


# DuckDuckGo
# In order to move to embeds you're going to have to write some complex code. Better to make a script.
@client.command(help="Search the internet with DuckDuckGo")
async def ddg(ctx, *, search):
    search = duckduckgo.get_zci(search)
    await ctx.send(f'```{search}```')


# Quickly thrown together. Poor handling of links. Move to embeds add search functionality and grab head summary at top of wiki page.
# TOP PRIORITY!!!
@client.command(help="Request a link to a page on the Arch Wiki")
async def arch(ctx, *, page):
    page.replace(" ", "_")
    url = arch_wiki_get(page)
    await ctx.send(url)

####################################################
#                LEVELING SYSTEM                   #
####################################################


@client.command(help="Tells you your level")
async def level(ctx, member: discord.Member=None):
    users = leveling.load_users()
    if member:
        user = member
    else:
        user = ctx.message.author
    level = users[str(user.id)]["level"]
    xp = users[str(user.id)]["experience"]
    end_xp = (level + 1) ** 4
    start_xp = level ** 4
    img = make_image(user, level, xp, start_xp, end_xp)
    file = io.BytesIO()
    img.save(file, "PNG")
    await ctx.send(file=discord.File(io.BytesIO(bytes(file.getbuffer())), filename="level.png"))


@client.event
async def on_member_join(member: discord.Member):
    """Adds new user to leveling system"""
    users = leveling.load_users()
    leveling.update_data(users, member)
    leveling.save_users(users)


@client.event
async def on_message(message):
    users = leveling.load_users()

    leveling.update_data(users, message.author)
    leveling.add_experience(users, message.author, 10)
    await check_level(users, message.author, message)

    leveling.save_users(users)

    # Execute additional commands
    await client.process_commands(message)


async def check_level(users, user: discord.member.Member, message: discord.Message):
    """Checks user's level, increases if needed"""
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_end > lvl_start:
        LEVELUP_CHANNEL = 710264223523012648 # Channel to post level up messages to
        channel = client.get_channel(LEVELUP_CHANNEL)
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
            await user.remove_roles(*remove)
            await user.add_roles(converted[lvl_end // 5])


# END OF LEVELING SYSTEM

# Start of Evil Hacker's Code

@client.command(help="Grabs a random image/video from the specified subreddit")
async def reddit(ctx, subreddit):
    # Grabs one of the top media-containing posts from the specified subreddit
    post = grab_good_post(subreddit)
    if post is None:
        await ctx.send("No media posts were found in the top 20 :(")
    else:
        await ctx.send(post[0] + " | " + post[1])


@client.command(help="Grabs an XKCD comic, random if no number is supplied")
async def xkcd(ctx, number=None):
    # Grabs an XKCD comic, random if no number is supplied
    valid = True
    if number:
        valid = validate_number(number)
        if not valid:
            await ctx.send("Please give a valid number")
            return
    post = get_url(number) if number else get_random_url()
    await ctx.send(post)


@client.command(hidden=True)
@commands.has_any_role(*admin)
async def set_threshold(ctx: commands.Context, number):
    valid = validate_number(number)
    if not valid:
        await ctx.send("Please give a valid number")
        return

    with open("settings.json", "r") as f:
        current = json.load(f)
    current["hall_of_fame_threshold"] = int(number)
    with open("settings.json", "w") as f:
        json.dump(current, f)
    await ctx.send("Threshold successfully set (will not affect old messages)")


@client.event
async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):
    guild = get_guild(reaction)
    if reaction.channel_id not in (709561915206008962,):
        if reaction.emoji.name == "linuxPowered":
            message: discord.Message = await guild.get_channel(reaction.channel_id).fetch_message(reaction.message_id)
            num = list(filter(lambda x: x.emoji.name == "linuxPowered", message.reactions))[0].count
            threshold = json.loads(open("settings.json").read())["hall_of_fame_threshold"]
            if num == threshold:
                hall_of_fame: discord.TextChannel = guild.get_channel(hall_of_fame_id)
                messages = await hall_of_fame.history(limit=200).flatten()
                for m in messages:
                    if str(message.id) in m.content:
                        # Return if it is a repost
                        return
                content = (">>> " + message.content) if len(message.content) > 0 else ""
                files = message.attachments

                def check(file):
                    return re.fullmatch("\\w+\\.(jpg|png|gif|jpeg)$", file.filename)
                embed = None
                eligible_files = list(filter(check, files))
                if len(eligible_files) > 0:
                    embed = discord.Embed()
                    embed.set_image(url=eligible_files[0].url)
                await hall_of_fame.send(f"`{message.author}` | `{message.created_at.strftime('%c')}` | `{message.id}`\n"
                                        f"{content}", embed=embed)
                users = leveling.load_users()

                leveling.update_data(users, message.author)
                leveling.add_experience(users, message.author, 500)
                await check_level(users, message.author, message)

                leveling.save_users(users)

    readme: discord.TextChannel = guild.get_channel(readme_channel_id)
    readme_message: discord.Message = await readme.fetch_message(readme_post_id)
    if not reaction.message_id == roles_post_id:
        reactions = readme_message.reactions
        for i in reactions:
            if i.emoji == "✅":  # Evil hacker's IDE is sad and can't display the character clearly seen here
                if len(reaction.member.roles) < 2:
                    await reaction.member.add_roles(discord.utils.get(guild.roles, id=starter_role_id))
            else:
                await readme_message.remove_reaction(reaction.emoji, reaction.member)
        return

    role: str = reaction.emoji.name
    msg = await client.get_channel(roles_channel_id).fetch_message(roles_post_id)
    if role not in distro_role_ids.keys():
        await msg.remove_reaction(reaction.emoji, reaction.member)
        return

    reactions = readme_message.reactions
    check_box = None
    for i in reactions:
        if i.emoji == "✅":  # Evil hacker's IDE is sad and can't display the character clearly seen here
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


if __name__ == '__main__':
    client.run(secrets["rolebot"]["token"])
