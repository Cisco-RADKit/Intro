from typing import Optional
from time import time

'''
A naive stopwatch class.
'''

class StopWatch:
    def __init__(self):
        self._start = 0
        self._stop = 0
    
    def start(self):
        self._start = time()
        self._stop = self.start
    
    def stop(self):
        self._stop = time()
    
    def delta(self):
        return (self._stop - self._start)
    
    def print_delta(self, message: Optional[str] = None):
        if not message:
            message = ""

        message = f"{message}{self.delta()}"
        print(message)
