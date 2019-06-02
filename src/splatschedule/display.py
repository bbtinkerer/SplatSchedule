import audioio
import board
from digitalio import DigitalInOut
import displayio
import gc
import neopixel
import os
import pulseio
import time


class Display:
    def __init__(self, default_bg=0x000000, status_neopixel=None, debug=0):
        self._debug = debug
        try:
            self._backlight = pulseio.PWMOut(board.TFT_BACKLIGHT)
        except ValueError:
            self._backlight = None
        self._set_backlight(1.0)  # turn on backlight

        if status_neopixel:
            self.neopix = neopixel.NeoPixel(status_neopixel, 1, brightness=0.2)
        else:
            self.neopix = None
        self.neo_status(0)

        if self._debug:
            print("Init display")
        self.splash = displayio.Group(max_size=15)

        if self._debug:
            print("Init background")
        self._bg_group = displayio.Group(max_size=1)
        self._bg_file = None
        self._default_bg = default_bg
        self.splash.append(self._bg_group)

        for bootscreen in ("/thankyou.bmp", "/pyportal_startup.bmp"):
            try:
                os.stat(bootscreen)
                board.DISPLAY.show(self.splash)

                for i in range(100, -1, -1):  # dim down
                    self._set_backlight(i/100)
                    time.sleep(0.005)
                self.set_background(bootscreen)
                board.DISPLAY.wait_for_frame()
                for i in range(100):  # dim up
                    self._set_backlight(i/100)
                    time.sleep(0.005)
                time.sleep(2)
            except OSError:
                pass  # they removed it, skip!
        self._speaker_enable = DigitalInOut(board.SPEAKER_ENABLE)
        self._speaker_enable.switch_to_output(False)
        self.audio = audioio.AudioOut(board.AUDIO_OUT)

        try:
            self.play_file("pyportal_startup.wav")
        except OSError:
            pass  # they deleted the file, no biggie!

    def _set_backlight(self, val):
        """Adjust the TFT backlight.
        :param val: The backlight brightness. Use a value between ``0`` and ``1``, where ``0`` is
        off, and ``1`` is 100% brightness.
        """
        val = max(0, min(1.0, val))

        if self._backlight:
            self._backlight.duty_cycle = int(val * 65535)
        else:
            board.DISPLAY.auto_brightness = False
            board.DISPLAY.brightness = val

    def neo_status(self, value):
        """The status NeoPixel.
        :param value: The color to change the NeoPixel.
        """
        if self.neopix:
            self.neopix.fill(value)

    def set_background(self, file_or_color, position=None):
        """The background image to a bitmap file.
        :param file_or_color: The filename of the chosen background image, or a hex color.
        """
        if self._debug:
            print("Set background to ", file_or_color)

        while self._bg_group:
            self._bg_group.pop()

        if not position:
            position = (0, 0)  # default in top corner

        if not file_or_color:
            return  # we're done, no background desired

        if self._bg_file:
            self._bg_file.close()

        if isinstance(file_or_color, str):  # its a filenme:
            self._bg_file = open(file_or_color, "rb")
            background = displayio.OnDiskBitmap(self._bg_file)
            try:
                self._bg_sprite = displayio.TileGrid(background,
                                                     pixel_shader=displayio.ColorConverter(),
                                                     position=position)
            except TypeError:
                self._bg_sprite = displayio.TileGrid(background,
                                                     pixel_shader=displayio.ColorConverter(),
                                                     x=position[0], y=position[1])
        elif isinstance(file_or_color, int):
            # Make a background color fill
            color_bitmap = displayio.Bitmap(320, 240, 1)
            color_palette = displayio.Palette(1)
            color_palette[0] = file_or_color

            try:
                self._bg_sprite = displayio.TileGrid(color_bitmap,
                                                     pixel_shader=color_palette,
                                                     position=(0, 0))
            except TypeError:
                self._bg_sprite = displayio.TileGrid(color_bitmap,
                                                     pixel_shader=color_palette,
                                                     x=position[0], y=position[1])
        else:
            raise RuntimeError("Unknown type of background")

        self._bg_group.append(self._bg_sprite)
        board.DISPLAY.refresh_soon()
        gc.collect()
        board.DISPLAY.wait_for_frame()

    def play_file(self, file_name, wait_to_finish=True):
        """Play a wav file.
        :param str file_name: The name of the wav file to play on the speaker.
        """
        board.DISPLAY.wait_for_frame()
        wavfile = open(file_name, "rb")
        wavedata = audioio.WaveFile(wavfile)
        self._speaker_enable.value = True
        self.audio.play(wavedata)
        if not wait_to_finish:
            return

        while self.audio.playing:
            pass

        wavfile.close()
        self._speaker_enable.value = False
