# import cobe
from cobe import brain
import string
import re
#
# with open("spaceballs.txt") as f:
#     lines = f.read().splitlines()
#
# with open("names.txt") as f:
#     names = f.read().splitlines()
#
# patterns = []
# for i in names:
#     patterns.append(re.compile("^" + i))
#
#
# def check(text):
#     for n in patterns:
#         if n.match(text):
#             return True
#     return False
#     # print()
#     # l = 0
#     # for j in text:
#     #     if j == j.upper():
#     #         l += 1
#     #     else:
#     #         return 8 > l > 0
#
#
# def remove_names(text):
#     for p in patterns:
#         if p.match(text):
#             return p.sub("", text)
#
#
# # for i in lines[:20]:
# #     print(i, check(i))
#     # check(i)
# filtered = list(filter(check, lines))
# filtered = list(map(remove_names, filtered))
# # print(filtered[:10])
# with open("spaceballs2.txt", "wt") as f:
#     f.write("\n".join(filtered))
#
# exit()
#
# with open("holy_grail.txt") as f:
#     lines = f.read().splitlines()
#
# all_lines = []
# current = ""
#
# for i in lines:
#     if len(i) < 1:
#         continue
#     if i[:1] == "\t" and not i[:2] == "\t" * 2:
#         # print(i)
#         current += i[1:]
#     if i[:2] == "\t" * 2:
#         all_lines.append(current)
#         current = ""
# #
# # print(all_lines[:10])
# with open("holy_grail_lines.txt", "wt") as f:
#     f.write("\n".join(all_lines))
# exit()

#
# # p = re.compile()
# p = re.compile("\\+\\+\\+\\$\\+\\+\\+")
# # p = re.compile("[\\w|\\s|\\!|\\?|\\@|\\#|\\%|\\^|\\&|\\*|\\(|\\)|\\-|_|\\=|]+$")
# with open("movie_lines2.txt") as f:
#     # print(f.read(1000))
#     lines = list(map(lambda x: p.split(x)[-1][1:], f.read().splitlines()))
#
# # print(lines[0:10])
#
# with open("movie_lines3.txt", "wt") as f:
#     f.write("\n".join(lines))

brain = brain.Brain("cobe_movie_2.brain")

# for i in lines:
#     brain.learn(i)

# for i in open("messages.txt").read().splitlines():
#     brain.learn(i)

# brain.learn
# brain.learn(open("messages.txt").read())
# print(brain.reply("Hello, I'm max"))


def learn_and_reply(message):
    brain.learn(message)
    return brain.reply(message)


# for i in range(1000):
#     for j in ["windows good", "microsoft is good", "windows is the best os", "windows is better than linux",
#               "I hate linux", "linux sucks"]:
#         brain.learn(j)
#         brain.learn("no, linux is better than windoze")
