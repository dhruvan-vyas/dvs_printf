from typing      import TypeAlias
from sys         import platform
from os          import getenv, getenv
from subprocess  import check_output, CalledProcessError, DEVNULL
from dataclasses import dataclass

attrs_str  : TypeAlias = str
attrs_RESET: TypeAlias = str

__all__ = [
    'console_EnvType',
    'rgb_to_ansi_func',
    'rgb_to_bg_ansi_func',
    
    'RESET',
    'RESET_FOREGROUND',
    'RESET_BACKGROUND',    
    'Font_Styles'
]

# Universal RESETS
RESET = "\033[0m"
"""Reset all terminal attributes (colors, styles, etc)."""

RESET_FOREGROUND = "\033[39m"
"""Reset text color to default."""

RESET_BACKGROUND = "\033[49m"
"""Reset background color to default."""
 
@dataclass
class Font_Styles:
    """
    ANSI font style codes for terminal text formatting.

    Defines common text styles using ANSI escape sequences.
    Use individual attributes or the `get()` method to combine styles.
    """

    BOLD          = "\033[1m"
    FAINT         = "\033[2m"
    ITALIC        = "\033[3m"
    UNDERLINE     = "\033[4m"
    BLINK         = "\033[5m"
    INVERSE       = "\033[7m"
    CONCEAL       = "\033[8m"
    STRIKETHROUGH = "\033[9m"

    RESET_BOLD          = "\033[22m"
    RESET_FAINT         = "\033[22m"
    RESET_ITALIC        = "\033[23m"
    RESET_UNDERLINE     = "\033[24m"
    RESET_BLINK         = "\033[25m"
    RESET_INVERSE       = "\033[27m"
    RESET_CONCEAL       = "\033[28m"
    RESET_STRIKETHROUGH = "\033[29m"
    
    ATTR_MAP = {
        "bold"          : ( BOLD         , RESET_BOLD          ),
        "faint"         : ( FAINT        , RESET_FAINT         ),
        "italic"        : ( ITALIC       , RESET_ITALIC        ),
        "underline"     : ( UNDERLINE    , RESET_UNDERLINE     ),
        "blink"         : ( BLINK        , RESET_BLINK         ),
        "inverse"       : ( INVERSE      , RESET_INVERSE       ),
        "conceal"       : ( CONCEAL      , RESET_CONCEAL       ),
        "strikethrough" : ( STRIKETHROUGH, RESET_STRIKETHROUGH ),
    }
    """
        Mapping of style names to (start_code, reset_code) pairs.

        Keys:
            str: Style name (e.g., "bold", "italic")
        Values:
            tuple[str, str]: Tuple of (start ANSI code, reset ANSI code)
    """
    

    @classmethod
    def get(cls, attrs: list[str]) -> tuple[attrs_str, attrs_RESET]:
        """
        Generate combined ANSI start and reset sequences for a list of styles.

        Args:
            attrs (list[str]): List of style names (e.g., ["bold", "underline"]).
                - ["bold", "faint", "italic", "underline", "blink", "inverse", "conceal", "strikethrough"]

            Test_attrs (list[str]): List Of Any
            
        Returns:
            tuple (tuple[str, str]): Combined start and reset ANSI sequences.

        Raises:
            Warning: If any style name is invalid or attrs is not a list.
        """
        from ..exceptions._warning import _Warning
        if not isinstance(attrs, list):
            raise _Warning(attrs, "Expected a LIST of style names. e.g., ['bold', 'Italic']" f', Got: {repr(attrs)}')
        
        start_seq = reset_seq = ""
        try:
            for name in attrs:
                start, end = cls.ATTR_MAP[name.lower()]
                start_seq += start
                reset_seq += end

        except:
            value_type = type(name)
            if value_type != str:
                E_value = f"The Attribute Value Must Be String (Not {value_type.__name__}). GOT: {repr(name)}"
            elif name != cls.ATTR_MAP:
                E_value = f"The Attribute '{name}' is NOT Defiend in ATTR_MAP."
            else:
                E_value = "Somthing Went Wrong While Collecting The Attributs."

            _Warning(
                name, 
                E_value
            ).print()

        return start_seq, reset_seq
    
def _get_Console_Env_Type() -> int:
    """
    Returns a number representing the console environment's color capabilities.
    Type 1: Truecolor (24-bit)
    Type 2: 256-color
    Type 3: 16-color
    Type 4: No color (monochromatic, or NO_COLOR environment variable set)
    """
    # Check for explicit NO_COLOR environment variable first
    # This is a widely adopted convention to disable color output.
    if getenv('NO_COLOR'):
        return 4  # No color support requested

    # Windows-specific check
    if platform == 'win32':
        # Windows Terminal and WSL environments typically support Truecolor.
        # WT_SESSION is a strong indicator for Windows Terminal.
        # WSL_DISTRO_NAME indicates running inside WSL, which usually has good terminal support.
        if getenv('WT_SESSION') or getenv('WSL_DISTRO_NAME'):
            return 1  # Truecolor support in Windows Terminal or WSL
        
        # For standard cmd.exe or PowerShell on modern Windows (Win10+),
        # ANSI escape codes are generally supported, including 256 colors.
        # This is a heuristic, as direct detection is tricky without external libs.
        # However, some older cmd.exe versions might only support 16 colors.
        # We'll default to 256-color as it's more common on recent Windows.
        return 2

    # Unix-like systems (Linux, macOS, Git Bash, Cygwin)
    else:
        colorterm = getenv('COLORTERM', '').lower()
        term = getenv('TERM', '').lower()

        # Check for explicit Truecolor support via COLORTERM
        if 'truecolor' in colorterm or '24bit' in colorterm:
            return 1

        # Check for 256-color support via TERM or tput
        if '256color' in term:
            return 2
        try:
            # Use tput to query terminal capabilities. stderr=DEVNULL prevents output on failure.
            colors_output = check_output(['tput', 'colors'], stderr=DEVNULL).decode('utf-8').strip()
            if int(colors_output) >= 256:
                return 2
        except (FileNotFoundError, CalledProcessError, ValueError):
            # tput not found, command failed, or output was not an integer.
            # This means we can't confirm 256+ colors via tput.
            pass

        # Fallback to 16-color support if no higher capability is detected.
        return 3
    
# Get the console environment type once
console_EnvType: int = _get_Console_Env_Type()
"""
A Number of console env Type (Rank).
    Type 1: (Truecolor, 24bit, ...) 
    Type 2: (256Color, tput, ...)
    Type 3: (16color, others)
    Type 4: (No color, monochromatic, NO_COLOR env var)
"""


def _rgb_to_ansi_16(r: int, g: int, b: int) -> int:
    """
    Converts an RGB color to the closest 16-color ANSI code.
    This is a simplified heuristic.
    Results are cached for performance.
    """
    # Determine brightness (average of R, G, B)
    brightness = (r + g + b) // 3

    # Check for grayscale first
    # If all components are very close, it's a shade of gray
    if max(r, g, b) - min(r, g, b) < 30: # Threshold for "grayscale"
        if brightness < 60: return 30 # Black
        elif brightness < 180: return 90 # Dark Gray (Bright Black)
        else: return 97 # Bright White

    # Determine dominant color and assign base ANSI code
    # Normal colors (30-37)
    # Bright colors (90-97)
    
    # Simple quantization to determine primary/secondary color
    # and then apply brightness
    ansi_code = 0
    if r > g and r > b: # Red dominant
        ansi_code = 31 # Red
    elif g > r and g > b: # Green dominant
        ansi_code = 32 # Green
    elif b > r and b > g: # Blue dominant
        ansi_code = 34 # Blue
    elif r > 0 and g > 0: # Yellow-ish (Red + Green)
        ansi_code = 33 # Yellow
    elif r > 0 and b > 0: # Magenta-ish (Red + Blue)
        ansi_code = 35 # Magenta
    elif g > 0 and b > 0: # Cyan-ish (Green + Blue)
        ansi_code = 36 # Cyan
    else:
        ansi_code = 37 # Default to White

    # Apply brightness for bright ANSI codes (add 60)
    if brightness > 128 and ansi_code != 30: # Don't brighten true black
        return ansi_code + 60
    return ansi_code



# Initialize ANSI functions based on detected console type
_Ansi_fg          = None
_Ansi_bg          = None
_Ansi_fg_text     = None
_Ansi_bg_text     = None
values_to_ansi_fg = None
values_to_ansi_bg = None

if console_EnvType == 1:  # Env_Type 1: (truecolor, 24bitColor)
    _Ansi_fg          = lambda r,g,b:     f"\033[38;2;{r};{g};{b}m"                # Foreground color
    _Ansi_bg          = lambda r,g,b:     f"\033[48;2;{r};{g};{b}m"                # Background color
    _Ansi_fg_text     = lambda r,g,b,txt: f"\033[38;2;{r};{g};{b}m{txt}"           # Foreground colored Text
    _Ansi_bg_text     = lambda r,g,b,txt: f"\033[48;2;{r};{g};{b}m{txt}\033[0m"    # Background colored Text
    values_to_ansi_fg = lambda rgb:       f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    values_to_ansi_bg = lambda rgb:       f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

elif console_EnvType == 2: # Env_Type 2: (256color, Tput)
    # The 256-color conversion formula is a standard way to map RGB to the xterm 256-color palette.
    # It quantizes the R, G, B components into a 6x6x6 cube, plus 24 grayscale steps.
    _Ansi_fg          = lambda r,g,b:     f"\033[38;5;{16 + (36 * round(r / 51)) + (6 * round(g / 51)) + round(b / 51)}m"              # Foreground color
    _Ansi_bg          = lambda r,g,b:     f"\033[48;5;{16 + (36 * round(r / 51)) + (6 * round(g / 51)) + round(b / 51)}m"              # Background color
    _Ansi_fg_text     = lambda r,g,b,txt: f"\033[38;5;{16 + (36 * round(r / 51)) + (6 * round(g / 51)) + round(b / 51)}m{txt}"         # Foreground colored Text
    _Ansi_bg_text     = lambda r,g,b,txt: f"\033[48;5;{16 + (36 * round(r / 51)) + (6 * round(g / 51)) + round(b / 51)}m{txt}\033[0m"  # Background colored Text
    values_to_ansi_fg = lambda ansi:      f"\033[38;5;{ansi}m"
    values_to_ansi_bg = lambda ansi:      f"\033[48;5;{ansi}m"

elif console_EnvType == 3: # Env_Type 3: (16color, others)
    # Use the helper function to map RGB to the closest 16-color ANSI code
    _Ansi_fg          = lambda r,g,b:     f"\033[{_rgb_to_ansi_16(r,g,b)}m"                     # Foreground color
    _Ansi_bg          = lambda r,g,b:     f"\033[{_rgb_to_ansi_16(r,g,b) + 10}m"                # Background color (+10 to foreground code)
    _Ansi_fg_text     = lambda r,g,b,txt: f"\033[{_rgb_to_ansi_16(r,g,b)}m{txt}"                # Foreground colored Text
    _Ansi_bg_text     = lambda r,g,b,txt: f"\033[{_rgb_to_ansi_16(r,g,b) + 10}m{txt}\033[0m"    # Background colored Text (+10)
    values_to_ansi_fg = lambda ansi:      f"\033[{ansi}m"                                       # Foreground color
    values_to_ansi_bg = lambda ansi:      f"\033[{ansi + 10}m"                                  # Background color (+10)

elif console_EnvType == 4: # Env_Type 4: (No color)
    # For no color, all functions return empty strings, effectively disabling color.
    _Ansi_fg          = lambda r,g,b:     ""
    _Ansi_bg          = lambda r,g,b:     ""
    _Ansi_fg_text     = lambda r,g,b,txt: txt # Only return the text, no color codes
    _Ansi_bg_text     = lambda r,g,b,txt: txt # Only return the text, no color codes
    values_to_ansi_fg = lambda ansi :     ""
    values_to_ansi_bg = lambda ansi :     ""



rgb_to_ansi_func = _Ansi_fg
"""
Generates an ANSI escape sequence for setting the foreground color.

Args:
    r (int): Red component (0-255).
    g (int): Green component (0-255).
    b (int): Blue component (0-255).

Returns:
    str: ANSI escape sequence for setting the foreground color.
"""


rgb_to_bg_ansi_func = _Ansi_bg
"""
Generates an ANSI escape sequence for setting the background color.

Args:
    r (int): Red component (0-255).
    g (int): Green component (0-255).
    b (int): Blue component (0-255).

Returns:
    str: ANSI escape sequence for setting the background color.
"""

color_text_fg = _Ansi_fg_text
"""
Applies foreground color to text using RGB values.

Returns:
    function: A lambda function that generates an ANSI-colored text string.
"""

color_text_bg = _Ansi_bg_text
"""
Applies background color to text using RGB values.

Returns:
    function: A lambda function that generates an ANSI-colored text string with background color.
"""


del _Ansi_fg, _Ansi_bg, _get_Console_Env_Type, getenv, check_output

