import requests


def get_random_url():
    return requests.get("https://c.xkcd.com/random/comic/").url


def get_url(number: int):
    return "https://xkcd.com/" + str(number)
