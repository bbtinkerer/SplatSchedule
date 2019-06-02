import adafruit_sdcard
import board
import busio
from digitalio import DigitalInOut
import storage


class Storage:
    def __init__(self, sd_mount_directory, spi, debug=False):
        self._debug = debug

        if self._debug:
            print("Init SD Card")
        sd_cs = DigitalInOut(board.SD_CS)
        self._sdcard = None
        try:
            self._sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
            vfs = storage.VfsFat(self._sdcard)
            storage.mount(vfs, sd_mount_directory)
        except OSError as error:
            print("No SD card found:", error)
