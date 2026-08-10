# import difflib
from ._colored_vars  import *
from ._base_exception import dvs_BaseException

import difflib
# from re import escape, search
from typing import Optional, Tuple, List, TYPE_CHECKING
from ._colored_vars  import PURPLE, RESET, GRAY, PURPLE, PEACH

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

# class SpinnerValueError(dvs_BaseException, ValueError):
#     def __init__(self, error_value = '', keyWord = "target"):
#         super().__init__(error_value, keyWord=self.keyWord, skip=2)
    
#     def __generate_message__(self):
#         return (
#                 f"{PURPLE}SpinnerValueError{RESET}: The speed value must be of type {GRAY}int{RESET} or {GRAY}float{RESET}, "
#                 f"and a value between {PEACH}1{RESET} to {PEACH}6{RESET}, or exactly {PEACH}7{RESET}. \n"
#                 f"{PURPLE}Received{RESET}: {GRAY}{self.value}{RESET}, type: {GRAY}{self._error_value_type.__name__}{RESET}."
#             )

"""
Custom exception for all validation errors and specific runtime issues 
encountered within the Spinner module.
"""
from typing import Optional
from ._base_exception import dvs_BaseException
# Assuming color placeholders (til, RESET, GRAY, TITLE) are imported from ._colored_vars

class SpinnerValueError(dvs_BaseException, ValueError):
    """
    Exception raised when an invalid value is supplied during the configuration 
    or execution of the LoadingBar.

    This exception is generic for configuration issues (style, color, dimension, etc.)
    and uses the `keyWord` property to enable precise argument highlighting in the traceback.
    """
    def __init__(self, error_value: object, message: Optional[str] = None, keyWord: str = "config"):
        """
        Initializes the SpinnerValueError.

        Args:
            error_value (object): The problematic value that failed validation.
            message (Optional[str]): A specific, detailed error message. If None, a generic 
                                     message including the keyword and received value is generated.
            keyWord (str): The keyword argument that failed validation (e.g., 'style', 'timeout', 
                           'bar_color'). Defaults to 'config'.
        """
        # Set the keyWord first so the base class uses it immediately for the traceback.
        self.keyWord = keyWord
        
        # We pass the message up to the parent, but use the setter logic for the message.
        super().__init__(error_value, message=message, keyWord=self.keyWord)

    def __generate_message__(self) -> str:
        """
        Generates the detailed error message if a custom one was not provided.
        """
        # Use placeholders for color formatting (assuming imports from _colored_vars)
    
        if self._message:
            return f"{PURPLE}SpinnerValueError{RESET}: {self._message}"
        else:
            return (
                f"{PURPLE}SpinnerValueError{RESET}: Invalid value encountered during Spinner configuration or runtime. \n"
                f"{PURPLE}Received{RESET}: {GRAY}{self.value!r}{RESET} (type: {GRAY}{self._error_value_type.__name__}{RESET})."
            )



class SpinnerAttributeError(dvs_BaseException, AttributeError):
    """
    Exception raised when an attribute or parameter is supplied with an 
    incorrect type (e.g., passing a string where a list is expected) 
    during LoadingBar configuration.

    It inherits from both dvs_BaseException (for custom traceback) and 
    AttributeError (for Python type hierarchy).
    """
    def __init__(self, error_value: object, expected_type: str, keyWord: str):
        """
        Initializes the SpinnerAttributeError.

        Args:
            error_value (object): The problematic value received.
            expected_type (str): A string describing the type that was expected 
                                 (e.g., 'int | float', 'list[str]').
            keyWord (str): The keyword argument that received the invalid type.
        """
        self.keyWord = keyWord
        self.expected_type = expected_type
        
        # We generate a descriptive message here to pass to the parent class.
        message = self.__generate_message__()
        super().__init__(error_value, message=message, keyWord=self.keyWord)

    def __generate_message__(self) -> str:
        """
        Generates the detailed error message indicating the expected vs. received types.
        """
        # Use placeholders for color formatting (assuming imports from _colored_vars)
        received_type_name = self._error_value_type.__name__

        # f"{PEACH}Tip{RESET}: Ensure '{self.keyWord}' is passed as a {self.expected_type}."
        
        return (
            f"{PURPLE}SpinnerAttributeError{RESET}: Invalid type for configuration keyword: {PEACH}{self.keyWord}{RESET}.\n"
            f"{PURPLE}Received{RESET} (type {received_type_name}): {GRAY}{self.value!r}{RESET}, {PURPLE}Expected{RESET}: {GRAY}{self.expected_type}{RESET}\n"
        )
