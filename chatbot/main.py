import time
import discord
from chatbot import chatbot
import json
import os

if os.path.abspath(".").split("/")[-1] != "discord_bot":
    os.chdir("../")


secrets = json.loads(open("secrets.json").read())

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


prefix = ""


@client.event
async def on_message(message):
    global prefix
    if message.author == client.user or message.channel == "unbelievaboat" or message.channel == "admin-corner-uwu":
        return
    if "$$$$" in message.content:
        prefix = "<$$$709896631855874088> "
    if "$%$%" in message.content:
        prefix = ""
    if secrets["chatbot"]["id"] in message.content or message.content[:4] == ":~$ ":
        content = message.content.replace(secrets["chatbot"]["id"], "").replace(":~$ ", "")
        if "$$$$" in content:
            prefix = "<$$$709896631855874088> "
        if "$%$%" in content:
            prefix = ""

        if str(message.channel) == "bot":
            await message.channel.send((prefix + chatbot.learn_and_reply(content).replace("@", "!!").replace("<u>", "_").replace("</u>", "_")).replace("$$$", "@"))
            time.sleep(1)
    else:
        chatbot.brain.learn(message.content)

client.run(secrets["chatbot"]["token"])
