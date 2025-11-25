import random


def getRandChar(count):
    chars = []
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    for i in range(count):
        char = random.choice(alphabet)
        chars.append(char)
    return ''.join(chars)