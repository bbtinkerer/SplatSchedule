configuration = {
    'battle_schedule_url': 'https://splatoon2.ink/data/schedules.json',
    'salmon_schedule_url': 'https://splatoon2.ink/data/coop-schedules.json',
    'time_adjust': -36000,  # hours in seconds
    'touchscreen_touch_throttle': 2,
    'sd_mount_directory': '/sd',
    'background_images_directory': '/sd/backgrounds/',
    'background_timeout': 900,  # 900 = 15 minutes
    'schedule_change_timeout': 180,  # 180 = 3 minutes
    'schedule_refresh': 43200,  # 43200 = 12 hours

    # if built the turntable stage
    'enable_turntable': True,

    # the following is for testing
    'debug': False,
    'disable_wifi': False,
    'use_test_files': False,
    'test_battle_schedule_file': '/test_battle_schedule.json',
    'test_salmon_schedule_file': '/test_salmon_schedule.json'
    }
