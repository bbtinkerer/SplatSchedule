# PyPortal Splatoon 2 Schedule Display

By bbtinkerer (<http://bb-tinkerer.blogspot.com/>)

## Description

Splatoon 2 Schedule display with PyPortal. Displays the stages, Ranked Type game, and Salmon Run schedule.  Use the touch screen to cycle through upcoming stages, ranked games, and Salmon Run.

Requires an Adafruit IO Account (https://io.adafruit.com/) for setting time.

Optional simple Amiibo animaltronics just for some hardware motion fun.

Instructables project at TBA

3D Files will be on Thingiverse.com

## Dependencies

* Adafruit CircuitPython 4.0.0 for PyPortal https://circuitpython.org/board/pyportal/
* Adafruit CircuitPython Libraries 4.x https://circuitpython.org/libraries

## Setup

1. Rename secrets.example.py to secrets.py in the conf folder.
1. Update secrets.py
   1. **SSID**: Your WiFi network name
   1. **PWD**: Your WiFi password
   1. **TIMEZONE**: Your timezone as found at http://worldtimeapi.org/timezones
   1. **AIO_USERNAME**: Your Adafruit IO account username, https://io.adafruit.com/
   1. **AIO_KEY**: Your Adafruit IO account key

## Configurations

### application_configuration.py

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
* **debug**: Help aid in debugging
* **disable_wifi**: Help aid in debugging
* **use_test_files**: Help aid in debugging
* **test_battle_schedule_file**: Help aid in debugging
* **test_salmon_schedule_file**: Help aid in debugging

### text_configurations.py 

* **fonts_directory**: Directory containing fonts_directory
* **text_xxx**: How to display text (font, color, (x,y)).

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