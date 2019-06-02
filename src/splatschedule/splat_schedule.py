import json
import time
import gc
from conf.application_configuration import configuration as config


class SplatSchedule:
    def __init__(self, refresh, wifi, debug=False):
        self._current_battle_index = 0
        self._battle_schedules_count = 0
        self._battle_schedules = []
        self._salmon_schedules = []
        self._refresh = refresh
        self._wifi = wifi
        self._debug = debug
        self._use_test_files = config['use_test_files']
        self._time_adjust = config['time_adjust']
        self._last_refresh = 0
        self.update()

    def update(self):
        # TODO timer so not contstantly calling
        now = time.time()

        if now - self._last_refresh > self._refresh:
            if self._debug:
                print("Schedule updating")
            # Getting MemoryError randomly, says socket cannot allocate 14916 bytes
            # when repopulating from the web. I went nuclear option and just flat out
            # reboot till can figure out the problem. Should have lots of memory left.
            try:
                self.populate_schedules()
            except MemoryError as error:
                print(error)
                import supervisor
                supervisor.reload()

    def populate_schedules(self):
        self._battle_schedules.clear()
        self._salmon_schedules.clear()
        gc.collect()
        if self._debug:
            print("fetching schedules via " + ("test files" if self._use_test_files else "wifi"))
        if self._use_test_files:
            self._populate_battle_schedule_from_file()
            self._populate_salmon_run_from_file()
        else:
            self._populate_battle_schedule_from_web()
            self._populate_salmon_run_from_web()
        self._last_refresh = time.time()

    def _populate_battle_schedule_from_file(self):
        file = open(config.get('test_battle_schedule_file'))
        json_text = file.read()
        self._parse_battle_json_text(json_text)

    def _populate_salmon_run_from_file(self):
        file = open(config.get('test_salmon_schedule_file'))
        json_text = file.read()
        self._parse_salmon_json_text(json_text)

    def _populate_battle_schedule_from_web(self):
        response = self._wifi.get_url_response_text(config['battle_schedule_url'])
        self._parse_battle_json_text(response)

    def _populate_salmon_run_from_web(self):
        response = self._wifi.get_url_response_text(config['salmon_schedule_url'])
        self._parse_salmon_json_text(response)

    def _parse_battle_json_text(self, json_text):
        json_full_schedule = json.loads(json_text)
        self._battle_schedules_count = len(json_full_schedule['regular'])
        for i in range(self._battle_schedules_count):
            regular_battle = json_full_schedule['regular'][i]
            ranked_battle = json_full_schedule['gachi'][i]
            league_battle = json_full_schedule['league'][i]
            start_time = regular_battle['start_time'] + self._time_adjust
            end_time = regular_battle['end_time'] + self._time_adjust
            self._battle_schedules.append({
                'start_time': start_time,
                'end_time': end_time,
                'time_slot': self._parse_battle_time_slot(start_time, end_time),
                'regular_rule_name': regular_battle['rule']['name'],
                'regular_stage_a': regular_battle['stage_a']['name'],
                'regular_stage_b': regular_battle['stage_b']['name'],
                'ranked_rule_name': ranked_battle['rule']['name'],
                'ranked_stage_a': ranked_battle['stage_a']['name'],
                'ranked_stage_b': ranked_battle['stage_b']['name'],
                'league_rule_name': league_battle['rule']['name'],
                'league_stage_a': league_battle['stage_a']['name'],
                'league_stage_b': league_battle['stage_b']['name']
            })

    def _parse_salmon_json_text(self, json_text):
        json_full_schedule = json.loads(json_text)
        self._salmon_schedules_count = len(json_full_schedule['details'])
        for i in range(self._salmon_schedules_count):
            salmon_run = json_full_schedule['details'][i]
            start_time = salmon_run['start_time'] + self._time_adjust
            end_time = salmon_run['end_time'] + self._time_adjust
            self._salmon_schedules.append({
                'start_time': start_time,
                'end_time': end_time,
                'time_slot': self._parse_salmon_time_slot(start_time, end_time),
                'stage': salmon_run['stage']['name']
            })

    def _parse_battle_time_slot(self, start_time, end_time):
        time_hash = self._create_time_hash(start_time, end_time)
        time_slot_text = '{start_month}/{start_day}/{start_year} {start_hour}:{start_minute:02d}{start_meridian} - {end_hour}:{end_minute:02d}{end_meridian}'
        return time_slot_text.format(**time_hash)

    def _parse_salmon_time_slot(self, start_time, end_time):
        time_hash = self._create_time_hash(start_time, end_time)
        time_slot_text = '{start_month}/{start_day} {start_hour}:{start_minute:02d}{start_meridian} - {end_month}/{end_day} {end_hour}:{end_minute:02d}{end_meridian}'
        return time_slot_text.format(**time_hash)

    def _create_time_hash(self, start_time, end_time):
        start = time.localtime(start_time)
        end = time.localtime(end_time)
        time_hash = {
            'start_month': start.tm_mon,
            'start_day': start.tm_mday,
            'start_year': start.tm_year,
            'start_hour': self._convert_to_12hour(start.tm_hour),
            'start_minute': start.tm_min,
            'start_meridian': self._get_meridian(start.tm_hour),
            'end_month': end.tm_mon,
            'end_day': end.tm_mday,
            'end_year': end.tm_year,
            'end_hour': self._convert_to_12hour(end.tm_hour),
            'end_minute': end.tm_min,
            'end_meridian': self._get_meridian(end.tm_hour)
        }
        return time_hash

    def _convert_to_12hour(self, hour):
        h = hour % 12
        if h == 0:
            h = 12
        return h

    def _get_meridian(self, hour):
        return "AM" if hour < 12 else "PM"

    def get_current_battle(self):
        return self._battle_schedules[self._current_battle_index]

    def get_next_battle(self):
        self._current_battle_index = (self._current_battle_index + 1) % self._battle_schedules_count
        return self.get_current_battle()

    def get_previous_battle(self):
        self._current_battle_index = (self._current_battle_index - 1)
        if self._current_battle_index < 0:
            self._current_battle_index = self._battle_schedules_count - 1
        return self.get_current_battle()

    def set_current_battle(self, time):
        self._current_battle_index = 0
        for i in range(self._battle_schedules_count):
            schedule = self._battle_schedules[i]
            start_time = schedule['start_time']
            end_time = schedule['end_time']
            if start_time <= time and time < end_time:
                self._current_battle_index = i
                return

    def print_battle_schedule(self):
        for game in self._battle_schedules:
            print(game)

    def get_current_salmon(self):
        return self._salmon_schedules[self._current_salmon_index]

    def get_next_salmon(self):
        self._current_salmon_index = (self._current_salmon_index + 1) % self._salmon_schedules_count
        return self.get_current_salmon()

    def get_previous_salmon(self):
        self._current_salmon_index = (self._current_salmon_index - 1)
        if self._current_salmon_index < 0:
            self._current_salmon_index = self._salmon_schedules_count - 1
        return self.get_current_salmon()

    def set_current_salmon(self, time):
        self._current_salmon_index = 0
        for i in range(self._salmon_schedules_count):
            schedule = self._salmon_schedules[i]
            start_time = schedule['start_time']
            end_time = schedule['end_time']
            if start_time <= time and time < end_time:
                self._current_salmon_index = i
                return

    def print_salmon_schedule(self):
        for game in self._salmon_schedules:
            print(game)
