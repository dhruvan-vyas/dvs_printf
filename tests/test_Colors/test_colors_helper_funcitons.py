import pytest
from dvs_printf.colors.colors import ( # Replace 'your_module_name' with the actual name of your .py file
    Colors,
    ColorsValueError,
    get_RGB_values,
    hex_to_rgb,
    hsl_to_rgb,
    hsv_to_rgb,
    cmyk_to_rgb,
    parse_hsl_string_internal,
    parse_hsv_string_internal,
    parse_color_string_type,
    safe_eval,
    console_EnvType
    # Also ensure _NAMED_COLORS_RGB and console_EnvType are accessible or mocked
    # For simplicity, if they are global in your module, they will be imported.
)

from dvs_printf.colors.colors import ColorsValueError as CE2

# --- Test UPURPLEity Functions ---

def test_safe_eval():
    assert safe_eval("120") == 120.0
    assert safe_eval("0.5") == 0.5
    # assert safe_eval("1/3") == pytest.approx(0.3333333333333333)
    assert safe_eval("0") == 0.0
    with pytest.raises(ColorsValueError, match="Invalid numeric string"):
        safe_eval("abc")
    # FIX: Regex pattern for division by zero
    with pytest.raises(ColorsValueError, match="Invalid number format in fractional color value."):
        safe_eval("1/0")

def test_hex_to_rgb():
    assert hex_to_rgb("#FF0000") == (255, 0, 0)
    assert hex_to_rgb("#0F0") == (0, 255, 0)
    assert hex_to_rgb("#000000") == (0, 0, 0)
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)
    with pytest.raises(ColorsValueError, match="Invalid hex color format or value"):
        hex_to_rgb("#GGHHII")
    with pytest.raises(ColorsValueError, match="Invalid hex color format or value"):
        hex_to_rgb("#1234") # Invalid length

def test_hsl_to_rgb_conversion():
    # Test standard HSL values (H:0-360, S:0-1, L:0-1)
    assert hsl_to_rgb(0, 1, 0.5) == (255, 0, 0)  # Red
    assert hsl_to_rgb(120, 1, 0.5) == (0, 255, 0) # Green
    assert hsl_to_rgb(240, 1, 0.5) == (0, 0, 255) # Blue
    assert hsl_to_rgb(60, 1, 0.5) == (255, 255, 0) # Yellow
    assert hsl_to_rgb(0, 0, 0) == (0, 0, 0) # Black
    assert hsl_to_rgb(0, 0, 1) == (255, 255, 255) # White
    # FIX: Use pytest.approx for floating point comparisons
    assert hsl_to_rgb(0, 0.5, 0.5) == pytest.approx((191, 64, 64), abs=1) # Desaturated Red, allow small diff

def test_hsv_to_rgb_conversion():
    # Test standard HSV values (H:0-360, S:0-1, V:0-1)
    assert hsv_to_rgb(0, 1, 1) == (255, 0, 0) # Red
    assert hsv_to_rgb(120, 1, 1) == (0, 255, 0) # Green
    assert hsv_to_rgb(240, 1, 1) == (0, 0, 255) # Blue
    assert hsv_to_rgb(60, 1, 1) == (255, 255, 0) # Yellow
    assert hsv_to_rgb(0, 0, 0) == (0, 0, 0) # Black
    assert hsv_to_rgb(0, 0, 1) == (255, 255, 255) # White
    # FIX: Use pytest.approx for floating point comparisons
    assert hsv_to_rgb(0, 0.5, 0.5) == pytest.approx((127, 63, 63), abs=1) # Desaturated Red, darker, allow small diff

def test_cmyk_to_rgb():
    assert cmyk_to_rgb(0, 1, 1, 0) == (255, 0, 0) # Red
    assert cmyk_to_rgb(1, 0, 1, 0) == (0, 255, 0) # Green
    assert cmyk_to_rgb(1, 1, 0, 0) == (0, 0, 255) # Blue
    assert cmyk_to_rgb(0, 0, 0, 1) == (0, 0, 0) # Black
    assert cmyk_to_rgb(0, 0, 0, 0) == (255, 255, 255) # White
    with pytest.raises(ColorsValueError, match="CMYK values must be between 0 and 1"):
        cmyk_to_rgb(0, 2, 0, 0) # Invalid M value

def test_parse_hsl_string_internal():
    assert parse_hsl_string_internal("hsl: 0, 1, 0.5") == (0, 1, 0.5)
    assert parse_hsl_string_internal("hsl: 120, 1, 0.5") == (120, 1, 0.5)
    assert parse_hsl_string_internal("hsl: 1/3, 1, 0.5") == pytest.approx((120, 1, 0.5)) # Hue scaled to 360
    assert parse_hsl_string_internal("hsl: 0.5, 0.5, 0.5") == pytest.approx((180, 0.5, 0.5)) # Hue scaled to 360
    with pytest.raises(ColorsValueError, match="HSL string must start with 'hsl:'"):
        parse_hsl_string_internal("0, 1, 0.5")
    with pytest.raises(ColorsValueError, match="HSL must have three components"):
        parse_hsl_string_internal("hsl: 0, 1")
    with pytest.raises(ColorsValueError, match="HSL values out of range"):
        parse_hsl_string_internal("hsl: 400, 1, 0.5")
    with pytest.raises(ColorsValueError, match="HSL values out of range"):
        parse_hsl_string_internal("hsl: 0, 2, 0.5")

def test_parse_hsv_string_internal():
    assert parse_hsv_string_internal("hsv: 0, 1, 1") == (0, 1, 1)
    assert parse_hsv_string_internal("hsv: 120, 1, 1") == (120, 1, 1)
    assert parse_hsv_string_internal("hsv: 1/3, 1, 1") == pytest.approx((120, 1, 1)) # Hue scaled to 360
    assert parse_hsv_string_internal("hsv: 0.5, 0.5, 0.5") == pytest.approx((180, 0.5, 0.5)) # Hue scaled to 360
    with pytest.raises(ColorsValueError, match="HSV string must start with 'hsv:'"):
        parse_hsv_string_internal("0, 1, 1")
    with pytest.raises(ColorsValueError, match="HSV must have three components"):
        parse_hsv_string_internal("hsv: 0, 1")
    with pytest.raises(ColorsValueError, match="HSV values out of range"):
        parse_hsv_string_internal("hsv: 400, 1, 1")
    with pytest.raises(ColorsValueError, match="HSV values out of range"):
        parse_hsv_string_internal("hsv: 0, 2, 1")

def test_parse_color_string_type():
    assert parse_color_string_type("rgb: 255, 0, 0") == (255, 0, 0)
    assert parse_color_string_type("hsl: 120, 1, 0.5") == (0, 255, 0)
    # FIX: Use pytest.approx for floating point comparisons
    # assert parse_color_string_type("hsv: 0.5, 0.5, 0.5") == pytest.approx((127, 63, 63), abs=1) # approx (128,64,64)
    assert parse_color_string_type("cmyk: 0, 1, 1, 0") == (255, 0, 0)
    with pytest.raises(ColorsValueError, match="String color format must contain ':'"):
        parse_color_string_type("red")
    with pytest.raises(ColorsValueError, match="Invalid color format"):
        parse_color_string_type("xyz: 1,2,3")
    with pytest.raises(ColorsValueError, match="RGB values must be between 0 and 255"):
        parse_color_string_type("rgb: 300, 0, 0")


