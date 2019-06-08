import os
import random
import time
import gc


class BackgroundRandomizer:
    def __init__(self, display, directory, timeout, debug=False):
        self._debug = debug
        self._timeout = timeout
        self._directory = directory
        self._display = display
        self._last_change = 0
        self._backgrounds = os.listdir(directory)
        self._backgrounds_count = len(self._backgrounds) - 1
        self.display_background()

    def update(self):
        now = time.time()
        if now - self._last_change > self._timeout:
            self.display_background()

    def clear_background(self):
        self._display.set_background(None)

    def display_background(self):
        background = self._directory + self._backgrounds[random.randint(0, self._backgrounds_count)]
        if self._debug:
            print("setting background: " + background)
        self._display.set_background(background)
        self._last_change = time.time()
