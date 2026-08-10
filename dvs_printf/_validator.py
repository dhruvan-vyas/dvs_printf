# from ._printf_helper import available_styles, chack_styles
# from . exceptions  import ( StyleNameError,
#                             DelayValueError,
#                             SpeedValueError,
#                             AttrsValueError,
#                             GetmatValueError,
#                             dvs_BaseException
#                         )

# __all__ = [
#     'UnknownError',
#     '_validate_style',
#     '_validate_speed',
#     '_validate_delay',
#     '_validate_attrs',
#     '_validate_getmat',
# ]

# def UnknownError(_):
#     raise dvs_BaseException(_,"Error Type Does Not Found")

# def _validate_style(value):
#     if isinstance(value, str) and ( 
#             value in available_styles 
#          or any(i in value for i in chack_styles)
#     ):
#         return True
#     raise StyleNameError(value)

# def _validate_speed(value):
#     if isinstance(value, (int, float)) and (1 <= value <= 6 or value == 7):
#         return True
#     raise SpeedValueError(value)

# def _validate_delay(value):
#     if isinstance(value, (int, float)) and value >= 0:
#         return True
#     raise DelayValueError(value)

# def _validate_attrs(value):
#     if type(value) == list and all([type(attr) == str for attr in value]): 
#         return True
#     raise AttrsValueError(value)

# def _validate_getmat(value):
#     if isinstance(value, (bool, str)) and value in (True, False, "true", "show"):
#         return True
#     raise GetmatValueError(value)



"""
Core validation uPURPLEities for the dvs_printf module.

This module contains functions responsible for validating all user-defined parameters 
(style, speed, delay, attributes, etc.) against predefined rules and raising 
specific, customized exceptions upon failure.

The use of specific validation functions ensures that errors are caught early and 
reported with context-rich tracebacks.
"""

from ._printf_helper import available_styles, chack_styles
from .exceptions     import (
    StyleNameError,
    DelayValueError,
    SpeedValueError,
    AttrsValueError,
    GetmatValueError,
    dvs_BaseException
)
from typing import Any, Union, List

# List of exceptions exposed publicly by this module
__all__ = [
    'UnknownError',
    '_validate_style',
    '_validate_speed',
    '_validate_delay',
    '_validate_attrs',
    '_validate_getmat',
]

def UnknownError(value: Any):
    """
    Raises a generic dvs_BaseException for unexpected errors not covered by 
    specific validation checks.
    
    Args:
        value (Any): The value or error object that caused the unknown issue.
    """
    raise dvs_BaseException(value, "Error Type Does Not Found")

def _validate_style(value: Any) -> bool:
    """
    Validates the user-provided animation style name.
    
    Checks if the style string matches a known available style or contains a keyword 
    (like 'center' or 'async') used for complex style variations.

    Args:
        value (Any): The style input (expected to be a string).

    Returns:
        bool: True if the style is valid.

    Raises:
        StyleNameError: If the style name is invalid or unknown.
    """
    if isinstance(value, str) and ( 
            value in available_styles 
         or any(i in value for i in chack_styles)
    ):
        return True
    raise StyleNameError(value)

def _validate_speed(value: Any) -> bool:
    """
    Validates the speed multiplier parameter.
    
    Speed must be an integer or float, and must be within the defined range 
    [1, 6] or exactly 7 (for max speed).

    Args:
        value (Any): The speed input.

    Returns:
        bool: True if the speed value is valid.

    Raises:
        SpeedValueError: If the value is not a number or outside the range [1, 6, 7].
    """
    if isinstance(value, (int, float)) and (1 <= value <= 6 or value == 7):
        return True
    raise SpeedValueError(value)

def _validate_delay(value: Any) -> bool:
    """
    Validates the delay parameter.
    
    Delay must be a non-negative integer or float (>= 0).

    Args:
        value (Any): The delay input.

    Returns:
        bool: True if the delay is valid.

    Raises:
        DelayValueError: If the value is negative or not a number.
    """
    if isinstance(value, (int, float)) and value >= 0:
        return True
    raise DelayValueError(value)

def _validate_attrs(value: Any) -> bool:
    """
    Validates the list of text attributes (`attrs`).
    
    The value must be a list where all elements are strings.

    Args:
        value (Any): The attributes input.

    Returns:
        bool: True if the attribute list is valid.

    Raises:
        AttrsValueError: If the value is not a list or contains non-string elements.
    """
    if isinstance(value, list) and all([isinstance(attr, str) for attr in value]): 
        return True
    raise AttrsValueError(value)

def _validate_getmat(value: Any) -> bool:
    """
    Validates the `getmat` parameter for complex array/matrix handling.
    
    The value must be one of the explicitly allowed modes: True, False, "true", or "show".

    Args:
        value (Any): The getmat input.

    Returns:
        bool: True if the mode is valid.

    Raises:
        GetmatValueError: If the value is outside the set of allowed inputs.
    """
    if isinstance(value, (bool, str)) and value in (True, False, "true", "show"):
        return True
    raise GetmatValueError(value)
