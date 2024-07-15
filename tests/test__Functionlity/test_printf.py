from io import StringIO
from contextlib import redirect_stdout
from dvs_printf import printf 

# #--------------------------------------------------------------------------------
# import sys
# def printf_output():
#     # Capture the output of printf
#     sys.stdout = captured_output = StringIO()
#     printf("hello world", "style test", style="left") # change name of style 

#     sys.stdout = sys.__stdout__
#     print(repr(captured_output.getvalue()))

# printf_output()   # values of your styles
# #--------------------------------------------------------------------------------


expected_output = [
'\x1b[?25lh|\x08e|\x08l|\x08l|\x08o|\x08 |\x08w|\x08o|\x08r|\x08l|\x08d|\x08 \ns|\x08t|\x08y|\x08l|\x08e|\x08 |\x08t|\x08e|\x08s|\x08t|\x08 \n\x1b[?25h', # typing
'\x1b[?25ld\rld\rrld\rorld\rworld\r world\ro world\rlo world\rllo world\rello world\rhello world\r\nt\rst\rest\rtest\r test\re test\rle test\ryle test\rtyle test\rstyle test\r\n\x1b[?25h', # left
'\x1b[?25l\x1b[?25l      w\r    o wo\r   lo wor\r  llo worl\r ello world\rhello world \r\n    e \r   le t\r  yle te\r tyle tes\rstyle test\r\n\x1b[?25h\x1b[?25h', # mid
'\x1b[?25l\x1b[?25l h\rh e\rhe l\rhel l\rhell o\rhello  \rhello  w\rhello w o\rhello wo r\rhello wor l\rhello worl d\rhello world \r\n s\rs t\rst y\rsty l\rstyl e\
\rstyle  \rstyle  t\rstyle t e\rstyle te s\rstyle tes t\rstyle test \r\n\x1b[?25h\x1b[?25h' # fire
]

def test_printf_style():
    typing = StringIO()
    with redirect_stdout(typing):
        printf("hello world","style test", speed=7)
    assert expected_output[0] == typing.getvalue()

    left = StringIO()
    with redirect_stdout(left):
        printf("hello world","style test", style="left", speed=7)
    assert expected_output[1] == left.getvalue()

    mid = StringIO()
    with redirect_stdout(mid):
        printf("hello world","style test", style="mid", speed=7)
    assert expected_output[2] == mid.getvalue()

    fire = StringIO()
    with redirect_stdout(fire):
        printf("hello world","style test", style="fire", speed=7)
    assert expected_output[3] == fire.getvalue()

