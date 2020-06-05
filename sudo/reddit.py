# Big boi script to get reddit things. Read documentation for each function.
import random
import requests
import re


# Subreddit is without the r/
def grab_top_posts(subreddit: str):
    # Grabs a list of top posts from a specified subreddit
    raw = requests.get("https://reddit.com/r/{}/top/.json?count=20".format(subreddit),
                       headers={'User-agent': 'your bot 0.1'})
    return raw.json()


def get_data(post_json: dict):
    # Grabs data about a post from the json blob
    return post_json["data"]["title"], post_json["data"]


def get_info_by_id(id_number: int, subreddit, data=None):
    # Gets one post by id number from a subreddit
    if not data:
        data = grab_top_posts(subreddit)["data"]["children"][id_number]["data"]
    else:
        data = data[id_number]["data"]
    is_video = data["is_video"]
    id_num = data["id"]
    if "post_hint" not in data:
        is_image = False
    else:
        is_image = data["post_hint"] == "image"
    return id_num, is_video, is_image, data


def get_media_by_id(id_number: int, subreddit, data=None):
    # Grabs any media attached to a post
    if not data:
        data = grab_top_posts(subreddit)["data"]["children"][id_number]["data"]
    info = get_info_by_id(id_number, subreddit, data)
    if not (info[1] or info[2]):
        return None
    if info[1]:
        return info[3]["media"]["reddit_video"]["fallback_url"]
    if info[2]:
        return info[3]["url"]


def grab_good_post(subreddit: str):
    # Fetches a media-containing post from the specified subreddit
    d = grab_top_posts(subreddit)["data"]["children"]
    posts = []
    for i in range(len(d)):
        item = get_media_by_id(i, subreddit, data=d)
        if item:
            posts.append((d[i]["data"]["title"], item))
    if len(posts) == 0:
        return None
    post = random.choice(posts)
    return post
