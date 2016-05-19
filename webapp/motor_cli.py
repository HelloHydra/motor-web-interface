#!/usr/bin/env python3

import serial
import time

class Motor:
    def __init__(self):
        self.serial = None
        self.target_position = 0
        self.current_position = 0

    def open(self):
        self.serial = serial.Serial(
            port = "/dev/cu.SLAB_USBtoUART",
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS
            )
    def close(self):
        self.serial.close()

    def get_position(self):
        self.serial.flushInput()
        self.serial.flushOutput()

        self.serial.write("gpos\n".encode('utf-8'))
        end = time.time() + 0.02

        reply = ''
        while time.time() < end:
            if self.serial.inWaiting() > 0:
                reply += self.serial.read().decode('utf-8')
        reply = reply[6:-2]

        self.serial.flushInput()
        self.serial.flushOutput()

        try:
            self.current_position = int(reply)
        except (ValueError):
            pass

        return self.current_position

    def set_position(self, position):
        self.serial.flushInput()
        self.serial.flushOutput()

        self.target_position = position

        self.serial.write("spos ".encode('utf-8'))
        self.serial.write(str(self.target_position).encode('utf-8'))
        self.serial.write("\n".encode('utf-8'))

        time.sleep(0.02)

if __name__ == '__main__':
    motor = Motor()
    motor.open()
    motor.get_position()

    motor.set_position(0)
    time.sleep(1)
    motor.set_position(100000)
    time.sleep(1)
    motor.set_position(0)
    time.sleep(1)
    motor.set_position(100000)

    print(motor.current_position)
    motor.close()