# A simple script to validate an int passed through the code to avoid errors.
import re


def validate_number(number):
    # matchall individual numbers to see if they are an int by themselves.
    if re.fullmatch("^[0|1|2|3|4|5|6|7|8|9]+$", number): # Oddly checking an int with a str, but it works
        # Make sure there is a value there in the first place and make sure the number isn't absurd.
        if 0 < len(number) < 5:
            return True
        else:
            return False
    else:
        return False # You need to have return false twice or else it won't return anything making error handling difficult
