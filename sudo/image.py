from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import discord
import os

if os.path.abspath(".").split("/")[-1] != "discord_bot":
    os.chdir("../")


def draw(percentage, color=(255, 0, 0)):
    """Creates a bar image"""
    im2 = Image.open("sudo/mask.png")
    im3 = Image.new("RGBA", (1920, 240), color=(20, 20, 20))
    draw2 = ImageDraw.Draw(im3)
    total_distance = 1920 - 50
    total_distance *= percentage / 100
    draw2.rectangle((25, 75, total_distance + 25, 125), fill=color)
    im3.alpha_composite(im2)
    return im3


def make_image(username: discord.Member, level: int, xp: int, lvl_start_xp: int, lvl_end_xp: int):
    """Creates an image that shows a user's level and XP"""
    color = username.top_role.color.to_rgb()
    img = draw(((xp - lvl_start_xp) / (lvl_end_xp - lvl_start_xp)) * 100, color=color)
    draw2 = ImageDraw.Draw(img)
    font = ImageFont.truetype("sudo/Roboto-Regular.ttf", size=50)
    draw2.text((20, 0),
               f"{username.display_name if type(username) is discord.Member else username}  |  {xp} / {lvl_end_xp} XP",
               font=font)
    draw2.text((20, 150), f"Level {level}", font=font)
    draw2.text((1920 - 200, 150), f"Level {level + 1}", font=font)
    return img
