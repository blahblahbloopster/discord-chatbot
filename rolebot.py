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
        return
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
    if role not in roles.keys():
        msg = await client.get_channel(709800728008327238).fetch_message(709827022800683038)
        await msg.remove_reaction(reaction.emoji, reaction.member)
        return
    guild = client.get_guild(reaction.guild_id)
    role = discord.utils.get(guild.roles, id=roles[role])
    await reaction.member.add_roles(role)


client.run(secrets["rolebot"]["token"])
