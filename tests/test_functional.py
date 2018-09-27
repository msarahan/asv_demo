from unittest import TestCase
from asv_demo import math_work, memory_work

test_size = 100


def tofurkey():
    math_work(test_size)
    a = memory_work(test_size)


def red_meat():
    from asv_demo import size
    math_work(size)
    a = memory_work(size)


# pytest-style
def test_tofurkey():
    tofurkey()


def test_red_meat():
    red_meat()


class IntegrationTests(TestCase):
    def test_class_tofurkey(self):
        tofurkey()

    def test_class_red_meat(self):
        red_meat()
