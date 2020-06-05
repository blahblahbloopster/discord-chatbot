# This script sucks. It needs to be reworked ASAP
import requests


def arch_wiki_get(page):
    # Fetches a page from the Arch linux wiki
    return requests.get("https://wiki.archlinux.org/index.php/" + str(page)).url
