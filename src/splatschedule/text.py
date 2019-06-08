from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from conf.text_configuration import configuration as config


class Text:
    def __init__(self, splash, debug=False):
        self._debug = debug
        self._splash = splash
        self._fonts_directory = config['fonts_directory']
        self._bitmap_fonts = {}
        self._texts = {}
        self._text_keys = []
        self._initialize_text_keys()
        self._preload_fonts()
        self._initialize_battle_texts()
        self._initialize_salmon_texts()

    def _initialize_text_keys(self):
        for key in config.keys():
            if key.startswith('text_'):
                self._text_keys.append(key)

    def _preload_fonts(self):
        if self._debug:
            print('_preload_fonts() start')

        # not the whole alphabet, just the letters that appear in the stage names
        # loaded faster than including extra unnecessary characters
        # not sure which character from the pyportal sample takes forever to load
        glyphs = b'ABCDFGHIKLMNOPRSTVWZabcdefghiklmnoprstuvwyz0123456789-: /'

        for key in self._text_keys:
            self._preload_font(key, glyphs)

        if self._debug:
            print('_preload_fonts() end')

    def _preload_font(self, key, glyphs):
        if self._debug:
            print('_preload_font(): start; key=' + key)

        font_name = config[key][0]
        font = self._fonts_directory + font_name

        if self._debug:
            print('preloading font: ' + font)

        if font_name not in self._bitmap_fonts:
            self._bitmap_fonts[font_name] = bitmap_font.load_font(font)
            self._bitmap_fonts[font_name].load_glyphs(glyphs)

        if self._debug:
            print('_preload_font(): end')

    def _initialize_battle_texts(self):
        for key in self._text_keys:
            if 'battle' in key:
                self._initialize_text(key)

    def _initialize_salmon_texts(self):
        for key in self._text_keys:
            if 'salmon' in key:
                self._initialize_text(key)

    def _initialize_text(self, key):
        text_config = config[key]
        font_name = text_config[0]
        color = config[key][1]
        x = config[key][2][0]
        y = config[key][2][1]
        if self._debug:
            print("font: {} color:{} x:{}, y:{}".format(font_name, hex(color), x, y))
        text = Label(self._bitmap_fonts[font_name], text='', max_glyphs=30)
        text.color = color
        text.x = x
        text.y = y
        self._texts[key] = text
        self._splash.append(text)
        if self._debug:
            print("end _initialize_text")

    def _update_battle_texts(self, slot):
        self._texts['text_battle_time_slot']._update_text(slot.time_slot)
        self._texts['text_battle_regular_stage_a']._update_text(slot.regular_stage_a)
        self._texts['text_battle_regular_stage_b']._update_text(slot.regular_stage_b)
        self._texts['text_battle_ranked_rule_name']._update_text(slot.ranked_rule_name)
        self._texts['text_battle_ranked_stage_a']._update_text(slot.ranked_stage_a)
        self._texts['text_battle_ranked_stage_b']._update_text(slot.ranked_stage_b)

    def _update_salmon_texts(self, slot):
        self._texts['text_salmon_time_slot']._update_text(slot.time_slot)
        self._texts['text_salmon_stage']._update_text(slot.stage)

    def print_battle_slot(self, schedule):
        self._update_battle_texts(schedule)

    def print_salmon_slot(self, schedule):
        self._update_salmon_texts(schedule)

    def clear(self):
        self._texts['text_battle_time_slot']._update_text('')
        self._texts['text_battle_regular_stage_a']._update_text('')
        self._texts['text_battle_regular_stage_b']._update_text('')
        self._texts['text_battle_ranked_rule_name']._update_text('')
        self._texts['text_battle_ranked_stage_a']._update_text('')
        self._texts['text_battle_ranked_stage_b']._update_text('')
        self._texts['text_salmon_time_slot']._update_text('')
        self._texts['text_salmon_stage']._update_text('')
