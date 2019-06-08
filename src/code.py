import board
import busio
import random
import time
import gc
import adafruit_sdcard
from digitalio import DigitalInOut
import storage
from conf.application_configuration import configuration as config
from splatschedule.splat_schedule import SplatSchedule
from splatschedule.wifi import WiFi
from splatschedule.time_sync import TimeSync
from splatschedule.touch import Touch
from splatschedule.display import Display
from splatschedule.text import Text
from splatschedule.background_randomizer import BackgroundRandomizer
from splatschedule.turntable import Turntable, FakeTurntable

debug = True if config.get('debug') else False

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

if debug:
    print("Init SD Card")
sd_cs = DigitalInOut(board.SD_CS)
sdcard = None
try:
    sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, config['sd_mount_directory'])
except OSError as error:
    print("No SD card found:", error)

# initializing
turn_table = Turntable(debug=debug) if config.get('enable_turntable') else FakeTurntable(debug=debug)
display = Display()
wifi = None if config.get('disable_wifi') else WiFi(spi, debug=debug)
time_sync = TimeSync(wifi)
background = BackgroundRandomizer(display, config['background_images_directory'], config['background_timeout'], debug)
text = Text(display.splash, debug=debug)
touch = Touch(config['touchscreen_touch_throttle'])
current_time = time.time()
schedule_change_timeout = config['schedule_change_timeout']
schedule_time_set = current_time
schedule_changed = False
schedule = SplatSchedule(wifi, debug)
schedule_refresh = config['schedule_refresh']
last_schedule_refresh = current_time
point = None
last_time_check = current_time
# the initial display of schedule
schedule.set_current_battle(current_time)
text.print_battle_slot(schedule.get_current_battle())
schedule.set_current_salmon(current_time)
text.print_salmon_slot(schedule.get_current_salmon())


def refresh_schedule():
    global last_schedule_refresh
    background.clear_background()
    text.clear()
    schedule.populate_schedules()
    background.display_background()
    schedule.set_current_battle(current_time)
    text.print_battle_slot(schedule.get_current_battle())
    schedule.set_current_salmon(current_time)
    text.print_salmon_slot(schedule.get_current_salmon())
    last_schedule_refresh = current_time

while True:
    time_sync.update()
    turn_table.update()
    background.update()
    current_time = time.time()

    # check to see if need to page forward/back through schedule if the user touched the screen
    point = touch.touch_point()
    if point is not None:
        turn_table.turn_in()
        x, y, z = point
        schedule_time_set = current_time
        schedule_changed = True
        if debug:
            print("touched: ({0}, {1})".format(x, y))
        if y < 190:
            if x >= 160:
                text.print_battle_slot(schedule.get_next_battle())
            else:
                text.print_battle_slot(schedule.get_previous_battle())
        else:
            if x >= 160:
                text.print_salmon_slot(schedule.get_next_salmon())
            else:
                text.print_salmon_slot(schedule.get_previous_salmon())

    # change the displayed schedule back to the current schedule if the user changed
    if schedule_changed and (current_time - schedule_time_set > schedule_change_timeout):
        turn_table.turn_in()
        schedule.set_current_battle(current_time)
        text.print_battle_slot(schedule.get_current_battle())
        schedule.set_current_salmon(current_time)
        text.print_salmon_slot(schedule.get_current_salmon())
        schedule_time_set = current_time
        schedule_changed = False

    # checking the time every minute to see if need to update displayed schedule
    if not schedule_changed and current_time - last_time_check > 60:
        last_time_check = current_time
        displayed_battle = schedule.get_current_battle()
        displayed_salmon = schedule.get_current_salmon()
        if current_time > displayed_battle.end_time:
            turn_table.turn_in()
            schedule.set_current_battle(current_time)
            text.print_battle_slot(schedule.get_current_battle())
        if current_time > displayed_salmon.end_time:
            turn_table.turn_in()
            schedule.set_current_salmon(current_time)
            text.print_salmon_slot(schedule.get_current_salmon())

    if current_time - last_schedule_refresh > schedule_refresh:
        refresh_schedule()
