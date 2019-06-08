import time
import board
import busio
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi as esp32spi
import adafruit_esp32spi.adafruit_esp32spi_requests as requests
from conf.secrets import secrets


class WiFi:
    def __init__(self, spi, adafruit_esp32spi_requests=None, debug=0):
        self._debug = debug
        esp32_ready = DigitalInOut(board.ESP_BUSY)
        esp32_gpio0 = DigitalInOut(board.ESP_GPIO0)
        esp32_reset = DigitalInOut(board.ESP_RESET)
        esp32_cs = DigitalInOut(board.ESP_CS)
        self._esp = esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset, esp32_gpio0)
        self._esp._debug = debug
        for _ in range(3):  # retries
            try:
                print("ESP firmware:", self._esp.firmware_version)
                break
            except RuntimeError:
                print("Retrying ESP32 connection")
                time.sleep(1)
                self._esp.reset()
        else:
            raise RuntimeError("Was not able to find ESP32")
        requests.set_interface(self._esp)
        self.neopix = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
        self._connect_esp()

    def neo_status(self, value):
        if self.neopix:
            self.neopix.fill(value)

    def _connect_esp(self):
        self.neo_status((0, 0, 100))
        while not self._esp.is_connected:
            # secrets dictionary must contain 'ssid' and 'password' at a minimum
            if self._debug:
                print("Connecting to AP", secrets['ssid'])
            self.neo_status((100, 0, 0))  # red = not connected
            try:
                self._esp.connect(secrets)
            except RuntimeError as error:
                print("Could not connect to internet", error)
                print("Retrying in 3 seconds...")
                time.sleep(3)

    def get_url_response_text(self, url):
        if self._debug:
            print('getting resonse text from: ' + url)
        self._connect_esp()
        response_text = None
        success = False
        retries = 3
        while not success and retries > 0:
            try:
                response = requests.get(url)
                response_text = response.text
                response.close()
                response = None
                success = True
                if self._debug:
                    print('success! received response')
            except RuntimeError as e:
                print('Failed to get data, retrying\n', e)
                time.sleep(20)
                retries = retries - 1
        if not success:
            import supervisor
            supervisor.reload()

        return response_text
