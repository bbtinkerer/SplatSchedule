# PyPortal Splatoon 2 Schedule Display

By bbtinkerer (<http://bb-tinkerer.blogspot.com/>)

## Description

Splatoon 2 Schedule display with PyPortal. Displays the stages, Ranked Type game, and Salmon Run schedule.  Use the touch screen to cycle through upcoming stages, ranked games, and Salmon Run.

Requires an [Adafruit IO Account](https://io.adafruit.com/) for setting time.

### Optional 

Simple Amiibo animaltronics just for some hardware motion fun.

[PyPortal Splatoon 2 Schedule Display](https://www.instructables.com/id/PyPortal-Splatoon-2-Schedule-Display) Instructables Project 

[PyPortal Splatoon 2 Stage](https://www.thingiverse.com/thing:3662274) 3D Files on Thingiverse.com

[PyPortal Splatoon 2 Schedule Display with Amiibotronics](https://youtu.be/n4F4rq-JXKI) Youtube video 

## Setup

1. Make a backgrounds directory on a micro SD card
1. Copy all the *.bmp files in images to the backgrounds folder you made on the micro SD card
1. Insert the micro SD card into the PyPortal
1. Rename secrets.example.py to secrets.py in the src/conf folder
1. Update secrets.py
   1. **SSID**: Your WiFi network name
   1. **PWD**: Your WiFi password
   1. **TIMEZONE**: Your timezone as found at http://worldtimeapi.org/timezones
   1. **AIO_USERNAME**: Your Adafruit IO account username, https://io.adafruit.com/
   1. **AIO_KEY**: Your Adafruit IO account key
1. Update application_configuration.py in the src/conf folder
   1. **time_adjust**: Your timezone adjustment in seconds
   1. **enable_turntable**: Set to True if you built the turntable
   1. All other settings can be left alone for now for a quick start
1. Install the SplatSchedule_[date].uf2 firmware from the firmware folder
   1. Press the reset button on the back of the PyPortal twice quickly
   1. Copy the SplatSchedule_[date].uf2 to the PyPortal-Splatoon-2-Schedule-Display. The PyPortal will automatically reboot itself after the copy completes
1. Copy all the files from the src folder to the PyPortal

## Configurations

### application_configuration.py

Required:

* **battle_schedule_url**: URL to splatoon2.ink battle schedule json
* **salmon_schedule_url**: URL to splatoon2.ink salmon schedule json
* **time_adjust**: Time to adjust schedule to in seconds, sorry couldn't get this from the timezone in secrets.py
* **touchscreen_touch_throttle**: Seconds between touch repeating
* **sd_mount_directory**: Directory to mount an SD card to
* **background_images_directory**: Directory containing your images
* **background_timeout**: How long to display a background for in seconds
* **schedule_change_timeout**: How long before reverting back to the current time slot in seconds 
* **schedule_refresh**: How long before getting latest schedules
* **enable_turntable**: Set to true if built the turntable stage

Optional:

* **debug**: Help aid in debugging
* **disable_wifi**: Help aid in debugging
* **use_test_files**: Help aid in debugging
* **test_battle_schedule_file**: Help aid in debugging
* **test_salmon_schedule_file**: Help aid in debugging

### text_configurations.py 

* **fonts_directory**: Directory containing fonts_directory
* **text_xxx**: How to display text (font, color, (x,y)).

## Firmware

See Building CircuitPython https://learn.adafruit.com/building-circuitpython?view=all

The following were frozen into the SplatSchedule_[date].uf2 firmware

* https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font
* https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* https://github.com/adafruit/Adafruit_CircuitPython_Display_Text
* https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI
* https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad
* https://github.com/adafruit/Adafruit_CircuitPython_Motor
* https://github.com/adafruit/Adafruit_CircuitPython_Register
* https://github.com/adafruit/Adafruit_CircuitPython_ADT7410
* https://github.com/adafruit/Adafruit_CircuitPython_LSM303
* https://github.com/adafruit/Adafruit_CircuitPython_miniQR
* https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
* https://github.com/adafruit/Adafruit_CircuitPython_SD
* https://github.com/adafruit/Adafruit_CircuitPython_ServoKit
* https://github.com/adafruit/Adafruit_CircuitPython_SlideShow
* https://github.com/adafruit/Adafruit_CircuitPython_TouchScreen
* https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel

### Known Issues

If you discover any bugs, feel free to create an issue on GitHub fork and
send a pull request.



## Authors

* bbtinkerer (https://github.com/bbtinkerer/)


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request


## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.