import time


class Message:

    def __init__(self, action, timestamp=None):
        self.timestamp = timestamp or time.time()
        self.action = action

    def __str__(self):
        return f'Message[{self.action}/{self.timestamp}]'
