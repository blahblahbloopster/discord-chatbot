import json
import discord


def load_users():
    """Loads users dict"""
    with open("users.json", "r") as f:
        users = json.load(f)
    return users


def save_users(data: dict):
    """Saves users dict"""
    with open('users.json', 'w') as f:
        json.dump(data, f)


def update_data(users: dict, user: discord.Member):
    """Adds user to dict if they aren't already"""
    if str(user.id) not in users:
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1


def add_experience(users: dict, user: discord.Member, exp: int):
    """Adds XP to user"""
    users[str(user.id)]['experience'] += exp
