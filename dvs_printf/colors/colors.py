""" dvs_printf.colors (Core Module)
This module contains the primary class (:class:Colors) for configuring color schemes
and handling the complex logic for applying True Color (RGB) ANSI escape codes,
including single colors and angular gradients, to text output.

It integrates seamlessly with the helper functions defined in this package to handle
all supported input formats (Named Colors, Hex, RGB Tuples, HSL/HSV strings).

Primary Components

:class:Colors:
The configuration class. Instances of this class hold a complete color scheme (e.g.,
a red-to-blue foreground gradient with a static black background). Its methods,
like .apply_to_str(), perform the character-by-character formatting.

:class:Color:
A static factory class providing easy access to named color constants (e.g.,
Color.RED) as pre-calculated RGB tuples, used for configuring :class:Colors.

Exposed Constants

These ANSI codes are defined and exposed for external use when manual resetting is necessary.

:const:RESET: Universal reset code (resets FG, BG, and attributes).
:const:RESET_FG: Resets only the foreground color.
:const:RESET_BG: Resets only the background color.

"""

from typing import (
    Any,
    Sequence,
    Tuple,
    List,
    Union,
    Generator,
    TypeAlias,
    overload
)

from ..exceptions       import ColorsValueError, _Warning
from .gredinat_styles   import GradientStyles
from .gradient          import apply_gradient
from .colors_dictionary import name_to_rgb, name_to_16, name_to_256
from .ansi              import (
    RESET, 
    RESET_FOREGROUND as RESET_FG, 
    RESET_BACKGROUND as RESET_BG,
    rgb_to_ansi_func    ,
    rgb_to_bg_ansi_func ,
    console_EnvType     ,
    values_to_ansi_fg   ,
    values_to_ansi_bg   ,
)

# --- Type Aliases ---
Color_Name: TypeAlias = str
ColorTuple     = Tuple[int, int, int]
ColorInput     = Union[ColorTuple , Color_Name]
rgb_Color      = Union[ColorTuple , Color_Name]
StrArray       = List [Color_Name ]
ColorSequence  = Tuple[ColorInput | Color_Name, ...]
GradientOutput = Generator[List[str]  , None, None]
GredinatInput  = Sequence[ColorInput]
ColorArg = Union[ColorInput, GredinatInput, GradientStyles]

# --- UPURPLEity functions for color conversions ---
def hex_to_rgb(hex_color: str) -> ColorTuple:
    """
    Converts a HEX color string (e.g., '#FF00AA', '#F0A') into an RGB tuple (0-255).

    Args:
        hex_color (str): The hexadecimal color string, optionally starting with '#'.

    Returns:
        ColorTuple (Tuple[int, int, int]): The corresponding RGB tuple.

    Raises:
        ColorsValueError: If the hex string has an invalid format, length, or content.
    """
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) >= 6:
            # RRGGBB format
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3:
            # RGB short format (e.g., #F0A -> #FF00AA)
            return tuple(int(c*2, 16) for c in hex_color)
        else:
            raise ValueError("Invalid hex color length.")
    except ValueError:
        raise ColorsValueError(error_value=f"#{hex_color}", message=f"Invalid hex color format or value. Got: #{hex_color}")

def safe_eval(val: str) -> float:
    """
    Safely evaluates numeric strings, including simple fractions, to a float.

    This function is used internally to parse components of color strings (e.g., 
    in 'hsl: 1/3, 0.5, 1').

    Args:
        val (str): The string to evaluate (e.g., '1/3', '0.5', '120').

    Returns:
        float: The resulting numeric value.

    Raises:
        ColorsValueError: If the string is not a valid number or results in 
                          a division by zero.
    """
    val = val.strip()
    if '/' in val:
        num_str, den_str = val.split('/')
        try:
            num = float(num_str)
            den = float(den_str)
            if den == 0:
                raise ColorsValueError(val, "Division by zero in fractional color value.")
            return num / den
        except: raise ColorsValueError(val, "Invalid number format in fractional color value.")
    try: 
        return float(val)
    except: raise ColorsValueError(val, "Invalid numeric string for color component.")

def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    """
    Converts HSL color components to RGB components using manual math (no colorsys).

    Args:
        h (float): Hue component (0-360).
        s (float): Saturation component (0-1).
        l (float): Lightness component (0-1).

    Returns:
        Tuple[int, int, int]: The resulting RGB tuple (0-255).
    """
    h_norm = h % 360
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h_norm / 60) % 2 - 1))
    m = l - c / 2

    r_prime, g_prime, b_prime = 0.0, 0.0, 0.0

    if     0 <= h_norm <  60: r_prime, g_prime, b_prime = c, x, 0
    elif  60 <= h_norm < 120: r_prime, g_prime, b_prime = x, c, 0
    elif 120 <= h_norm < 180: r_prime, g_prime, b_prime = 0, c, x
    elif 180 <= h_norm < 240: r_prime, g_prime, b_prime = 0, x, c
    elif 240 <= h_norm < 300: r_prime, g_prime, b_prime = x, 0, c
    elif 300 <= h_norm < 360: r_prime, g_prime, b_prime = c, 0, x

    r = int((r_prime + m) * 255)
    g = int((g_prime + m) * 255)
    b = int((b_prime + m) * 255)

    return r, g, b

def hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    """
    Converts HSV color components to RGB components using manual math (no colorsys).

    Args:
        h (float): Hue component (0-360).
        s (float): Saturation component (0-1).
        v (float): Value component (0-1).

    Returns:
        Tuple[int, int, int]: The resulting RGB tuple (0-255).
    """
    h_norm = h % 360
    c = v * s
    x = c * (1 - abs((h_norm / 60) % 2 - 1))
    m = v - c

    r_prime, g_prime, b_prime = 0.0, 0.0, 0.0

    if     0 <= h_norm <  60: r_prime, g_prime, b_prime = c, x, 0
    elif  60 <= h_norm < 120: r_prime, g_prime, b_prime = x, c, 0
    elif 120 <= h_norm < 180: r_prime, g_prime, b_prime = 0, c, x
    elif 180 <= h_norm < 240: r_prime, g_prime, b_prime = 0, x, c
    elif 240 <= h_norm < 300: r_prime, g_prime, b_prime = x, 0, c
    elif 300 <= h_norm < 360: r_prime, g_prime, b_prime = c, 0, x
    
    r = int((r_prime + m) * 255)
    g = int((g_prime + m) * 255)
    b = int((b_prime + m) * 255)

    return r, g, b


def parse_hsl_string_internal(hsl_str: str) -> tuple[float, float, float]:
    """
    Parses the internal 'hsl: H, S, L' string format into floating-point components.
    
    This function includes a heuristic to scale normalized Hue (H: 0-1) to degrees (0-360) 
    if a decimal or fraction is detected.

    Args:
        hsl_str (str): String starting with 'hsl:', followed by three comma-separated values.

    Returns:
        Tuple[float, float, float]: The normalized HSL components (H:0-360, S/L:0-1).

    Raises:
        ColorsValueError: If the format is incorrect or values are out of range.
    """
    if not hsl_str.lower().startswith("hsl:"):
        raise ColorsValueError(hsl_str, "HSL string must start with 'hsl:'")
    
    parts = hsl_str[len("hsl:"):].split(',')
    if len(parts) != 3:
        raise ColorsValueError(hsl_str, "HSL must have three components: H, S, L")
    
    h, s, l = safe_eval(parts[0]), safe_eval(parts[1]), safe_eval(parts[2])
    
    # Normalize H to 0-360 range if it appears to be a 0-1 normalized value
    if (0 < h <= 1.0) and ('.' in parts[0] or '/' in parts[0]):
        h *= 360.0 

    # Validate ranges (after potential scaling for H)
    if not ((0 <= h <= 360) and (0 <= s <= 1) and (0 <= l <= 1)):
        raise ColorsValueError(hsl_str, "HSL values out of range (H:0-360, S/L:0-1).")
    
    return h, s, l

def parse_hsv_string_internal(hsv_str: str) -> tuple[float, float, float]:
    """
    Parses the internal 'hsv: H, S, V' string format into floating-point components.

    This function includes a heuristic to scale normalized Hue (H: 0-1) to degrees (0-360) 
    if a decimal or fraction is detected.

    Args:
        hsv_str (str): String starting with 'hsv:', followed by three comma-separated values.

    Returns:
        Tuple[float, float, float]: The normalized HSV components (H:0-360, S/V:0-1).

    Raises:
        ColorsValueError: If the format is incorrect or values are out of range.
    """
    if not hsv_str.lower().startswith("hsv:"):
        raise ColorsValueError(hsv_str, "HSV string must start with 'hsv:'")
    
    parts = hsv_str[len("hsv:"):].split(',')
    if len(parts) != 3:
        raise ColorsValueError(hsv_str, "HSV must have three components: H, S, V")
    
    h, s, v = safe_eval(parts[0]), safe_eval(parts[1]), safe_eval(parts[2])

    # Normalize H to 0-360 range if it appears to be a 0-1 normalized value
    if (0 < h <= 1.0) and ('.' in parts[0] or '/' in parts[0]):
        h *= 360.0 

    # Validate ranges (after potential scaling for H)
    if not ((0 <= h <= 360) and (0 <= s <= 1) and (0 <= v <= 1)):
        raise ColorsValueError(hsv_str, "HSV values out of range (H:0-360, S/V:0-1).")
    
    return h, s, v

def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> ColorTuple:
    """
    Converts CMYK color components (0-1) to RGB components (0-255).

    Args:
        c (float): Cyan component (0-1).
        m (float): Magenta component (0-1).
        y (float): Yellow component (0-1).
        k (float): Key/Black component (0-1).

    Returns:
        ColorTuple (Tuple[int, int, int]): The resulting RGB tuple (0-255).

    Raises:
        ColorsValueError: If any CMYK value is outside the 0-1 range.
    """
    if not all(0 <= val <= 1 for val in (c, m, y, k)):
        raise ColorsValueError(f"c:{c},m:{m},y:{y},k:{k}", "CMYK values must be between 0 and 1.")
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)


def parse_color_string_type(color_str: str) -> Tuple[int, int, int]:
    """
    Identifies the color space (RGB, HSL, HSV, CMYK) from a string and delegates 
    to the appropriate conversion function.

    Expected format: "TYPE: val1, val2, ..."

    Args:
        color_str (str): The color string (e.g., 'rgb: 255, 0, 0').

    Returns:
        ColorTuple (Tuple[int, int, int]): The final RGB tuple (0-255).

    Raises:
        ColorsValueError: If the format is invalid, the type is unknown, or component
                          ranges are incorrect.
    """
    if ":" not in color_str:
        raise ColorsValueError(color_str, "String color format must contain ':' (e.g., 'rgb:').")
    
    parts = color_str.split(":", 1)
    if len(parts) < 2:
        raise ColorsValueError(color_str, "String color format is missing values after ':'.")
        
    color_type = parts[0].strip().lower()
    values_str = parts[1]

    num_parts = [p.strip() for p in values_str.split(',')]
    if not num_parts or any(not p for p in num_parts):
        raise ColorsValueError(color_str, "No numeric values found in color string or invalid comma separation.")

    values = [safe_eval(s) for s in num_parts]

    if color_type == "rgb" and len(values) == 3:
        if not all(0 <= v <= 255 for v in values):
            raise ColorsValueError(color_str, "RGB values must be between 0 and 255.")
        return tuple(map(int, values))
    elif color_type == "hsl" and len(values) == 3:
        # Pass original string for internal HSL parser
        h, s, l = parse_hsl_string_internal(color_str) 
        return hsl_to_rgb(h, s, l) 
    elif color_type == "hsv" and len(values) == 3:
        # Pass original string for internal HSV parser
        h, s, v = parse_hsv_string_internal(color_str) 
        return hsv_to_rgb(h, s, v) 
    elif color_type == "cmyk" and len(values) == 4:
        return cmyk_to_rgb(*values)
    else: 
        raise ColorsValueError(color_str, "Invalid color format (rgb, hsl, hsv, cmyk) or incorrect number of components.")
 
def get_RGB_values(color: ColorInput, only_RGB: bool = True) -> ColorTuple:
    """
    The main color parsing entry point. Converts any valid color input format 
    (Tuple, List, Str, Hex, Named Color) into an RGB tuple.

    Args:
        color (ColorInput): The color value to process.
        only_RGB (bool, optional): If True (default), ensures the return value is 
            always a standard RGB tuple (0-255).

    Returns:
        ColorTuple: The final RGB tuple (0-255). Returns None if the input is an 
            empty string, signifying no color.

    Raises:
        ColorsValueError: For any invalid format, type, or range error.
    """
    
    if isinstance(color, str) and not color.strip():
        return None # Return None to signify no color
    
    if isinstance(color, (tuple, list)):
        if len(color) == 3:
            if all(isinstance(c, int) for c in color): 
                if all(0 <= c <= 255 for c in color):
                    return tuple(color)
                else:
                    raise ColorsValueError(error_value=color, message="RGB tuple values must be integers between 0 and 255.")
            else: raise ColorsValueError(error_value=color, message=f"Invalid tuple elements: {color}. Expected (int, int, int) for RGB.")
        else: raise ColorsValueError(error_value=color, message="Tuple/list color must have 3 components for RGB.")

    elif isinstance(color, str):
        try:
            color = color.strip()
            if color.startswith("#"): 
                return hex_to_rgb(color)
            elif ":" in color: 
                return parse_color_string_type(color) # Use the specific string parser

            color = color.replace(" ", "").lower() # Normalize for named colors
            
            # Delegates to named color lookup based on environment color depth.
            if   console_EnvType==1 or only_RGB:  
                                     return name_to_rgb(color)
            elif console_EnvType==2: return name_to_256(color)
            elif console_EnvType==3: return name_to_16 (color)
            else:                    return 0

        except ColorsValueError: # Re-raise custom errors
            raise
        except Exception as e: # Catch other parsing errors
            raise ColorsValueError(error_value=color, message=f"Error parsing color string: {e}")
    else:
        raise ColorsValueError(error_value= color,message=f"Invalid input: Expected a tuple, list, or string. Got: {type(color).__name__}: {color}")


def Log(type, msg):
    # Placeholder for logging function, as per user's code
    log_co =        "\033[38;2;230;10;230m"
    log_from_co =   "\033[38;2;153;51;153m"
    log_msg_co =    "\033[38;2;240;5;5m" 
    # print(f"{log_co}Log \033[0m[{log_from_co}{type}\033[0m]: {log_msg_co}{msg}\033[0m")   

def Log2(type, msg):
    # Placeholder for logging function, as per user's code
    log_co =        "\033[38;2;230;10;230m"
    log_from_co =   "\033[38;2;153;51;153m"
    log_msg_co =    "\033[38;2;240;5;5m" 
    # print(f"{log_co}Log \033[0m[{log_from_co}{type}\033[0m]: {log_msg_co}{msg}\033[0m")   

# Log2("TEST", 'TEST 2')

def isgredinat(value: Any) -> bool:
    """
    Checks if a given value is configured as a list or tuple of multiple colors, 
    implying it represents a gradient (List[ColorInput] or Tuple[ColorInput, ...]).
    
    Args:
        value (Any): The input value to check (e.g., from *colors or background).

    Returns:
        bool: True if the value is an iterable containing multiple elements 
              suitable for a gradient; False otherwise.
    """
    return (    isinstance(value , (list, tuple)) 
            and len(value) > 1
            and isinstance(value[0], (str, list, tuple))
        )   

def get_ansi_color(_color: Any) -> str:
    """
    Retrieves the raw starting ANSI escape code for a given color configuration.
    
    This function is a uPURPLEity that delegates the actual ANSI code generation 
    to the Colors class instance.
    
    Args:
        _color (Any): A single ColorInput or an initialized Colors object.

    Returns:
        str: The raw ANSI escape sequence (e.g., "\033[38;2;R;G;Bm").
    """
    # Assuming Colors class is available in scope
    if isinstance(_color, Colors):
        return _color._get_ansi_color(get_list=False)
    else:
        # Create a temporary Colors object to process the input
        return Colors(_color)._get_ansi_color(get_list=False)



class Colors:
    """
    A class for configuring and applying 24-bit True Color (RGB) ANSI escape codes 
    to console text.

    This class acts as a flexible color scheme configuration object, supporting:
    1. Single uniform foreground color.
    2. Foreground gradient (multiple colors).
    3. Single uniform background color.
    4. Background gradient (multiple colors).

    The color configuration is set during initialization, and the actual coloring 
    is applied to text using the `apply()` or `apply_to_str()` methods.

    Note: The effectiveness of 24-bit colors and gradients depends entirely on the 
    terminal emulator's support for True Color ANSI escape sequences.
    """

    # ANSI escape code for resetting text formatting
    
    # ANSI escape code prefixes for 24-bit true color (RGB)
    _FG_ANSI_PREFIX = "\033[38;2;" # Foreground color
    _BG_ANSI_PREFIX = "\033[48;2;" # Background color
    _ANSI_SUFFIX = "m"             # Suffix for ANSI color codes

    RESET = "\033[0m"
# ColorTuple = Tuple[int, int, int]
# ColorInput = Union[ColorTuple , Color_Name]

    @overload
    def __init__(self, *colors: ColorInput | GredinatInput , background: ColorInput | bool | None = None, angle: int | None = None): ...
    
    @overload
    def __init__(self, style: GradientStyles, *, background: ColorInput | GredinatInput | bool | None = None, angle: int | None = None): ...
    
    @overload
    def __init__(self, color: ColorInput | GredinatInput, *, background: ColorArg | GredinatInput | bool | None = None, angle: int | None = None): ...


    def __init__(
        self,
        *colors, # Changed to ColorInput for clarity
        background  = None,  # Can be True, False, a single color, or a list of colors for gradient
        angle: int | None = None, # if gradient then gradient angle 
        style = None,
        # color_reset: bool | None = None
    ):
        """
        Initializes the Colors object as a scheme configuration for foreground and background.

        **Supported Color Input Formats (`ColorInput`):**
        - **RGB Tuple:** `(255, 0, 0)`
        - **Named Color:** `"red"`, `"midnightblue"` (requires lookup in internal color data)
        - **Hex String:** `"#FF0000"` (or short form `"#F00"`)
        - **Color Space String:** `"rgb: 255,0,0"`, `"hsl: 120,1,0.5"`

        Args:
            *colors (ColorInput | GredinatInput | GradientStyles, optional): Positional arguments 
                defining the foreground color(s).
                - **Single Color:** One `ColorInput` argument provided.
                - **Gradient:** Multiple `ColorInput` arguments provided, or a single list/tuple
                  of `ColorInput`s.
                - **Style:** A `GradientStyles` object (if provided, it replaces positional colors).
            
            background (ColorInput | List[ColorInput] | bool | None): Optional. Specifies the background.
                - **`None` (default) or `False`**: **No background color is applied.**
                - **`True`**: Applies the configured **Foreground** color (or gradient) as the **Background**.
                  Foreground is reset to default.
                - `ColorInput`: A specific uniform background color.
                - `List[ColorInput]`: A list of colors to create a **background gradient**.

            angle (int | None): Optional. Specifies the angle of the gradient (if one is used). 
                Default is None, typically resulting in a linear, left-to-right calculation.

            style (GradientStyles | None): Optional. Used to apply a predefined gradient pattern. 
                If provided, it overrides explicit positional `*colors`.

        Attributes Set:
            self.color (ColorTuple | None): The single foreground RGB color.
            self._colors (List[ColorTuple]): The list of RGB colors for a foreground gradient.
            self._gradient (bool): True if the foreground is a gradient.
            self.bg_color (ColorTuple | None): The single background RGB color.
            self._bg_colors (List[ColorTuple]): The list of RGB colors for a background gradient.
            self._bg_gradient (bool): True if the background is a gradient.
        """
        self.style = style
        self.angle = angle
        # self.color_reset = color_reset
        self._gradient = False # Flag to indicate if foreground is a gradient
        self._bg_gradient = False # Flag to indicate if background is a gradient
        self.only_RGB = console_EnvType == 1 # Always true for 24-bit mode (as per mock)
        self.is_backgroun = background is True
        # if background is True:
        #     background = colors
        #     colors = ()
        Log2(" START THIS IS BACKGOUND:", background)

        self.color:      ColorTuple | None = None # Stores single foreground RGB tuple
        self.bg_color:   ColorTuple | None = None # Stores single background RGB tuple
        self._colors:    List[ColorTuple]  = []   # Stores list of RGB tuples for foreground gradient
        self._bg_colors: List[ColorTuple]  = []   # Stores list of RGB tuples for background gradient

        if style:
            # print("style", style)
            # print("colors", colors)
            colors = (self.style,)
        Log('[Log colors, background:] at start:', f'{colors, background}')
        # Determine if foreground is a single color or a gradient
        if background is True:
            background = colors[0] if len(colors) == 1 else colors
            colors = []
            Log('[Log colors, background:] in backgroun is True:', f'{colors}, {background}')
        elif len(colors) == 1:
            first_arg = colors[0]
            # Check if the single positional argument is a list/tuple, implying a gradient
            # if isinstance(first_arg, (list, tuple)) and len(first_arg) > 1 and \
            #    all(isinstance(c, (str, tuple, list)) for c in first_arg):
            if isgredinat(first_arg):
                self._colors   = [get_RGB_values(c, only_RGB=True) for c in first_arg]
                self._gradient = True
            # if len(first_arg) == 1:
            #     self._colors   = get_RGB_values(first_arg[0], only_RGB=True)
            else:
                # It's a single direct color
                self.color = get_RGB_values(first_arg, only_RGB=self.only_RGB)

                # self.color = get_RGB_values(
                    # first_arg[0] if len(first_arg) == 1 else first_arg, 
                    # only_RGB=self.only_RGB)
                
        elif len(colors) > 1:
            # Multiple positional arguments mean a gradient
            self._colors = [get_RGB_values(c, only_RGB=True) for c in colors]
            self._gradient = True
        # If no *colors are provided, self.color and self._colors remain None/empty

        # Process background color
        # if background is True:
        #     self.bg_color = (0, 0, 0) # Default true background to black RGB
            # ======== changes ========
            # self.bg_color =  self.color
            # self.color = None
            # =========================
        Log2(" UPTO THIS IS BACKGOUND:", background)

        if isinstance(background, (list, tuple)) and len(background) >= 1: # Handles lists/tuples for background gradient
            Log2("geint background:", f'{background}')
            if (self.is_backgroun or len(background) > 1) and all(isinstance(c, (str, tuple, list)) for c in background):
                Log("geint background:", "len(background) > 1 and all(isinstance(c, (str, tuple, list)) for c in background)")
                self._bg_colors = [get_RGB_values(c, only_RGB=True) for c in background]
                self._bg_gradient = True
                self.bg_color = None # Ensure single bg_color is not set if gradient
            # elif len(background) == 3 and all(isinstance(c, int) for c in background):
                # If it's a single RGB tuple for background
                # self.bg_color = get_RGB_values(background, only_RGB=self.only_RGB)
            
            else:
                Log("Error", f"Invalid background color list/tuple format: {background}")
                # print("fale back")
                # self.bg_color = None # Fallback to no background on error
                self.bg_color = get_RGB_values(
                    background[0] if len(background) == 1 else background, 
                    only_RGB=self.only_RGB
                )

        elif background:
            # If a specific single color string is provided for background
            Log2("THIS IS BACKGOUND:", background)
            self.bg_color = get_RGB_values(background, only_RGB=self.only_RGB)
            
            # try:
            #     self.bg_color = get_RGB_values(background, only_RGB=self.only_RGB)
            # except ColorsValueError as E:
            #     # Log("Error", f"Invalid background color: {E.value} - {E.message}")
            #     self.bg_color = None # Fallback to no background on error
        # print('[Log colors, background:] After __init__:', colors, background)

        
        
    def apply(self, values: List[str], angle: int | None = None, reset: bool = True) -> Generator[List[str], None, None]: 
        """
        Applies the configured foreground/background scheme to a sequence of strings 
        (typically lines of text).

        If the scheme includes a gradient, this function delegates to `apply_gradient`
        to calculate the color changes character-by-character across the text.

        Args:
            values (List[str] | Tuple[str] | Generator[str, None, None]): An iterable 
                of strings, where each string is typically treated as a line or segment
                to be colored.
            angle (int | None, optional): Overrides the gradient angle set during 
                initialization. Used only if a gradient is configured. Defaults to None.
            reset (bool, optional): If True, ensures the appropriate ANSI reset code(s) 
                are appended to the end of the colored output segments to prevent color 
                leakage into subsequent text. Defaults to True.

        Yields:
            Generator ([List[str], None, None]): A generator that yields a list of 
                formatted string segments for each input line. Each segment contains 
                the necessary ANSI escape codes.

        Raises:
            TypeError: If `values` is not an accepted iterable type.
        """
        if not isinstance(values, (list, tuple, Generator)):
            raise TypeError("Values must be a list, tuple, or generator of strings.")

        # Determine effective foreground colors to pass to apply_gradient
        effective_fg_colors: List[ColorTuple] = []
        if self._gradient:
            effective_fg_colors = self._colors
        elif self.color:
            effective_fg_colors = [self.color] # Wrap single color in list for apply_gradient consistency

        # Determine effective background colors to pass to apply_gradient
        effective_bg_colors: List[ColorTuple] | ColorTuple | bool = False
        if self._bg_gradient:
            effective_bg_colors = self._bg_colors
        elif self.bg_color:
            effective_bg_colors = self.bg_color # Pass single tuple directly
        elif self.bg_color is True: # Should already be handled in __init__ to (0,0,0)
            # effective_bg_colors = (0,0,0)
            effective_bg_colors = True

        is_gradient_pre_config = (bool(self.color),  bool(self.bg_color), self._gradient, self._bg_gradient)

        # If either foreground or background is a gradient, use apply_gradient
        if self._gradient or self._bg_gradient:
            Log("[Colors.apply] Calling apply_gradient", "True")
            Log("[Colors.apply] effective_fg_colors", effective_fg_colors)
            Log("[Colors.apply] effective_bg_colors", effective_bg_colors)
            # print("start Gen Apply")
            yield from apply_gradient(
                text_list=values,
                colors=effective_fg_colors, # Always a list of tuples for gradient, or single tuple in list
                background=effective_bg_colors, # Can be list of tuples, single tuple, or False
                angle=angle or self.angle,
                reset=reset,
                is_gradient_pre_config=is_gradient_pre_config,
            ) 

        else: # No gradients, apply uniform colors
            fg_ansi = values_to_ansi_fg(self.color   ) if self.color    != None else ""
            bg_ansi = values_to_ansi_bg(self.bg_color) if self.bg_color != None else ""
        
            combined_ansi = f"{fg_ansi}{bg_ansi}"
                
            _RESET = ''
            if reset:
                if fg_ansi: _RESET += RESET_FG
                if bg_ansi: _RESET += RESET_BG

            # Log("[THIS IS RESET - T]:", f'{[_RESET], [RESET_FG, RESET_BG]}\n\n\n')

            if self.color and not self.bg_color:  # Only foreground color
                yield from ((( [fg_ansi + line[0]] + [*line[1:-1]] + [line[-1] + _RESET]
                            ) if len(line) > 1 else [fg_ansi + line + _RESET] 
                        ) if line else [''] 
                    for line in values
                )
            elif combined_ansi: 

                Log("log[conform-single]: coming from colors3, colors, Tools", f'{(fg_ansi, ":" , bg_ansi)}')
                yield from (    [f"{combined_ansi}{char}{_RESET}" for char in line] 
                            if line else _RESET
                        for line in values
                )

            else: # No color applied
                Log("log[No Color]:", f'{(fg_ansi,":", bg_ansi)}')
                yield from (list(line) for line in values)


    def apply_to_str(self, value:str, reset:bool=True) -> str:
        """
        Applies the configured color scheme to a single string value.

        If a gradient is configured, it processes the string character-by-character.
        It handles embedded newline characters (`\\n`) correctly by inserting the 
        color escape codes after each line break, ensuring the coloring persists 
        across multiple lines.

        Args:
            value (str): The single string to be colored.
            reset (bool, optional): If True, appends the necessary ANSI reset 
                code(s) at the very end of the output. Defaults to True.

        Returns:
            str: The fully formatted (colored) string.

        Raises:
            ColorsValueError: If an unexpected error occurs during color application.
        """
        if value=="" or type(value)!=str: 
            _Warning(
                value,
                f"Type of input value muct be `str`: got {type(value)}"
            ).print()
            return value
        
        try:
            if self._gradient or self._bg_gradient:
                _value = ""
                if "\n" in value:
                    for i in self.apply(value.split("\n"), reset=reset):
                        _value += "".join(i) + "\n"
                else:
                    for i in self.apply([value], reset=reset):
                        _value += "".join(i)

                return _value
            
            else:
                _color, _reset = '', ''
                if self.color is not None:
                    _color += values_to_ansi_fg(self.color) 
                    _reset += RESET_FG if reset else ''
                if self.bg_color is not None:
                    _color += values_to_ansi_bg(self.bg_color) 
                    _reset += RESET_BG if reset else ''

                # Log("[THIS IS RESET - T]:", f'{[_reset], [RESET_FG, RESET_BG]}\n\n\n')

                if "\n" in value:
                    value = value.replace("\n", _reset + "\n" + _color)

                _value = _color + value + _reset
                return _value
        
        except Exception as E:
            raise ColorsValueError(error_value=value, message=f"Got UnExpected Error While Applying Colors to str: {E}")
    
    def _get_ansi_color(self, get_list=False) -> str | list:
        """
        Internal uPURPLEity to retrieve the raw starting ANSI escape sequence or the 
        list of colors used for a gradient.
        """

        _color = ''
        if self._gradient or self._bg_gradient:  
            if get_list:            
                return [self._colors, self._bg_colors]
            else:
                if self._colors:    _color += rgb_to_ansi_func   (*self._colors[0])
                if self._bg_colors: _color += rgb_to_bg_ansi_func(*self._bg_colors[0])

        else:
                if self.color:      _color += values_to_ansi_fg(self.color)
                if self.bg_color:   _color += values_to_ansi_bg(self.bg_color) 

        return _color
    
    def __str__(self):
        """
        Provides the raw starting ANSI escape code sequence for the current configuration.
        This is useful for concatenating the color configuration directly with a string.
        (e.g., `str(Colors('red')) + 'text'`).
        """
        return self._get_ansi_color()
    
    def __repr__(self):
        """
        Provides a developer-friendly string representation of the Colors object,
        detailing its full configuration (foreground, background, and angle).
        Useful for debugging.
        """
        fg_display = self._colors if self._gradient else self.color
        bg_display = self._bg_colors if self._bg_gradient else ((self.bg_color + 10) if console_EnvType == 3 and self.bg_color else self.bg_color)
        return (f"Colors(foreground={fg_display!r}, background={bg_display!r}, angle={self.angle!r})")
    
    def __add__(self, value: str) -> str:
        """
        Allows the class to be used with the addition operator: `Colors(...) + "text"`.
        The method uses `apply_to_str()` to format the string.
        """
        return self.apply_to_str(value)

    def __radd__(self, value: str) -> str:
        """
        Allows the class to be used with the reverse addition operator: `"text" + Colors(...)`.
        (Though typically used as `Colors(...) + "text"`).
        The method uses `apply_to_str()` to format the string.
        """
        return self.apply_to_str(value)
