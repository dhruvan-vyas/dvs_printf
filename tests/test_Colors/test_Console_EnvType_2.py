'Specif Test for console_EnvType: 2 terminal'

import pytest 
# from dvs_printf.errors.colors_errors import ColorsValueError
from dvs_printf.colors import Colors
from dvs_printf.colors.ansi import console_EnvType

# print("console_EnvType:", console_EnvType)

# Only Run Tests When (console_EnvType == 2)
if console_EnvType == 2:

    def test_colors_init_single_foreground():
        c = Colors("red")
        print(c.color , [c.color ])
        assert c.color == 9
        assert not c._gradient
        assert c.bg_color is None
        assert not c._bg_gradient

        c = Colors((0, 0, 255))
        print(c.color , [c.color ])
        assert c.color == (0, 0, 255)
        assert not c._gradient


    def test_colors_init_single_background():
        c = Colors(background="blue")
        print(c.bg_color, [c.bg_color])
        assert c.color is None
        assert c.bg_color == 12
        assert not c._bg_gradient

        c = Colors(background=(255, 255, 0))
        print(c.bg_color, [c.bg_color])
        assert c.bg_color == (255, 255, 0)


    # def test_colors_init_background_true():
    #     c = Colors(background=True)
    #     assert c.bg_color == (0, 0, 0) # Default black
    #     assert not c._bg_gradient



    def test_colors_init_combined_single_colors():
        c = Colors("red", background="blue")
        print(c.color)
        print(c.bg_color)
        assert c.color == 9
        assert c.bg_color == 12
        assert not c._gradient
        assert not c._bg_gradient




    def test_colors_init_angle():
        c = Colors("red", angle=90)
        assert c.angle == 90
        c = Colors("red", "blue", angle=45)
        assert c.angle == 45





    def test_apply_to_str_single_foreground():
        c = Colors("red")
        text = "TEST"
        # FIX: Expected output for per-character ANSI
        expected = f"\x1b[38;5;9m{text}\x1b[39m"
        assert c.apply_to_str(text) == expected

    # =========================================================================================================
    # ================================================ (Complited) ============================================
    # =========================================================================================================


    def test_apply_to_str_foreground_gradient(): 
        c = Colors("#FF0000", "#0000FF", angle=1) # Red to Blue
        text = "GRADIENT"
        result = c.apply_to_str(text)
        print(result)
        print([result])
        # FIX: Check start and end of gradient and overall structure
        assert result.startswith('\x1b[38;5;126mG\x1b[39')# Starts red
        assert result.endswith("T\x1b[39m") # Ends with T and reset
        # Further check: length of result should be original_len * (ansi_code_len + 1) + RESET_len
        # This is hard to assert exactly due to varying RGB values, but the start/end and reset are key.
        assert len(result) > len(text) # Should be longer due to ANSI codes

    def test_apply_to_str_single_background():
        c = Colors(background="green")
        text = "Only BG Test"
        # FIX: Expected output for per-character ANSI
        expected = '\x1b[48;5;2mOnly BG Test\x1b[49m' # Default FG is black
        assert c.apply_to_str(text) == expected

    def test_apply_to_str_foreground_gradient():
        c = Colors(background=["#FF0000", "#0000FF"], angle=45) # Red to Blue
        text = "GRADIENT"
        result = c.apply_to_str(text)
        print(result)
        print([result])
        # FIX: Check start and end of gradient and overall structure
        assert result.startswith("\x1b[48;5;196mG\x1b[49m") # Starts red
        assert result.endswith("T\x1b[49m") # Ends with T and reset
        # Further check: length of result should be original_len * (ansi_code_len + 1) + RESET_len
        # This is hard to assert exactly due to varying RGB values, but the start/end and reset are key.
        assert len(result) > len(text) # Should be longer due to ANSI codes

    def test_apply_to_str_combined_single_colors():
        c = Colors("white", background="black")
        text = "COMBINED"
        # FIX: Expected output for per-character ANSI
        expected = '\x1b[38;5;15m\x1b[48;5;0mCOMBINED\x1b[39m\x1b[49m'
        a = c.apply_to_str(text)
        print(a, [a])
        assert a == expected


    def test_apply_to_str_background_gradient(): 
        c = Colors(background=["pink", "yellow"], angle=45)
        text = "BGRADIENT"
        result = c.apply_to_str(text)
        print(result)
        print([result])
        # FIX: Check start and end of gradient and overall structure
        assert result.startswith("\x1b[48;5;224mB\x1b[49m") # Starts pink BG, default FG is black
        assert result.endswith("T\033[49m") # Ends with T and reset
        # assert len(result) > len(text) # Should be longer due to ANSI codes



    def test_apply_to_str_multi_line():
        c = Colors("cyan", background="purple")
        text = "Line1\nLine2"
        result = c.apply_to_str(text)
        print([result])
        print(result)
    #     # FIX: Expected output for per-character ANSI for each line
        expected_line = '\x1b[38;5;14m\x1b[48;5;5mLine1\x1b[39m\x1b[49m\n\x1b[38;5;14m\x1b[48;5;5mLine2\x1b[39m\x1b[49m'
        assert result == expected_line

    def test_apply_to_str_empty_string():
        c = Colors("red")
        assert c.apply_to_str("") == ""

    def test_apply_to_str_reset_false():
        c = Colors("red")
        text = "NO_RESET"
        # FIX: Expected output for per-character ANSI without final reset
        expected = '\x1b[38;5;9mNO_RESET'
        assert c.apply_to_str(text, reset=False) == expected

    # # # --- Test apply method (generator) ---

    def test_apply_single_foreground():
        c = Colors("red")
        lines = ["Line A", "Line B"]
        result_generator = c.apply(lines)

        # FIX: Expected output for per-character ANSI
        expected_line_a_list = ['\x1b[38;5;9mL', 'i', 'n', 'e', ' ', 'A\x1b[39m']
        expected_line_b_list = ['\x1b[38;5;9mL', 'i', 'n', 'e', ' ', 'B\x1b[39m']

        assert next(result_generator) == expected_line_a_list
        assert next(result_generator) == expected_line_b_list
        with pytest.raises(StopIteration):
            next(result_generator)


    def test_apply_foreground_gradient(): # ========================================(Need To Update)
        c = Colors("red", "blue", angle=45)
        lines = ["Short", "Longer line of text"]
        result_generator = c.apply(lines)

        short_line_result = next(result_generator)[0]
        short_line_result1 = next(result_generator)[0]
        # print(''.join(short_line_result))
        print([short_line_result])
        # print(''.join(short_line_result1))
        print([short_line_result1])

        # long_line_result = next(result_generator)[0]
        assert short_line_result  == '\x1b[38;5;161mS\x1b[39m'
        assert short_line_result1 == '\x1b[38;5;161mL\x1b[39m'

        with pytest.raises(StopIteration):
            next(result_generator)


    def test_apply_background_gradient(): # ========================================(Need To Update)
        c = Colors(background=["orange", "brown"])
        lines = ["Test", "More Text"]
        result_generator = c.apply(lines)

        test_line = next(result_generator)[0]
        assert test_line == '\x1b[48;5;214mT\x1b[49m'
        more_text_line = next(result_generator)[0]
        assert more_text_line == '\x1b[48;5;214mM\x1b[49m'

        with pytest.raises(StopIteration):
            next(result_generator)



    def test_apply_empty_list():
        c = Colors("red")
        result_generator = c.apply([])
        assert list(result_generator) == []

    def test_apply_list_with_empty_strings():
        c = Colors("green")
        lines = ["", "Hello", ""]
        result_generator = c.apply(lines)
        # FIX: Empty string should yield an empty string, not a colored string
        assert next(result_generator) == ['']
        assert next(result_generator) == ['\x1b[38;5;2mH','e','l','l','o\033[39m']
        assert next(result_generator) == ['']
        with pytest.raises(StopIteration):
            next(result_generator)

    def test_apply_invalid_input_type():
        c = Colors("red")
        with pytest.raises(TypeError, match="Values must be a list, tuple, or generator of strings."):
            list(c.apply("not a list"))
        with pytest.raises(TypeError, match="Values must be a list, tuple, or generator of strings."):
            list(c.apply(123))

    # # # --- Test __str__ and __repr__ ---

    def test_str_and_repr():
        c_single = Colors("red", background="blue")
        # assert "Colors(foreground=9, background=12, angle=None)" in str(c_single)
        assert '\x1b[38;5;9m\x1b[48;5;12m' in str(c_single)
        assert "Colors(foreground=9, background=12, angle=None)" in repr(c_single)

        c_gradient = Colors(["red", "green"], background=["blue", "cyan"], angle=45)
        # assert "Colors(foreground=[(255, 0, 0), (0, 128, 0)], background=[(0, 0, 255), (0, 255, 255)], angle=45)" in str(c_gradient)
        assert '\x1b[38;5;196m\x1b[48;5;21m' in str(c_gradient)
        assert "Colors(foreground=[(255, 0, 0), (0, 128, 0)], background=[(0, 0, 255), (0, 255, 255)], angle=45)" in repr(c_gradient)






