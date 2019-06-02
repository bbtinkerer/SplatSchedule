import time
import board
import busio
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi as esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager as manager
from conf.secrets import secrets


class WiFi:
    def __init__(self, spi, adafruit_esp32spi_requests=None, debug=0):
        esp32_cs = DigitalInOut(board.ESP_CS)
        esp32_ready = DigitalInOut(board.ESP_BUSY)
        esp32_reset = DigitalInOut(board.ESP_RESET)

        self._esp = esp32spi.ESP_SPIcontrol(spi, esp32_cs,
                                            esp32_ready, esp32_reset)
        self._esp._debug = debug
        status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
        self._wifi = manager.ESPSPI_WiFiManager(self._esp, secrets, status_light)
        self._debug = debug

    def get_url_response_text(self, url):
        if self._debug:
            print('getting resonse text from: ' + url)
        response_text = None
        success = False
        while not success:
            try:
                response = self._wifi.get(url)
                response_text = response.text
                response.close()
                response = None
                success = True
                if self._debug:
                    print('success! received response')
            except RuntimeError as e:
                print('Failed to get data, retrying\n', e)
                self._wifi.reset()
                time.sleep(20)

        return response_text

    def get(self, url):
        return self._wifi.get(url)
