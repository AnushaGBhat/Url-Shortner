import re
import random
import string

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    pattern = re.compile(r'^(http|https)://')
    return pattern.match(url) is not None
