import json
import time
import gc
from conf.application_configuration import configuration as config


class ScheduleBattleSlot:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.time_slot = None
        self.regular_rule_name = None
        self.regular_stage_a = None
        self.regular_stage_b = None
        self.ranked_rule_name = None
        self.ranked_stage_a = None
        self.ranked_stage_b = None
        self.league_rule_name = None
        self.league_stage_a = None
        self.league_stage_b = None


class ScheduleSalmonSlot:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.time_slot = None
        self.stage = None


class SplatSchedule:
    BATTLE_SLOTS_COUNT = const(12)
    SALMON_SLOTS_COUNT = const(2)

    def __init__(self, wifi, debug=False):
        self._current_battle_index = 0
        self._battle_schedules = [ScheduleBattleSlot() for _ in range(BATTLE_SLOTS_COUNT)]
        self._salmon_schedules = [ScheduleSalmonSlot() for _ in range(SALMON_SLOTS_COUNT)]
        self._wifi = wifi
        self._debug = debug
        self._time_adjust = config['time_adjust']
        self._use_test_files = config.get('use_test_files')
        if self._use_test_files:
            self._test_battle_schedule_file = config.get('test_battle_schedule_file')
            self._test_salmon_schedule_file = config.get('test_salmon_schedule_file')
        else:
            self._battle_schedule_url = config['battle_schedule_url']
            self._salmon_schedule_url = config['salmon_schedule_url']
        self.populate_schedules()

    def clear_schedules(self):
        for slot in self._battle_schedules:
            slot.start_time = None
            slot.end_time = None
            slot.time_slot = None
            slot.regular_rule_name = None
            slot.regular_stage_a = None
            slot.regular_stage_b = None
            slot.ranked_rule_name = None
            slot.ranked_stage_a = None
            slot.ranked_stage_b = None
            slot.league_rule_name = None
            slot.league_stage_a = None
            slot.league_stage_b = None
        for slot in self._salmon_schedules:
            slot.start_time = None
            slot.end_time = None
            slot.time_slot = None
            slot.stage = None

    def populate_schedules(self):
        if self._debug:
            print("fetching schedules via " + ("test files" if self._use_test_files else "wifi"))
        if self._use_test_files:
            self._populate_battle_schedule_from_file()
            self._populate_salmon_run_from_file()
        else:
            self._populate_from_web()

    def _populate_from_web(self):
        if self._debug:
            print("Schedule updating")
        success = False
        retries = 5
        while not success and retries > 0:
            try:
                self.clear_schedules()
                self._populate_battle_schedule_from_web()
                self._populate_salmon_run_from_web()
                success = True
            except Exception as exception:
                print('Error getting schedule from web: ', exception)
                time.sleep(30)
                retries = retries - 1
        if not success:
            import supervisor
            supervisor.reload()

    def _populate_battle_schedule_from_file(self):
        file = open(self._test_battle_schedule_file)
        json_text = file.read()
        self._parse_battle_json_text(json_text)

    def _populate_salmon_run_from_file(self):
        file = open(self._test_salmon_schedule_file)
        json_text = file.read()
        self._parse_salmon_json_text(json_text)

    def _populate_battle_schedule_from_web(self):
        response = self._wifi.get_url_response_text(self._battle_schedule_url)
        self._parse_battle_json_text(response)

    def _populate_salmon_run_from_web(self):
        response = self._wifi.get_url_response_text(self._salmon_schedule_url)
        self._parse_salmon_json_text(response)

    def _parse_battle_json_text(self, json_text):
        json_full_schedule = json.loads(json_text)
        for i in range(BATTLE_SLOTS_COUNT):
            regular_battle = json_full_schedule['regular'][i]
            ranked_battle = json_full_schedule['gachi'][i]
            league_battle = json_full_schedule['league'][i]
            start_time = regular_battle['start_time'] + self._time_adjust
            end_time = regular_battle['end_time'] + self._time_adjust
            slot = self._battle_schedules[i]
            slot.start_time = start_time
            slot.end_time = end_time
            slot.time_slot = self._parse_battle_time_slot(start_time, end_time)
            slot.regular_rule_name = regular_battle['rule']['name']
            slot.regular_stage_a = regular_battle['stage_a']['name']
            slot.regular_stage_b = regular_battle['stage_b']['name']
            slot.ranked_rule_name = ranked_battle['rule']['name']
            slot.ranked_stage_a = ranked_battle['stage_a']['name']
            slot.ranked_stage_b = ranked_battle['stage_b']['name']
            slot.league_rule_name = league_battle['rule']['name']
            slot.league_stage_a = league_battle['stage_a']['name']
            slot.league_stage_b = league_battle['stage_b']['name']

    def _parse_salmon_json_text(self, json_text):
        json_full_schedule = json.loads(json_text)
        for i in range(SALMON_SLOTS_COUNT):
            salmon_run = json_full_schedule['details'][i]
            start_time = salmon_run['start_time'] + self._time_adjust
            end_time = salmon_run['end_time'] + self._time_adjust
            slot = self._salmon_schedules[i]
            slot.start_time = start_time
            slot.end_time = end_time
            slot.time_slot = self._parse_salmon_time_slot(start_time, end_time)
            slot.stage = salmon_run['stage']['name']

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
        self._current_battle_index = (self._current_battle_index + 1) % BATTLE_SLOTS_COUNT
        return self.get_current_battle()

    def get_previous_battle(self):
        self._current_battle_index = (self._current_battle_index - 1)
        if self._current_battle_index < 0:
            self._current_battle_index = BATTLE_SLOTS_COUNT - 1
        return self.get_current_battle()

    def set_current_battle(self, time):
        self._current_battle_index = 0
        for i in range(BATTLE_SLOTS_COUNT):
            slot = self._battle_schedules[i]
            start_time = slot.start_time
            end_time = slot.end_time
            if start_time <= time and time < end_time:
                self._current_battle_index = i
                return

    def get_current_salmon(self):
        return self._salmon_schedules[self._current_salmon_index]

    def get_next_salmon(self):
        self._current_salmon_index = (self._current_salmon_index + 1) % SALMON_SLOTS_COUNT
        return self.get_current_salmon()

    def get_previous_salmon(self):
        self._current_salmon_index = (self._current_salmon_index - 1)
        if self._current_salmon_index < 0:
            self._current_salmon_index = SALMON_SLOTS_COUNT - 1
        return self.get_current_salmon()

    def set_current_salmon(self, time):
        self._current_salmon_index = 0
        for i in range(SALMON_SLOTS_COUNT):
            slot = self._salmon_schedules[i]
            start_time = slot.start_time
            end_time = slot.end_time
            if start_time <= time and time < end_time:
                self._current_salmon_index = i
                return
