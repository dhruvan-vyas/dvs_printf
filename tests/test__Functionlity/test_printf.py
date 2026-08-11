from contextlib import contextmanager
from dvs_printf import printf, console_EnvType
from io import StringIO
import sys

@contextmanager
def capture_output():
    """Capture both print() and dvs_printf.printf() output."""
    old_stdout = sys.stdout
    buffer = StringIO()
    sys.stdout = buffer

    # Patch dvs_printf internal _write/_flush to also go into buffer
    # import dvs_printf
    from dvs_printf import console
    console._write = buffer.write
    console._flush = buffer.flush
    old_write, old_flush = console._write, console._flush
    console._write = buffer.write
    console._flush = buffer.flush

    try:
        yield buffer
    finally:
        # Restore everything
        sys.stdout = old_stdout
        console._write, console._flush = old_write, old_flush

def get_output(buffer: StringIO):
    """Return full output and also line-by-line list."""
    buffer.flush()
    text = buffer.getvalue()
    return text, text.splitlines()


# =================================(Way To Use)======================
# with capture_output() as buf:
#     printf("hello world \nthis is Animation",
#            style="typing", color=("red", "blue"), speed=7)

# # # Get everything
# # full, lines = get_output(buf)

# # print("FULL:", repr(full))
# # print("LINES:", lines)
# ===================================================================



expected_output = [
    '\x1b[?25lh|\x08e|\x08l|\x08l|\x08o|\x08 |\x08w|\x08o|\x08r|\x08l|\x08d|\x08 \ns|\x08t|\x08y|\x08l|\x08e|\x08 |\x08t|\x08e|\x08s|\x08t|\x08 \n\x1b[?25h',
    '\x1b[?25ld\rld\rrld\rorld\rworld\r world\ro world\rlo world\rllo world\rello world\rhello world\r\nt\rst\rest\rtest\r test\re test\rle test\ryle test\rtyle test\rstyle test\r\n\x1b[?25h',
    '\x1b[?25l    o \r   lo w\r  llo wo\r ello wor\rhello world\r\n    e \r   le t\r  yle te\r tyle tes\rstyle test\r\n\x1b[?25h',
    '\x1b[?25l h\rh e\rhe l\rhel l\rhell o\rhello  \rhello  w\rhello w o\rhello wo r\rhello wor l\rhello worl d\rhello world \r\n '
        's\rs t\rst y\rsty l\rstyl e\rstyle  \rstyle  t\rstyle t e\rstyle te s\rstyle tes t\rstyle test \r\n\x1b[?25h',
]




expected_colored_output = (
    '\x1b[?25l\x1b[38;2;232;0;22mh\x1b[39m|\x08\x1b[38;2;217;0;37me\x1b[39m|\x08\x1b[38;2;210;0;45ml\x1b[39m|\x08\x1b[38;2;202;0;52ml\x1b[39m|\x08\x1b[38;2;187;0;67mo\x1b[39m|\x08\x1b[38;2;180;0;75m '
    '\x1b[39m|\x08\x1b[38;2;165;0;90mw\x1b[39m|\x08\x1b[38;2;157;0;97mo\x1b[39m|\x08\x1b[38;2;150;0;105mr\x1b[39m|\x08\x1b[38;2;135;0;120ml\x1b[39m|\x08\x1b[38;2;127;0;127md\x1b[39m|\x08\x1b[38;2;112;0;142m '
    '\x1b[39m|\x08 \n\x1b[38;2;217;0;37mt\x1b[39m|\x08\x1b[38;2;210;0;45mh\x1b[39m|\x08\x1b[38;2;202;0;52mi\x1b[39m|\x08\x1b[38;2;187;0;67ms\x1b[39m|\x08\x1b[38;2;180;0;75m \x1b[39m|\x08\x1b[38;2;165;0;90mi'
    '\x1b[39m|\x08\x1b[38;2;157;0;97ms\x1b[39m|\x08\x1b[38;2;150;0;105m \x1b[39m|\x08\x1b[38;2;135;0;120mA\x1b[39m|\x08\x1b[38;2;127;0;127mn\x1b[39m|\x08\x1b[38;2;112;0;142mi\x1b[39m|\x08\x1b[38;2;105;0;150mm'
    '\x1b[39m|\x08\x1b[38;2;97;0;157ma\x1b[39m|\x08\x1b[38;2;82;0;172mt\x1b[39m|\x08\x1b[38;2;75;0;180mi\x1b[39m|\x08\x1b[38;2;60;0;195mo\x1b[39m|\x08\x1b[38;2;52;0;202mn\x1b[39m|\x08 \n\x1b[?25h'
    , # ^ Console Env Type 1  

    '\x1b[?25l\x1b[38;5;196mh\x1b[39m|\x08\x1b[38;5;161me\x1b[39m|\x08\x1b[38;5;161ml\x1b[39m|\x08\x1b[38;5;161ml\x1b[39m|\x08\x1b[38;5;161mo\x1b[39m|\x08\x1b[38;5;161m \x1b[39m|\x08\x1b[38;5;126mw\x1b[39m|'
    '\x08\x1b[38;5;126mo\x1b[39m|\x08\x1b[38;5;126mr\x1b[39m|\x08\x1b[38;5;126ml\x1b[39m|\x08\x1b[38;5;90md\x1b[39m|\x08\x1b[38;5;91m \x1b[39m|\x08 \n\x1b[38;5;161mt\x1b[39m|\x08\x1b[38;5;161mh\x1b[39m|'
    '\x08\x1b[38;5;161mi\x1b[39m|\x08\x1b[38;5;161ms\x1b[39m|\x08\x1b[38;5;161m \x1b[39m|\x08\x1b[38;5;126mi\x1b[39m|\x08\x1b[38;5;126ms\x1b[39m|\x08\x1b[38;5;126m \x1b[39m|\x08\x1b[38;5;126mA\x1b[39m|'
    '\x08\x1b[38;5;90mn\x1b[39m|\x08\x1b[38;5;91mi\x1b[39m|\x08\x1b[38;5;91mm\x1b[39m|\x08\x1b[38;5;91ma\x1b[39m|\x08\x1b[38;5;91mt\x1b[39m|\x08\x1b[38;5;56mi\x1b[39m|\x08\x1b[38;5;56mo\x1b[39m|'
    '\x08\x1b[38;5;56mn\x1b[39m|\x08 \n\x1b[?25h'
    , # ^ Console Env Type 2 

    '\x1b[?25l\x1b[31mh\x1b[39m|\x08\x1b[31me\x1b[39m|\x08\x1b[31ml\x1b[39m|\x08\x1b[31ml\x1b[39m|\x08\x1b[31mo\x1b[39m|\x08\x1b[31m \x1b[39m|\x08\x1b[31mw\x1b[39m|\x08\x1b[31mo\x1b[39m|\x08\x1b[31mr\x1b[39m|'
    '\x08\x1b[31ml\x1b[39m|\x08\x1b[35md\x1b[39m|\x08\x1b[34m \x1b[39m|\x08 \n\x1b[31mt\x1b[39m|\x08\x1b[31mh\x1b[39m|\x08\x1b[31mi\x1b[39m|\x08\x1b[31ms\x1b[39m|\x08\x1b[31m \x1b[39m|\x08\x1b[31mi\x1b[39m|'
    '\x08\x1b[31ms\x1b[39m|\x08\x1b[31m \x1b[39m|\x08\x1b[31mA\x1b[39m|\x08\x1b[35mn\x1b[39m|\x08\x1b[34mi\x1b[39m|\x08\x1b[34mm\x1b[39m|\x08\x1b[34ma\x1b[39m|\x08\x1b[34mt\x1b[39m|\x08\x1b[34mi\x1b[39m|'
    '\x08\x1b[34mo\x1b[39m|\x08\x1b[34mn\x1b[39m|\x08 \n\x1b[?25h'
    , # ^ Console Env Type 3 

    '\x1b[?25lh\x1b[39m|\x08e\x1b[39m|\x08l\x1b[39m|\x08l\x1b[39m|\x08o\x1b[39m|\x08 \x1b[39m|\x08w\x1b[39m|\x08o\x1b[39m|\x08r\x1b[39m|\x08l\x1b[39m|\x08d\x1b[39m|\x08 \x1b[39m|\x08 \nt\x1b[39m|\x08h\x1b[39m|'
    '\x08i\x1b[39m|\x08s\x1b[39m|\x08 \x1b[39m|\x08i\x1b[39m|\x08s\x1b[39m|\x08 \x1b[39m|\x08A\x1b[39m|\x08n\x1b[39m|\x08i\x1b[39m|\x08m\x1b[39m|\x08a\x1b[39m|\x08t\x1b[39m|\x08i\x1b[39m|\x08o\x1b[39m|'
    '\x08n\x1b[39m|\x08 \n\x1b[?25h'
    , # ^ Console Env Type 4
)

# '\x1b[?25l\x1b[38;2;232;0;22mh\x1b[39m|\x08\x1b[38;2;217;0;37me\x1b[39m|\x08\x1b[38;2;210;0;45ml\x1b[39m|\x08\x1b[38;2;202;0;52ml\x1b[39m|\x08\x1b[38;2;187;0;67mo\x1b[39m|\x08\x1b[38;2;180;0;75m \x1b[39m|\x08\x1b[38;2;165;0;90mw\x1b[39m|\x08\x1b[38;2;157;0;97mo\x1b[39m|\x08\x1b[38;2;150;0;105mr\x1b[39m|\x08\x1b[38;2;135;0;120ml\x1b[39m|\x08\x1b[38;2;127;0;127md\x1b[39m|\x08\x1b[38;2;112;0;142m \x1b[39m|\x08 \n\x1b[38;2;217;0;37mt\x1b[39m|\x08\x1b[38;2;210;0;45mh\x1b[39m|\x08\x1b[38;2;202;0;52mi\x1b[39m|\x08\x1b[38;2;187;0;67ms\x1b[39m|\x08\x1b[38;2;180;0;75m \x1b[39m|\x08\x1b[38;2;165;0;90mi\x1b[39m|\x08\x1b[38;2;157;0;97ms\x1b[39m|\x08\x1b[38;2;150;0;105m \x1b[39m|\x08\x1b[38;2;135;0;120mA\x1b[39m|\x08\x1b[38;2;127;0;127mn\x1b[39m|\x08\x1b[38;2;112;0;142mi\x1b[39m|\x08\x1b[38;2;105;0;150mm\x1b[39m|\x08\x1b[38;2;97;0;157ma\x1b[39m|\x08\x1b[38;2;82;0;172mt\x1b[39m|\x08\x1b[38;2;75;0;180mi\x1b[39m|\x08\x1b[38;2;60;0;195mo\x1b[39m|\x08\x1b[38;2;52;0;202mn\x1b[39m|\x08 \n\x1b[?25h'
# '\x1b[?25l\x1b[38;2;232;0;22mh\x1b[39m|\x08\x1b[38;2;217;0;37me\x1b[39m|\x08\x1b[38;2;210;0;45ml\x1b[39m|\x08\x1b[38;2;202;0;52ml\x1b[39m|\x08\x1b[38;2;187;0;67mo\x1b[39m|\x08\x1b[38;2;180;0;75m \x1b[39m|\x08\x1b[38;2;165;0;90mw\x1b[39m|\x08\x1b[38;2;157;0;97mo\x1b[39m|\x08\x1b[38;2;150;0;105mr\x1b[39m|\x08\x1b[38;2;135;0;120ml\x1b[39m|\x08\x1b[38;2;127;0;127md\x1b[39m|\x08\x1b[38;2;112;0;142m \x1b[39m|\x08 \n\x1b[38;2;105;0;150mt\x1b[39m|\x08\x1b[38;2;97;0;157mh\x1b[39m|\x08\x1b[38;2;82;0;172mi\x1b[39m|\x08\x1b[38;2;75;0;180ms\x1b[39m|\x08\x1b[38;2;60;0;195m \x1b[39m|\x08\x1b[38;2;217;0;37mi\x1b[39m|\x08\x1b[38;2;210;0;45ms\x1b[39m|\x08\x1b[38;2;202;0;52m \x1b[39m|\x08\x1b[38;2;187;0;67mA\x1b[39m|\x08\x1b[38;2;180;0;75mn\x1b[39m|\x08\x1b[38;2;165;0;90mi\x1b[39m|\x08\x1b[38;2;157;0;97mm\x1b[39m|\x08\x1b[38;2;150;0;105ma\x1b[39m|\x08\x1b[38;2;135;0;120mt\x1b[39m|\x08\x1b[38;2;127;0;127mi\x1b[39m|\x08\x1b[38;2;112;0;142mo\x1b[39m|\x08\x1b[38;2;105;0;150mn\x1b[39m|\x08 \n\x1b[?25h'

def test_printf_color():
    with capture_output() as buf:
        printf("hello world \nthis is Animation", 
               style="typing", 
               color=("red", "blue"), 
               speed=7
            )
    full, _ = get_output(buf)
    assert expected_colored_output[console_EnvType-1] == f'{full}' 
    # console_EnvType range:  (1 to 4), 
    # console_EnvType-1: convert tuple range (0 to 3) for expected_colored_output 

def test_printf_style():
    with capture_output() as buf:
        printf("hello world","style test", speed=7)
    full, _ = get_output(buf)
    assert expected_output[0] == f'{full}' 
    with capture_output() as buf:
        printf("hello world","style test", style="left", speed=7)
    full, _ = get_output(buf)
    assert expected_output[1] == f'{full}' 
    with capture_output() as buf:
        printf("hello world","style test", style="mid", speed=7)
    full, _ = get_output(buf)
    assert expected_output[2] == f'{full}' 
    with capture_output() as buf:
        printf("hello world","style test", style="fire", speed=7)
    full, _ = get_output(buf)
    assert expected_output[3] == f'{full}' 


# from time import time_ns

# start = time_ns()
# printf("hello world \nthis is Animation", 'this is any other thing that can be done while dont any thng',
#                style="typing", 
#                color=("red", "blue"), 
#                speed=7
#             )
# end = time_ns()
# print()
