##
# Hardware Interface Module
#
from config import config
from components import display, servos, proximity_sensor, lid_switch


class HIM:

    def __init__(self):
        cfg = config.components
        # Init servos
        print("Initializing Servos")
        p1 = cfg.servos.platforms.p1
        p2 = cfg.servos.platforms.p2
        servos.ServoDriver.init_kit(cfg.servos.channels,
                                    cfg.servos.pulse_width_range)
        self.servo_driver = servos.ServoDriver(p1 + p2)

        # servo platforms (p1 is bottom, p2 is top)
        self.p1 = servos.ServoPlatform(self.servo_driver, p1[0].label,
                                       p1[1].label)
        self.p2 = servos.ServoPlatform(self.servo_driver, p2[0].label,
                                       p2[1].label)
        self.dispenser = servos.ServoDispenser(self.p1, self.p2)

        # Init Proximity Sensor
        print("Initializing Proximity Sensor")
        self.adc = proximity_sensor.ADC(**cfg.proximity_sensor.pins)
        self.sensor = proximity_sensor.ProximitySensor(
            self.adc, cfg.proximity_sensor.channel)

        # Init Display
        print("Initializing Display")
        self.display = display.Display(cfg.display.width, cfg.display.height,
                                       cfg.display.pins.SCL,
                                       cfg.display.pins.SDA,
                                       cfg.display.i2c_addr,
                                       cfg.display.font_path)

        # Init Lid Switch
        print("Initializing Lid Switch")
        self.lid_switch = lid_switch.LidSwitch(cfg.lid_switch.pullup_pin)

    ##
    # Change the pin currently displayed on the built in screen

    def change_pin(self, pin):
        self.display.show("{:0>4d}".format(pin))

    ##
    # Dispense a roll of toilet paper

    def dispense(self):
        # TODO: Maniuplate the servos in such a way that only one roll escapes
        self.display.show("")
        self.dispenser.dispense()

    ##
    # Return the number of rolls of toilet paper currently in the holder.

    def get_remaining_rolls(self):
        distance = self.sensor.voltage
        # TODO: Calculate remaining rolls
        return -1


# if __name__ == '__main__':
#     import time
#     h = HIM()
#     h.dispenser.dispense()
#     while True:
#         h.display.message(str(h.sensor.voltage)[:10], h.lid_switch.check())
#         time.sleep(.2)
