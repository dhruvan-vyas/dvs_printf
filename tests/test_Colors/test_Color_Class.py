from dvs_printf.colors import Colors, console_EnvType

if console_EnvType == 1: # ENV 1
   value_1 = '\x1b[38;2;255;0;0mHii\x1b[39m'
   value_2 = [['\x1b[38;2;255;0;0mH', 'i', 'i\x1b[39m']]
   value_3 = '\x1b[38;2;255;0;0mHii'
   value_4 = [['\x1b[38;2;255;0;0mH', 'i', 'i']]

elif console_EnvType == 2: # ENV 2
    value_1 = '\x1b[38;5;9mHii\x1b[39m'
    value_2 = [['\x1b[38;5;9mH', 'i', 'i\x1b[39m']]
    value_3 = '\x1b[38;5;9mHii'
    value_4 = [['\x1b[38;5;9mH', 'i', 'i']]

elif console_EnvType == 3: # ENV 3
    value_1 = '\x1b[31mHii\x1b[39m'
    value_2 = [['\x1b[31mH', 'i', 'i\x1b[39m']]
    value_3 = '\x1b[31mHii'
    value_4 = [['\x1b[31mH', 'i', 'i']]

else: # console_EnvType >= 4: ENV 4
    value_1 = 'Hii\x1b[39m'
    value_2 = [['H', 'i', 'i']]
    value_3 = 'Hii'
    value_4 = [['H', 'i', 'i']]

def test_apple_single_color():
    assert  Colors("red").apply_to_str(
                                "Hii",
                                reset=True
            ) == value_1
    
    assert  list(
                Colors("red").apply(
                                ["Hii"],
                                reset=True
                )
            )  == value_2
    
def test_reset_color():
    assert  Colors("red").apply_to_str(
                                "Hii",
                                reset=False
            ) == value_3
    
    assert  list(
                Colors("red").apply(
                                ["Hii"],
                                reset=False
                )
            )  == value_4
    
