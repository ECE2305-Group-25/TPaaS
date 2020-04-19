##
# Lid Switch Detector Driver Module
#
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


class LidSwitch:

    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        pass

    def check(self):
        return not GPIO.input(self.pin)

    def __delete__(self, instance):
        GPIO.cleanup()


# if __name__ == '__main__':
#     import time
#     s = LidSwitch(21)
#     while True:
#         print(s.check(), end="\r", flush=True)
#         time.sleep(.2)
