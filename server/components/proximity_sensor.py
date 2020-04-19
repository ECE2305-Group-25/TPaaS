##
# Proximity Sensor Driver Module
#
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# resolver to load pins by name in config


def resolve_pin(name):
    return board.__dict__[name]


# The ADC used to read analog data
class ADC:
    def __init__(self, CLOCK=board.SCK, MISO=board.MISO, MOSI=board.MOSI, DATA=board.D5):
        self.available_channels = list(range(0, 8))
        self.allocated_channels = []

        if type(CLOCK) is str:
            CLOCK = resolve_pin(CLOCK)
        if type(MISO) is str:
            MISO = resolve_pin(MISO)
        if type(MOSI) is str:
            MOSI = resolve_pin(MOSI)
        if type(DATA) is str:
            DATA = resolve_pin(DATA)

        # create the spi bus
        self.spi = busio.SPI(clock=CLOCK, MISO=MISO, MOSI=MOSI)

        # create the cs (chip select)
        self.cs = digitalio.DigitalInOut(DATA)

        # create the mcp object
        self.mcp = MCP.MCP3008(self.spi, self.cs)

    def add_channel(self, number):
        if number in self.allocated_channels:
            print("Warning: This channel has already been allocated")
            return AnalogIn(self.mcp, number)
        elif number not in self.available_channels:
            print("Error: Channel number outside available range")
            return
        self.available_channels.remove(number)
        self.allocated_channels.append(number)
        return AnalogIn(self.mcp, number)


# Wrapper to start enable reading on ADC channel
class ProximitySensor(AnalogIn):
    def __init__(self, adc, channel=0):
        base_obj = adc.add_channel(channel)
        self.__class__ = type(base_obj.__class__.__name__,
                              (self.__class__, base_obj.__class__),
                              {})
        self.__dict__ = base_obj.__dict__


# Code to test ADC by printing out channel 0 voltage
#
# if __name__ == '__main__':
#     import time
#     adc = ADC()
#     channel = ProximitySensor(adc)
#     print(channel)
#     while True:
#         print(channel.voltage, end="\r", flush=True)
#         time.sleep(.2)
