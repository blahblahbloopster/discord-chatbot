import discord
import pickle as pkl
from pprint import pprint
import chatbot
from chatbot import learn_and_reply
import json

secrets = json.loads(open("secrets.json").read())

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user or message.channel == "unbelievaboat" or message.channel == "admin-corner-uwu":
        return
    if secrets["chatbot"]["id"] in message.content or message.content[:4] == ":~$ ":
        content = message.content.replace(secrets["chatbot"]["id"], "").replace(":~$ ", "")
        # print(str(message.channel))
        # if str(message.channel) == "bot":
            # messages = list(map(lambda x: x.content + "\n", await message.channel.history(limit=200).flatten()))
            # pprint(messages)
            # messages.reverse()
            # messages = "\n".join(messages)
            # with open("messages.txt", "wt") as f:
            #     f.writelines(messages)
            # return
            # with open("channel_messages.txt", "a+", encoding="utf-8") as f:
            #     print(*messages, sep="\n\n", file=f)
            # # print(message.content)
            # return
            # client.logs_from(message.channel, limit=200)
            # return
            # messages = await message.channel.history(limit=200).flatten()
            # pprint(messages)
            # pkl.Pickler(open("messages", "wb")).dump(messages)
        # return

        if str(message.channel) == "bot":
            # print(message.content[22:])
            await message.channel.send(chatbot.brain.reply(content).replace("@", "!!").replace("<u>", "_").replace("</u>", "_"))
            # await message.channel.send("(I'm in observation mode for the moment)")
    else:
        chatbot.brain.learn(message.content)

client.run(secrets["chatbot"]["token"])
