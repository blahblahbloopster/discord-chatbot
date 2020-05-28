import requests


def ArchGet(page):
    return requests.get("https://wiki.archlinux.org/index.php/" + str(page)).url
