##
# Hardware Interface Module
#

import irprox
import servo
import display
import lidswitch

class HIM:

    def __init__(self):
        self.irprox = irprox.IRProx()
        self.servo1 = servo.Servo()
        self.servo2 = servo.Servo()
        self.display = display.Display()
        self.lidswitch = lidswitch.LidSwitch()

    ##
    # Change the pin currently displayed on the built in screen
    def change_pin(self, pin):
        print("STUB: change_pin({})".format(pin))
        self.display.show("{:0>4d}".format(pin))

    ##
    # Dispense a roll of toilet paper
    def dispense(self):
        print("STUB: dispense()")
        # TODO: Maniuplate the servos in such a way that only one roll escapes
        pass

    ##
    # Return the number of rolls of toilet paper currently in the holder.
    def get_remaining_rolls(self):
        distance = self.irprox.read()
        # TODO: Calculate remaining rolls
        return -1