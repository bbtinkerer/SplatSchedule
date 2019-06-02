
import board
import adafruit_touchscreen as touchscreen
import time


class Touch:
    def __init__(self, throttle, debug=False):
        self._touchscreen = touchscreen.Touchscreen(
            board.TOUCH_XL, board.TOUCH_XR, board.TOUCH_YD, board.TOUCH_YU,
            calibration=((5200, 59000), (5800, 57000)), size=(320, 240))
        self._throttle = throttle
        self._last_touch_time = time.time()
        self._last_touch = None

    def touch_point(self):
        now = time.time()
        elapsed = now - self._last_touch_time

        # sometimes the first point is way off
        # taking the 2 samples that are close together
        points = []
        points.append(self._touchscreen.touch_point)
        points.append(self._touchscreen.touch_point)
        p0 = points[0]
        p1 = points[1]
        while p0 is not None and p1 is not None and abs(p0[0] - p1[0]) > 10:
            points.pop(0)
            points.append(self._touchscreen.touch_point)
            p0 = points[0]
            p1 = points[1]
        point = p0
        if point is not None and elapsed < self._throttle:
            point = None
        elif point is not None:
            self._last_touch_time = now

        return point
