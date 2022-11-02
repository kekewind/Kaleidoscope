from retrying import retry
import random


@retry
def do_something_unreliable():
    if random.randint(0, 10) > 1:
        print("just have a test")
        raise IOError("raise exception!")
    else:
        return "good job!"


print(do_something_unreliable())
