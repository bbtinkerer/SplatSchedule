configuration = {
    'battle_schedule_url': 'https://splatoon2.ink/data/schedules.json',
    'salmon_schedule_url': 'https://splatoon2.ink/data/coop-schedules.json',
    
    'time_service': "http://192.168.1.70:8080/data/time.txt?x-aio-key=%s&%s",
    'time_service_strftime': '&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S.%25L+%25j+%25u+%25z+%25Z',
    # Adafruit IO strftime is %Y-%m-%d %H:%M:%S.%L %j %u %z %Z see http://strftime.net/ for decoding details
    # See https://apidock.com/ruby/DateTime/strftime for full options

    'time_adjust': -36000,  # hours in seconds
    'touchscreen_touch_throttle': 2,
    'sd_mount_directory': '/sd',
    'background_images_directory': '/sd/backgrounds/',
    'background_timeout': 900,  # 900 = 15 minutes
    'schedule_change_timeout': 180,  # 180 = 3 minutes
    'schedule_refresh': 43200,  # 43200 = 12 hours

    # If you built the turntable stage, set to True
    'enable_turntable': False,

    # The follow are optional and used for testing and debuggin
    # 'debug': False,
    # 'disable_wifi': False,
    # 'use_test_files': False,
    # 'test_battle_schedule_file': '/test_battle_schedule.json',
    # 'test_salmon_schedule_file': '/test_salmon_schedule.json'
    }
