import time


class Message:

    def __init__(self, action, timestamp=None, mat_data=None):
        self.timestamp = timestamp or time.time()
        self.action = action
        self.mat_data = mat_data

    def __str__(self):
        return f'Message[{self.action}/{self.timestamp}]'
