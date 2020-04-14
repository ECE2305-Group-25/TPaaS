##
# PIN Generation and management module
#

import time
import random

class PIN:

    def __init__(self):
        self.minimum_pin_lifespan = 30 # seconds
        self.pin = 0
        self.last_pin_generation_time = 0

    def generate_new_pin(self):
        if time.time() > self.last_pin_generation_time + self.minimum_pin_lifespan:
            self.pin = random.randrange(0,10000)
            self.last_pin_generation_time = time.time()
            return True, self.pin
        else:
            return False, "Pin changed too recently"

    def check_pin(self, pin):
        return int(pin) == self.pin