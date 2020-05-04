#!/usr/bin/python3

from components import proximity_sensor
import json
from config import config
import time

cfg = config.components

adc = proximity_sensor.ADC(**cfg.proximity_sensor.pins)
sensor = proximity_sensor.ProximitySensor(
    adc, cfg.proximity_sensor.channel)

measurements = 25
delay = .1

data = dict()

def take_reading(rollnum):
    if rollnum == 0:
        print("Please make sure the hopper is empty")
    else:
        print("Please insert roll number {}".format(rollnum))
    input("Press ENTER to continue...")
    voltage_accumulator = 0
    for i in range(0,measurements):
        print("\r" + ("▰"*i) + ("▱"*(measurements-i-1)),end="")
        time.sleep(delay)
        voltage_accumulator += sensor.voltage
    print()
    data[str(rollnum)] = voltage_accumulator / measurements

for roll in range(0,7):
    take_reading(roll)

out = open("calibration.json","w")
out.write(json.dumps(data))
out.close()

print("\033[32mDone\033[0m")