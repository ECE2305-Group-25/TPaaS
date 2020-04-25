##
# Servo Driver Module
#
import time
import threading
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
for i in range(16):
    kit.servo[i].set_pulse_width_range(500, 2500)
    kit.servo[i].throttle = 1


class ServoDriver:
    @staticmethod
    def init_kit(channels, pulse_width_range):
        kit = ServoKit(channels=channels)
        for i in range(channels):
            kit.servo[i].set_pulse_width_range(*pulse_width_range)
            kit.servo[i].throttle = 1

    def __init__(self, servos):
        self.servos = {}
        for servo in servos:
            self.servos[servo['label']] = servo

    def angle(self, label, angle):
        ch = self.servos[label]['channel']
        kit.servo[ch].angle = angle

    def format_servo_data(label, channel, min_angle=0, max_angle=180,
                          inverted=False):
        return {'label': label, 'channel': channel, 'min_angle': min_angle,
                'max_angle': max_angle, 'inverted': inverted}

    def full_angle(self, labels, pos):
        if not (type(labels) is list):
            labels = [labels]
        for l in labels:
            servo = self.servos[l]
            if pos:
                if not servo['inverted']:
                    self.angle(l, servo['max_angle'])
                else:
                    self.angle(l, servo['min_angle'])
            else:
                if not servo['inverted']:
                    self.angle(l, servo['min_angle'])
                else:
                    self.angle(l, servo['max_angle'])


class ServoPlatform:
    def __init__(self, servo_driver, left, right):
        self.driver = servo_driver
        self.servos = [left, right]

    def open(self):
        self.driver.full_angle(self.servos, 0)

    def close(self):
        self.driver.full_angle(self.servos, 1)


class ServoDispenser:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.run_lock = threading.Lock()

    def operate(self):
        self.run_lock.acquire()
        self.p1.open()
        time.sleep(2)
        self.p1.close()
        self.p2.open()
        time.sleep(2)
        self.p2.close()
        self.run_lock.release()

    def dispense(self):
        t = threading.Thread(target=self.operate)
        t.start()
        return t


# if __name__ == '__main__':
#     import sys
#     import os
#     sys.path.append(os.path.join(sys.path[0], '../'))
#     from config import config
#     sc = config['components']['servos']
#     channels = sc['channels']
#     pwr = sc['pulse_width_range']
#     pwr = (pwr[0], pwr[1])
#     servo_entries = sc['platforms']['p1'] + sc['platforms']['p2']
#     hs = ServoDriver(servo_entries)

#     all = ['l1', 'r1', 'l2', 'r2']
#     hs.full_angle(all, 1)
#     time.sleep(1)
#     hs.full_angle(all, 0)
