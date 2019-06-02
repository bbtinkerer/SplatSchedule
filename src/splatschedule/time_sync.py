import time
import gc
import rtc
from conf.secrets import secrets


class TimeSync:
    # RTC reset delay default to 8 hours, my PyPortal drifted ~2 minutes after 8 hours
    def __init__(self, wifi, rtc_reset_delay=28800, debug=False):
        self._debug = debug
        self._wifi = wifi
        self._rtc_reset_delay = rtc_reset_delay
        self._last_Rtc_set = None
        self.set_Rtc()

    def update(self):
        if self._wifi is None:
            return
        now = time.time()
        if now - self._last_Rtc_set > self._rtc_reset_delay:
            self.set_Rtc()

    def set_Rtc(self):
        if self._wifi is None:
            return
        TIME_SERVICE = "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s"
        # our strftime is %Y-%m-%d %H:%M:%S.%L %j %u %z %Z see http://strftime.net/ for decoding details
        # See https://apidock.com/ruby/DateTime/strftime for full options
        TIME_SERVICE_STRFTIME = '&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S.%25L+%25j+%25u+%25z+%25Z'
        api_url = None
        try:
            aio_username = secrets['aio_username']
            aio_key = secrets['aio_key']
        except KeyError:
            raise KeyError("\n\nOur time service requires a login/password to rate-limit. Please register for a free adafruit.io account and place the user/key in your secrets file under 'aio_username' and 'aio_key'")

        location = None
        location = secrets.get('timezone', location)

        if location:
            if self._debug:
                print("Getting time for timezone", location)
            api_url = (TIME_SERVICE + "&tz=%s") % (aio_username, aio_key, location)
        else:  # we'll try to figure it out from the IP address
            if self._debug:
                print("Getting time from IP address")
            api_url = TIME_SERVICE % (aio_username, aio_key)
        api_url += TIME_SERVICE_STRFTIME

        try:
            response = self._wifi.get(api_url)
            if self._debug:
                print("Time request: ", api_url)
                print("Time reply: ", response.text)
            times = response.text.split(' ')
            the_date = times[0]
            the_time = times[1]
            year_day = int(times[2])
            week_day = int(times[3])
            is_dst = None  # no way to know yet
        except KeyError:
            raise KeyError("Was unable to lookup the time, try setting secrets['timezone'] according to http://worldtimeapi.org/timezones")

        year, month, mday = [int(x) for x in the_date.split('-')]
        the_time = the_time.split('.')[0]
        hours, minutes, seconds = [int(x) for x in the_time.split(':')]
        now = time.struct_time((year, month, mday, hours, minutes, seconds, week_day, year_day, is_dst))
        rtc.RTC().datetime = now
        self._last_Rtc_set = time.mktime(now)
        # now clean up
        response.close()
        response = None
        gc.collect()

    def get_current_time(self):
        t = time.localtime()
        hour = t.tm_hour
        meridian = "AM" if hour < 12 else "PM"
        hour = hour % 12
        if hour == 0:
            hour = 12
        return "{0: >2}:{1:02d} {2}".format(hour, t.tm_min, meridian)
