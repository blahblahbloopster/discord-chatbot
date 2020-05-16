import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import discord

# img = Image.new("RGB", (1920, 720))

# draw = ImageDraw.Draw(img)

# draw.text((10, 10), "foo")
# draw.ellipse((100, 310, 150, 360))


def draw(percentage, color=(255, 0, 0)):
    im2 = Image.open("mask.png")
    im3 = Image.new("RGBA", (1920, 480), color=(20, 20, 20))
    draw2 = ImageDraw.Draw(im3)
    total_distance = 1920 - 50
    total_distance *= percentage / 100
    draw2.rectangle((25, 75, total_distance + 25, 125), fill=color)
    im3.alpha_composite(im2)
    return im3


def make_image(username: discord.Member, level: int, xp: int, lvl_start_xp: int, lvl_end_xp: int):
    color = username.top_role.color.to_rgb()
    img = draw(((xp - lvl_start_xp) / (lvl_end_xp - lvl_start_xp)) * 100, color=color)
    draw2 = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Regular.ttf", size=50)
    draw2.text((20, 0),
               f"{username.display_name if type(username) is discord.Member else username}  |  {xp} / {lvl_end_xp} XP",
               font=font)
    draw2.text((20, 150), f"Level {level}", font=font)
    draw2.text((1920 - 200, 150), f"Level {level + 1}", font=font)
    # img.show()
    return img


# make_image("evil_hacker", 4, 400, 300, 500)
