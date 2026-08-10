'Specif Test for console_EnvType: 1 terminal'

import pytest 
from dvs_printf.colors.ansi import console_EnvType
from dvs_printf.colors.colors import Colors, get_RGB_values, ColorsValueError as CE2
from dvs_printf.exceptions.colors_exception import ColorsValueError

# print("console_EnvType:", console_EnvType)

# Only Run Tests When (console_EnvType == 1)
if console_EnvType == 1:
    def test_get_RGB_values_valid():
        assert get_RGB_values((255, 0, 0)) == (255, 0, 0)
        assert get_RGB_values("#FF0000") == (255, 0, 0)
        assert get_RGB_values("#F00") == (255, 0, 0)
        assert get_RGB_values("red") == (255, 0, 0)
        assert get_RGB_values("rgb: 255, 0, 0") == (255, 0, 0)
        assert get_RGB_values("hsl: 0, 1, 0.5") == (255, 0, 0)
        assert get_RGB_values("hsl: 1/3, 1, 0.5") == (0, 255, 0) # Green
        assert get_RGB_values("hsl: 2/3, 1, 0.5") == (0, 0, 255) # Blue
        assert get_RGB_values("hsl: 120, 1, 0.5") == (0, 255, 0) # Green
        assert get_RGB_values("hsv: 0, 1, 1") == (255, 0, 0)
        assert get_RGB_values("hsv: 1/3, 1, 1") == (0, 255, 0) # Green
        assert get_RGB_values("cmyk: 0, 1, 1, 0") == (255, 0, 0)

    def test_get_RGB_values_invalid():
        with pytest.raises((ColorsValueError,CE2), match="RGB tuple values must be integers between 0 and 255"):
            get_RGB_values((256, 0, 0))
        with pytest.raises((ColorsValueError,CE2), match="Invalid hex color format"):
            get_RGB_values("#GGHHII")
        with pytest.raises((ColorsValueError,CE2)):
            get_RGB_values("not_a_color")
        with pytest.raises((ColorsValueError,CE2), match="Invalid input: Expected a tuple, list, or string"):
            get_RGB_values(12345) # This should now pass
# "ColorsValueError: The Color_name: 'not_a_color' is not specified in colors dict"
# "ColorsValueError: The Color_name: 'not_a_color' is not specified in colors dict"
    # --- Test Colors Class Initialization ---

    def test_colors_init_single_foreground():
        c = Colors("red")
        assert c.color == (255, 0, 0)
        assert not c._gradient
        assert c.bg_color is None
        assert not c._bg_gradient

        c = Colors((0, 0, 255))
        assert c.color == (0, 0, 255)
        assert not c._gradient

    def test_colors_init_foreground_gradient_positional():
        c = Colors("red", "blue")
        assert c._colors == [(255, 0, 0), (0, 0, 255)]
        assert c._gradient
        assert c.bg_color is None

    def test_colors_init_foreground_gradient_list():
        c = Colors(["green", "yellow", "red"])
        assert c._colors == [(0, 128, 0), (255, 255, 0), (255, 0, 0)]
        assert c._gradient
        assert c.bg_color is None

    def test_colors_init_single_background():
        c = Colors(background="blue")
        assert c.color is None
        assert c.bg_color == (0, 0, 255)
        assert not c._bg_gradient

        c = Colors(background=(255, 255, 0))
        assert c.bg_color == (255, 255, 0)


    def test_colors_init_background_gradient():
        c = Colors(background=["pink", "yellow", "green"])
        assert c.color is None
        assert c.bg_color is None # single bg_color should be None if gradient
        assert c._bg_colors == [(255, 192, 203), (255, 255, 0), (0, 128, 0)]
        assert c._bg_gradient

    def test_colors_init_combined_single_colors():
        c = Colors("red", background="blue")
        assert c.color == (255, 0, 0)
        assert c.bg_color == (0, 0, 255)
        assert not c._gradient
        assert not c._bg_gradient

    def test_colors_init_combined_fg_gradient_bg_single():
        c = Colors("red", "green", background="blue")
        assert c._colors == [(255, 0, 0), (0, 128, 0)]
        assert c._gradient
        assert c.bg_color == (0, 0, 255)
        assert not c._bg_gradient

    def test_colors_init_combined_fg_single_bg_gradient():
        c = Colors("red", background=["blue", "cyan"])
        assert c.color == (255, 0, 0)
        assert not c._gradient
        assert c.bg_color is None
        assert c._bg_colors == [(0, 0, 255), (0, 255, 255)]
        assert c._bg_gradient

    def test_colors_init_combined_gradients():
        c = Colors(["red", "green"], background=["blue", "cyan"])
        assert c._colors == [(255, 0, 0), (0, 128, 0)]
        assert c._gradient
        assert c._bg_colors == [(0, 0, 255), (0, 255, 255)]
        assert c._bg_gradient

    def test_colors_init_angle():
        c = Colors("red", angle=90)
        assert c.angle == 90
        c = Colors("red", "blue", angle=45)
        assert c.angle == 45


    #===========================(Went wrong)====================================================
    def test_colors_init_invalid_ColorInput():
        with pytest.raises(CE2):
            Colors((120,130))
        with pytest.raises(CE2):
            Colors(background="invalid_bg_color")
        with pytest.raises(CE2):
            Colors(["red", "invalid_gradient_color"])
        with pytest.raises(CE2):
            Colors(background=["blue", "invalid_bg_gradient_color"])
    #==========================================================================================


    # --- Test apply_to_str method ---

    def test_apply_to_str_single_foreground():
        c = Colors("red")
        text = "TEST"
        # FIX: Expected output for per-character ANSI
        expected = f"\033[38;2;255;0;0m{text}\x1b[39m"
        assert c.apply_to_str(text) == expected

    def test_apply_to_str_foreground_gradient(): 
        c = Colors("#FF0000", "#0000FF", angle=1) # Red to Blue
        text = "GRADIENT"
        result = c.apply_to_str(text)
        print(result)
        print([result])
        # FIX: Check start and end of gradient and overall structure
        assert result.startswith(f"\x1b[38;2;255;0;0mG\x1b[39m")# Starts red
        assert result.endswith("T\x1b[39m") # Ends with T and reset
        # Further check: length of result should be original_len * (ansi_code_len + 1) + RESET_len
        # This is hard to assert exactly due to varying RGB values, but the start/end and reset are key.
        assert len(result) > len(text) # Should be longer due to ANSI codes

    def test_apply_to_str_single_background():
        c = Colors(background="green")
        text = "Only BG Test"
        # FIX: Expected output for per-character ANSI
        expected = '\x1b[48;2;0;128;0mOnly BG Test\x1b[49m' # Default FG is black
        assert c.apply_to_str(text) == expected

    def test_apply_to_str_foreground_gradient():
        c = Colors(background=["#FF0000", "#0000FF"], angle=45) # Red to Blue
        text = "GRADIENT"
        result = c.apply_to_str(text)
        print(result)
        print([result])
        # FIX: Check start and end of gradient and overall structure
        assert result.startswith(f"\x1b[48;2;255;0;0mG\x1b[49m") # Starts red
        assert result.endswith("T\x1b[49m") # Ends with T and reset
        # Further check: length of result should be original_len * (ansi_code_len + 1) + RESET_len
        # This is hard to assert exactly due to varying RGB values, but the start/end and reset are key.
        assert len(result) > len(text) # Should be longer due to ANSI codes

    def test_apply_to_str_combined_single_colors():
        c = Colors("white", background="black")
        text = "COMBINED"
        # FIX: Expected output for per-character ANSI
        expected = '\x1b[38;2;255;255;255m\x1b[48;2;0;0;0mCOMBINED\x1b[39m\x1b[49m'
        assert c.apply_to_str(text) == expected


    def test_apply_to_str_background_gradient(): 
        c = Colors(background=["pink", "yellow"], angle=45)
        text = "BGRADIENT"
        result = c.apply_to_str(text)
        print(result)
        print([result])
        # FIX: Check start and end of gradient and overall structure
        assert result.startswith(f"\x1b[48;2;255;192;203mB\x1b[49m") # Starts pink BG, default FG is black
        assert result.endswith("T\033[49m") # Ends with T and reset
        # assert len(result) > len(text) # Should be longer due to ANSI codes



    def test_apply_to_str_multi_line():
        c = Colors("cyan", background="purple")
        text = "Line1\nLine2"
        result = c.apply_to_str(text)
        print([result])
        print(result)
    #     # FIX: Expected output for per-character ANSI for each line
        expected_line = '\x1b[38;2;0;255;255m\x1b[48;2;128;0;128mLine1\x1b[39m\x1b[49m\n\x1b[38;2;0;255;255m\x1b[48;2;128;0;128mLine2\x1b[39m\x1b[49m'
        assert result == expected_line

    def test_apply_to_str_empty_string():
        c = Colors("red")
        assert c.apply_to_str("") == ""

    def test_apply_to_str_reset_false():
        c = Colors("red")
        text = "NO_RESET"
        # FIX: Expected output for per-character ANSI without final reset
        expected = f"\033[38;2;255;0;0m{text}"
        assert c.apply_to_str(text, reset=False) == expected

    # # --- Test apply method (generator) ---

    def test_apply_single_foreground():
        c = Colors("red")
        lines = ["Line A", "Line B"]
        result_generator = c.apply(lines)

        # FIX: Expected output for per-character ANSI
        expected_line_a_list = ['\x1b[38;2;255;0;0mL', 'i', 'n', 'e', ' ', 'A\x1b[39m']
        expected_line_b_list = ['\x1b[38;2;255;0;0mL', 'i', 'n', 'e', ' ', 'B\x1b[39m']

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
        assert short_line_result == '\x1b[38;2;228;0;26mS\x1b[39m'
        assert short_line_result1 == '\x1b[38;2;221;0;33mL\x1b[39m'

        with pytest.raises(StopIteration):
            next(result_generator)


    def test_apply_background_gradient(): # ========================================(Need To Update)
        c = Colors(background=["orange", "brown"])
        lines = ["Test", "More Text"]
        result_generator = c.apply(lines)

        test_line = next(result_generator)[0]
        assert test_line == '\x1b[48;2;250;158;2mT\x1b[49m'
        more_text_line = next(result_generator)[0]
        assert more_text_line == '\x1b[48;2;245;151;4mM\x1b[49m'

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
        assert next(result_generator) == ['\x1b[38;2;0;128;0mH','e','l','l','o\033[39m']
        assert next(result_generator) == ['']
        with pytest.raises(StopIteration):
            next(result_generator)

    def test_apply_invalid_input_type():
        c = Colors("red")
        with pytest.raises(TypeError, match="Values must be a list, tuple, or generator of strings."):
            list(c.apply("not a list"))
        with pytest.raises(TypeError, match="Values must be a list, tuple, or generator of strings."):
            list(c.apply(123))

    # # --- Test __str__ and __repr__ ---

    def test_str_and_repr():
        c_single = Colors("red", background="blue")
        # assert "Colors(foreground=(255, 0, 0), background=(0, 0, 255), angle=None)" in str(c_single)
        assert '\x1b[38;2;255;0;0m\x1b[48;2;0;0;255m' in str(c_single)
        assert "Colors(foreground=(255, 0, 0), background=(0, 0, 255), angle=None)" in repr(c_single)

        c_gradient = Colors(["red", "green"], background=["blue", "cyan"], angle=45)
        # assert "Colors(foreground=[(255, 0, 0), (0, 128, 0)], background=[(0, 0, 255), (0, 255, 255)], angle=45)" in str(c_gradient)
        assert '\x1b[38;2;255;0;0m\x1b[48;2;0;0;255m' in str(c_gradient)
        assert "Colors(foreground=[(255, 0, 0), (0, 128, 0)], background=[(0, 0, 255), (0, 255, 255)], angle=45)" in repr(c_gradient)






# c = Colors(background=["#FF0000", "#0000FF"], angle=45) # Red to Blue
# text = "GRADIENT"
# result = c.apply_to_str(text)
# print(result)
# print([result])
# # FIX: Check start and end of gradient and overall structure
# # assert 
# print(result.startswith(f"\x1b[48;2;255;0;0mG\x1b[49m"))


#  c = Colors(background=["pink", "yellow"], angle=45)
#         text = "BGRADIENT"
#         result = c.apply_to_str(text)
#         print(result)
#         print([result])
#         # FIX: Check start and end of gradient and overall structure
#         assert result.startswith(f"\x1b[48;2;255;192;203mB\x1b[49m") #


# c = Colors("red", "blue", angle=45)
#         lines = ["Short", "Longer line of text"]
#         result_generator = c.apply(lines)

#         short_line_result = next(result_generator)[0]
#         short_line_result1 = next(result_generator)[0]
#         # print(''.join(short_line_result))
#         print([short_line_result])
#         # print(''.join(short_line_result1))
#         print([short_line_result1])

#         # long_line_result = next(result_generator)[0]
#         assert short_line_result == '\x1b[38;2;228;0;26mS\x1b[39m'
#         assert short_line_result1 == '\x1b[38;2;221;0;33mL\x1b[39m'

#         with pytest.raises(StopIteration):
#             next(result_generator)




    # c = Colors(background=["orange", "brown"])
    #     lines = ["Test", "More Text"]
    #     result_generator = c.apply(lines)

    #     test_line = next(result_generator)[0]
    #     assert test_line == '\x1b[48;2;250;158;2mT\x1b[49m'
    #     more_text_line = next(result_generator)[0]
    #     assert more_text_line == '\x1b[48;2;245;151;4mM\x1b[49m'

    #     with pytest.raises(StopIteration):
    #         next(result_generator)
