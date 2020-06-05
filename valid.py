import re


def validate(number):
    if re.fullmatch("^[0|1|2|3|4|5|6|7|8|9]+$", number):
        if 0 < len(number) < 5:
            return True
        else:
            return False
    else:
        return False
