import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.sample(characters, length))
    return random_string

random_string = generate_random_string(12)
print(random_string)
