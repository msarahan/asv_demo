import math
import random
import string

size = 10000


def math_work(n):
    for i in range(int(n)):
        math.sqrt(i)


def memory_work(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n)) * 1000
