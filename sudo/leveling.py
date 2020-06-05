# Functions for loading Saving and dealing with the JSON monster that is our leveling system
import json
import discord
import os

if os.path.abspath(".").split("/")[-1] != "discord_bot":
    os.chdir("../")


def load_users():
    # Loads users dict
    with open("sudo/users.json", "r") as f:
        users = json.load(f)
    return users


def save_users(data: dict):
    # Saves users dict
    with open('sudo/users.json', 'w') as f:
        json.dump(data, f)


def update_data(users: dict, user: discord.Member):
    # Adds user to dict if they aren't already
    if str(user.id) not in users:
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1


def add_experience(users: dict, user: discord.Member, exp: int):
    # Adds XP to user
    users[str(user.id)]['experience'] += exp
