from unittest import TestCase
import time

from asv_demo.functionality import somefunc

delay_time = 0


def meat():
    if delay_time:
        time.sleep(delay_time)
    print("I am testing!")
    assert somefunc() == "hello world"
    return True


# pytest-style
def test_somefunc():
    meat()


class IntegrationTests(TestCase):
    def test_class_somefunc(self):
        meat()
