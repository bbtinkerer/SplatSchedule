import time
import gc
import rtc
from conf.secrets import secrets
from conf.application_configuration import configuration as config


class TimeSync:
    # RTC reset delay default to 8 hours, my PyPortal drifted ~2 minutes after 8 hours
    def __init__(self, wifi, rtc_reset_delay=28800, debug=False):
        self._debug = debug
        self._wifi = wifi
        self._rtc_reset_delay = rtc_reset_delay
        self._last_Rtc_set = None
        self._time_service_strftime = config['time_service_strftime']
        self._time_service = config['time_service']
        self._aio_username = secrets['aio_username']
        self._aio_key = secrets['aio_key']
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
        api_url = None

        location = None
        location = secrets.get('timezone', location)

        if location:
            if self._debug:
                print("Getting time for timezone", location)
            api_url = (self._time_service + "&tz=%s") % (self._aio_username, self._aio_key, location)
        else:  # we'll try to figure it out from the IP address
            if self._debug:
                print("Getting time from IP address")
            api_url = self._time_service % (self._aio_username, self._aio_key)
        api_url += self._time_service_strftime

        try:
            response_text = self._wifi.get_url_response_text(api_url)
            if self._debug:
                print("Time request: ", api_url)
                print("Time reply: ", response_text)
            times = response_text.split(' ')
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
