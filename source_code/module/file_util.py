import random
import string

def generate_random_string(count=3):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) \
        for _ in range(count))

def generate_alphanumeric_string(count=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(count))

def generate_specialchars_string(count=4, chars=string.punctuation.replace("\"","").replace("\'","")):
    return ''.join(random.choice(chars) for _ in range(count))

def generate_random_string_uppercase(count=3):
    return ''.join(random.choice(string.ascii_uppercase) \
        for _ in range(count))

def generate_random_string_lowercase(count=3):
    return ''.join(random.choice(string.ascii_lowercase) \
        for _ in range(count))

def generate_random_number(count=1):
    range_start = 10**(count-1)
    range_end = (10**count)-1
    return random.randint(range_start, range_end)