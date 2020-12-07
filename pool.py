import time
from contextlib import contextmanager


class Pool:
    """
    Fixed size object pool
    """

    def __init__(self, class_to_create, amount: int):
        self.amount = amount
        self.free_instances = list()

        for _ in range(amount):
            self.free_instances.append(class_to_create())

    @contextmanager
    def get(self):
        instance = None

        while not instance:
            try:
                instance = self.free_instances.pop()
            except IndexError:
                instance = None

            time.sleep(0.5)

        try:
            yield instance
        finally:
            self.free_instances.append(instance)
