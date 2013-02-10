import random
import string 

def get_random(limit):
    fn = lambda : \
            random.choice(string.lowercase + string.uppercase + string.digits)
    value = ''.join(fn() for i in range(limit))
    return value

