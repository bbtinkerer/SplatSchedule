import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_servokit import ServoKit


class Turntable:
    def __init__(self, debug=False):
        self._debug = debug
        self._last_movement = 0
        self._last_enabled = 0
        self._output_enable = DigitalInOut(board.D3)
        self._output_enable.direction = Direction.OUTPUT
        self._disable()
        self._kit = ServoKit(channels=16)
        self.reset_position()

    def update(self):
        if self._last_movement:
            current_time = time.time()
            if current_time - self._last_movement > 5:
                self.reset_position()
        if self._last_enabled:
            current_time = time.time()
            if current_time - self._last_enabled > 8:
                self._disable()

    def turn_in(self):
        if self._debug:
            print("turntable turn in")
        self._enable()
        self._kit.servo[0].angle = 0
        self._kit.servo[1].angle = 180
        self._last_movement = time.time()

    def reset_position(self):
        if self._debug:
            print("turntable reset")
        self._enable()
        self._kit.servo[0].angle = 90
        self._kit.servo[1].angle = 90
        self._last_movement = 0

    def _enable(self):
        # PCA9685 board is active low
        if self._debug:
            print("turntable enabling output")
        self._output_enable.value = False
        self._last_enabled = time.time()

    def _disable(self):
        # PCA9685 board is active low
        # give time to move before disabling
        if self._debug:
            print("turntable disabling output")
        self._output_enable.value = True
        self._last_enabled = 0


class FakeTurntable:
    def __init__(self, debug=False):
        self._debug = debug

    def update(self):
        pass

    def turn_in(self):
        pass

    def reset_position(self):
        pass
