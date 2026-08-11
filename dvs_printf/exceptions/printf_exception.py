import difflib
from ._colored_vars  import *
from ._base_exception import dvs_BaseException

import difflib
from re import escape, search
from typing import Optional, Tuple, List, TYPE_CHECKING

from ._colored_vars  import * 
from ._base_exception import dvs_BaseException

# Type checking for external modules to prevent circular imports if necessary
if TYPE_CHECKING:
    from .._printf_helper import available_styles

# __all__ = [
#     'StyleNameError'  , 
#     'DelayValueError' , 
#     'SpeedValueError' , 
#     'AttrsValueError' ,
#     'GetmatValueError',
# ]


class StyleNameError(dvs_BaseException, ValueError):
    """
    Exception raised when a requested text style name is not defined or recognized.

    This exception uses the `difflib` module to provide a helpful suggestion 
    for what the user might have intended to type.
    """
    def __init__(self, error_value:None=None):
        """
        Initializes the StyleNameError.

        It finds the closest matching style name to provide a helpful suggestion
        in the final error message.

        Args:
            error_value: The invalid style name string provided by the user.
        """
        # Importing here to prevent potential circular dependency
        from .._printf_helper  import available_styles
        
        self._error_value_type = type(error_value)
        self.value = str(error_value)
        
        # Use difflib to find the closest match
        matches = difflib.get_close_matches(str(error_value), available_styles, n=1, cutoff=0.6)
        self.suggestion = matches[0] if matches else None
        
        self._TraceBack_message = ""
        self.keyWord = "style"
        
        # Initialize base class with error value and keyword
        super().__init__(error_value, keyWord=self.keyWord, skip=1)

    def __generate_message__(self):
        """
        Generates the formatted error message, including a suggestion if one was found.

        Returns:
            The complete, user-friendly error string.
        """
        message = f"{PURPLE}StyleNameError{RESET}: The Style {GRAY}'{self.value}'{RESET} Is Not Recognized."
        if self.suggestion:
                message += f' Did you mean: {PEACH}"{self.suggestion}"{RESET}?'
        else:   message += " Please check the available styles."
        return message

class SpeedValueError(dvs_BaseException, ValueError):
    """
    Exception raised when the `speed` parameter is invalid (wrong type or out of range).

    The `speed` value must be an integer or float between 1 and 6, or exactly 7.
    """
    def __init__(self, error_value=None, message=None):
        """
        Initializes the SpeedValueError.

        Args:
            error_value: The invalid value provided for speed.
            message: An optional custom error message.
        """
        self.value = error_value
        self._error_value_type = type(error_value)
        self._notes = []
        self.message = message
        self.keyWord = "speed"
        
        # Initialize base class
        super().__init__(error_value, keyWord=self.keyWord, skip=3)

    def __generate_message__(self):
        """
        Generates the error message, providing tailored information based on 
        whether the error is due to an invalid type or an out-of-range value.

        Returns:
            The complete, formatted error string.
        """
        if self.message is not None:
            return self.message

        if self._error_value_type in (int, float):
            # Error is due to value being out of range
            return (
                f"{PURPLE}SpeedValueError{RESET}: The speed value must be a number "
                f"between {PEACH}1{RESET} to {PEACH}6{RESET}, or exactly {PEACH}7{RESET}. \n"
                f"{PURPLE}Received{RESET}: {GRAY}{self.value}{RESET}, type: {GRAY}{self._error_value_type.__name__}{RESET}"
            )
        else:
            # Error is due to incorrect type
            return (
                f"{PURPLE}SpeedValueError{RESET}: The speed value must be of type {GRAY}int{RESET} or {GRAY}float{RESET}, "
                f"and a value between {PEACH}1{RESET} to {PEACH}6{RESET}, or exactly {PEACH}7{RESET}. \n"
                f"{PURPLE}Received{RESET}: {GRAY}{self.value}{RESET}, type: {GRAY}{self._error_value_type.__name__}{RESET}."
            )

class DelayValueError(dvs_BaseException, ValueError):
    """
    Exception raised when the `delay` parameter is invalid (non-numeric or negative).

    The `delay` value must be a non-negative integer or float (>= 0).
    """
    def __init__(self, error_value=None):
        """
        Initializes the DelayValueError.

        Args:
            error_value: The invalid value provided for delay.
        """
        self.value = error_value
        self._error_value_type = type(error_value)
        self.keyWord = "delay"
        self._notes = []
        self._TraceBack_message = ""
        
        # Initialize base class
        super().__init__(error_value, keyWord=self.keyWord, skip=1)

    def __generate_message__(self):
        """
        Generates the error message, clarifying that the value must be a 
        non-negative number and indicating the received value and type.

        Returns:
            The complete, formatted error string.
        """
        if self._error_value_type in (int, float):
            return (
                f"{PURPLE}DelayValueError{RESET}: The delay value must be a non-negative number (>= {PEACH}0{RESET}). "
                f"Received: {GRAY}{[self.value]}{RESET}."
            )
        else:
            return (
                f"{PURPLE}DelayValueError{RESET}: The delay value must be of type ({GRAY}int{RESET} or {GRAY}float{RESET}), "
                f"and a non-negative number (>= {PEACH}0{RESET}). "
                f"Received: {GRAY}{self.value}{RESET} (type: {GRAY}{self._error_value_type.__name__}{RESET})."
            )

class AttrsValueError(dvs_BaseException, ValueError):
    """
    Exception raised when the `attrs` parameter is not a list of valid attribute strings.

    It provides a helpful tip on how to find the available attributes.
    """
    def __init__(self, error_value=None):
        """
        Initializes the AttrsValueError.

        Args:
            error_value: The invalid value provided for attributes.
        """
        self.value = error_value
        self._error_value_type = type(error_value)
        self.keyWord = "attrs"
        self._TraceBack_message = ""
        
        # Initialize base class
        super().__init__(error_value, keyWord=self.keyWord, skip=1)

    def __generate_message__(self):
        """
        Generates the error message, specifying the required type (`List[str]`) 
        and offering a tip to see available options.

        Returns:
            The complete, formatted error string.
        """
        return (
            f"{PURPLE}AttrsValueError{RESET}: The `attrs` must be a list of strings (List[str]) from the available attributes.\n"
            f"Received: {GRAY}{self.value}{RESET}, type: {self._error_value_type.__name__}.\n\n"
            f"{PEACH}Tip: try using `list(FontStyles.ATTR_MAP)` to see the valid options.{RESET}"
            )

class GetmatValueError(dvs_BaseException, ValueError):
    """
    Exception raised when the `getmat` parameter has an invalid value or type.

    Allowed values are restricted to boolean or specific string representations: 
    `True`, `False`, `'true'`, or `'show'`.
    """
    def __init__(self, error_value=None, ):
        """
        Initializes the GetmatValueError.

        Args:
            error_value: The invalid value provided for getmat.
        """
        self.value = error_value
        self._error_value_type = type(error_value)
        self.keyWord = "gatmat" 
        self._TraceBack_message = ""
        
        # Initialize base class
        super().__init__(error_value, keyWord=self.keyWord, skip=1)

    def __generate_message__(self):
        """
        Generates the error message, clearly listing the allowed values for `getmat`.

        Returns:
            The complete, formatted error string.
        """
        return  (
                f"{PURPLE}GetMatValueError{RESET}: The `getmat` value must be one of the allowed values: "
                f"{PEACH}True, False, 'true', 'show'{RESET}.\n"
                f"Received: {GRAY}{self.value}{RESET} "
                f"(type: {GRAY}{self._error_value_type.__name__}{RESET})."
        )
