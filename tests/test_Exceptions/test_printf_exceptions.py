from dvs_printf import printf, console_EnvType

if console_EnvType == 1:
    error_massages = {
        "style": '\x1b[38;2;155;82;199mStyleNameError\x1b[0m: The style \x1b[38;2;110;118;129m"none"\x1b[0m is not defined. Please check the available styles.',
        "speed": '\x1b[38;2;155;82;199mSpeedValueError\x1b[0m: The speed value must be of type \x1b[38;2;110;118;129mint\x1b[0m or \x1b[38;2;110;118;129mfloat\x1b[0m, and a value between \x1b[38;2;206;145;120m1\x1b[0m to \x1b[38;2;206;145;120m6\x1b[0m, or exactly \x1b[38;2;206;145;120m7\x1b[0m. \n\x1b[38;2;155;82;199mReceived\x1b[0m: \x1b[38;2;110;118;129m10\x1b[0m, type: \x1b[38;2;110;118;129mstr\x1b[0m.',
        "delay": '\x1b[38;2;155;82;199mDelayValueError\x1b[0m: The delay value must be of type (\x1b[38;2;110;118;129mint\x1b[0m or \x1b[38;2;110;118;129mfloat\x1b[0m), and a non-negative number (>= \x1b[38;2;206;145;120m0\x1b[0m). Received: \x1b[38;2;110;118;129mFalse\x1b[0m (type: \x1b[38;2;110;118;129mstr\x1b[0m).',
        "attrs": '\x1b[38;2;155;82;199mAttrsValueError\x1b[0m: The `attrs` must be a list of strings (List[str]) from the available attributes.\nReceived: \x1b[38;2;110;118;129m10\x1b[0m, type: int.\n\n\x1b[38;2;206;145;120mTip: try using `list(FontStyles.ATTR_MAP)` to see the valid options.\x1b[0m',
        "color": '\x1b[38;2;155;82;199mColorsValueError\x1b[0m: Invalid hex color format or value. Got: #red',
        "getmat": "\x1b[38;2;155;82;199mGetMatValueError\x1b[0m: The `getmat` value must be one of the allowed values: \x1b[38;2;206;145;120mTrue, False, 'true', 'show'\x1b[0m.\nReceived: \x1b[38;2;110;118;129mmat\x1b[0m (type: \x1b[38;2;110;118;129mstr\x1b[0m).",
    }
elif console_EnvType == 2:
    error_massages = {
        'style': '\x1b[38;5;140mStyleNameError\x1b[0m: The style \x1b[38;5;103m"none"\x1b[0m is not defined. Please check the available styles.',
        'speed': '\x1b[38;5;140mSpeedValueError\x1b[0m: The speed value must be of type \x1b[38;5;103mint\x1b[0m or \x1b[38;5;103mfloat\x1b[0m, and a value between \x1b[38;5;180m1\x1b[0m to \x1b[38;5;180m6\x1b[0m, or exactly \x1b[38;5;180m7\x1b[0m. \n\x1b[38;5;140mReceived\x1b[0m: \x1b[38;5;103m10\x1b[0m, type: \x1b[38;5;103mstr\x1b[0m.',
        'delay': '\x1b[38;5;140mDelayValueError\x1b[0m: The delay value must be of type (\x1b[38;5;103mint\x1b[0m or \x1b[38;5;103mfloat\x1b[0m), and a non-negative number (>= \x1b[38;5;180m0\x1b[0m). Received: \x1b[38;5;103mFalse\x1b[0m (type: \x1b[38;5;103mstr\x1b[0m).',
        'attrs': '\x1b[38;5;140mAttrsValueError\x1b[0m: The `attrs` must be a list of strings (List[str]) from the available attributes.\nReceived: \x1b[38;5;103m10\x1b[0m, type: int.\n\n\x1b[38;5;180mTip: try using `list(FontStyles.ATTR_MAP)` to see the valid options.\x1b[0m',
        'color': '\x1b[38;5;140mColorsValueError\x1b[0m: Invalid hex color format or value. Got: #red',
        'getmat': "\x1b[38;5;140mGetMatValueError\x1b[0m: The `getmat` value must be one of the allowed values: \x1b[38;5;180mTrue, False, 'true', 'show'\x1b[0m.\nReceived: \x1b[38;5;103mmat\x1b[0m (type: \x1b[38;5;103mstr\x1b[0m).",
    }

elif console_EnvType == 3:
    error_massages = {
        'style': '\x1b[94mStyleNameError\x1b[0m: The style \x1b[90m"none"\x1b[0m is not defined. Please check the available styles.',
        'speed': '\x1b[94mSpeedValueError\x1b[0m: The speed value must be of type \x1b[90mint\x1b[0m or \x1b[90mfloat\x1b[0m, and a value between \x1b[91m1\x1b[0m to \x1b[91m6\x1b[0m, or exactly \x1b[91m7\x1b[0m. \n\x1b[94mReceived\x1b[0m: \x1b[90m10\x1b[0m, type: \x1b[90mstr\x1b[0m.',
        'delay': '\x1b[94mDelayValueError\x1b[0m: The delay value must be of type (\x1b[90mint\x1b[0m or \x1b[90mfloat\x1b[0m), and a non-negative number (>= \x1b[91m0\x1b[0m). Received: \x1b[90mFalse\x1b[0m (type: \x1b[90mstr\x1b[0m).',
        'attrs': '\x1b[94mAttrsValueError\x1b[0m: The `attrs` must be a list of strings (List[str]) from the available attributes.\nReceived: \x1b[90m10\x1b[0m, type: int.\n\n\x1b[91mTip: try using `list(FontStyles.ATTR_MAP)` to see the valid options.\x1b[0m',
        'color': '\x1b[94mColorsValueError\x1b[0m: Invalid hex color format or value. Got: #red',
        'getmat': "\x1b[94mGetMatValueError\x1b[0m: The `getmat` value must be one of the allowed values: \x1b[91mTrue, False, 'true', 'show'\x1b[0m.\nReceived: \x1b[90mmat\x1b[0m (type: \x1b[90mstr\x1b[0m).",
    }
    
else: error_massages = {
        'style': 'StyleNameError\x1b[0m: The style "none"\x1b[0m is not defined. Please check the available styles.',
        'speed': 'SpeedValueError\x1b[0m: The speed value must be of type int\x1b[0m or float\x1b[0m, and a value between 1\x1b[0m to 6\x1b[0m, or exactly 7\x1b[0m. \nReceived\x1b[0m: 10\x1b[0m, type: str\x1b[0m.',
        'delay': 'DelayValueError\x1b[0m: The delay value must be of type (int\x1b[0m or float\x1b[0m), and a non-negative number (>= 0\x1b[0m). Received: False\x1b[0m (type: str\x1b[0m).',
        'attrs': 'AttrsValueError\x1b[0m: The `attrs` must be a list of strings (List[str]) from the available attributes.\nReceived: 10\x1b[0m, type: int.\n\nTip: try using `list(FontStyles.ATTR_MAP)` to see the valid options.\x1b[0m',
        'color': 'ColorsValueError\x1b[0m: Invalid hex color format or value. Got: #red',
        'getmat': "GetMatValueError\x1b[0m: The `getmat` value must be one of the allowed values: True, False, 'true', 'show'\x1b[0m.\nReceived: mat\x1b[0m (type: str\x1b[0m).",
    }

def test_printf_keyword_style():
    try:   printf("hello world", style="none")
    except Exception as E: 
        assert str(E) == error_massages["style"]

def test_printf_keyword_speed():
    try:   printf("hello world", speed = '10')
    except Exception as E: assert str(E) == error_massages["speed"]

def test_printf_keyword_delay():
    try:   printf("hello world", delay="False")
    except Exception as E: assert str(E) == error_massages["delay"]

def test_printf_keyword_attrs():
    try:   printf("hello world", attrs=10)
    except Exception as E: assert str(E) == error_massages["attrs"]

def test_printf_keyword_color():
    try:   printf("hello world", color = ("#red"), )
    except Exception as E: assert str(E) == error_massages["color"]

def test_printf_keyword_getma():
    try:   printf("hello world", getmat="mat")
    except Exception as E: assert str(E) == error_massages["getmat"]
  



# '\x1b[38;2;155;82;199mColorsValueError\x1b[0m: Invalid hex color format or value. Got: #red' == 
# '\x1b[38;2;155;82;199mColorsValueError\x1b[0m: Invalid hex color format or value. Got: #red'