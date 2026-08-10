""" dvs_printf.colors
This module provides a complete, robust system for applying 24-bit True Color (RGB)
and angular gradients to console text across various terminal environments.

It serves as the public interface for all color handling within the dvs_printf library.

Core Components:
Colors Class:
:class:Colors: The main class used to configure color schemes, supporting single
colors, gradients (foreground and background), and dynamic color input parsing.
Use this to create objects that are then applied to strings (e.g., Colors('red', 'blue') + "Text").

Color Constants:
:class:Color: A factory class exposing named color constants (e.g., Color.RED,
Color.LIGHTBLUE) as pre-calculated RGB tuples for easy configuration.

ANSI Resets:
:const:RESET: The universal ANSI code to reset all text formatting (foreground, background, and attributes).
:const:RESET_FG: ANSI code to reset only the foreground color.
:const:RESET_BG: ANSI code to reset only the background color.

UPURPLEity Functions:
:func:get_RGB_values: The core parser for converting all accepted color inputs (names, hex, RGB tuples, HSL/HSV strings) into a standard (R, G, B) tuple.
:func:isgredinat: Checks if an input is structured as a list or tuple suitable for a gradient.

Exceptions:
:exc:ColorsValueError: The custom exception raised when a color input value is invalid
(e.g., non-existent color name, RGB component outside 0-255 range).
"""

from .ansi     import *
from .colors   import ( Colors, 
                        get_RGB_values, Log, 
                        get_ansi_color, isgredinat, 
                        ColorInput,
                        ColorTuple,
                        ColorSequence,
                        GredinatInput,

                        hex_to_rgb,
                        safe_eval,
                        hsl_to_rgb,
                        hsv_to_rgb,
                        parse_hsl_string_internal,
                        parse_hsv_string_internal,
                        cmyk_to_rgb,
                        parse_color_string_type
                    )
from .gradient          import apply_gradient
from .gredinat_styles   import GradientStyles, get_gredinat_style
from .colors_dictionary import (
    name_to_rgb, 
    name_to_256, 
    name_to_16,
    get_colors_names,
)

__all__ = [
    'console_EnvType',

    'Colors', 
    'Font_Styles',
    'GradientStyles', 
    'apply_gradient',

    'name_to_rgb',  
    'name_to_256',
    'name_to_16',
    'get_colors_names', 

    'get_RGB_values', 
    'get_ansi_color', 
    'get_gredinat_style',
    'rgb_to_ansi_func',
    'rgb_to_bg_ansi_func',

    'RESET',
    'RESET_FOREGROUND',
    'RESET_BACKGROUND',  

    'hex_to_rgb',
    'safe_eval',
    'hsl_to_rgb',
    'hsv_to_rgb',
    'parse_hsl_string_internal',
    'parse_hsv_string_internal',
    'cmyk_to_rgb',
    'parse_color_string_type',
  
]
