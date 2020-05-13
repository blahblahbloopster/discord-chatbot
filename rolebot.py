from typing import List

import discord
import chatbot
import json

with open("secrets.json") as f:
    secrets = json.loads(f.read())

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_raw_reaction_add(reaction):
    if not reaction.message_id == 709827022800683038:
        guild = client.get_guild(reaction.guild_id)
        readme: discord.TextChannel = guild.get_channel(709580982688153621)
        message: discord.Message = await readme.fetch_message(709897964771999816)
        check = message.reactions
        for i in check:
            if i.emoji == "✅":  # There IS a char there, but my IDE doesn't display it.  It's
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
