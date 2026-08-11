# from re              import escape, search
# from ._base_exception import dvs_BaseException
# from ._colored_vars  import PURPLE, RESET, GRAY, PURPLE


# class ColorsValueError(dvs_BaseException):
#     def __init__(self, error_value=None, message: str = None, ):
#         self.value = error_value
#         self._error_value_type = type(error_value)
#         self.keyWord = "Colors"
#         self._message = message or (  
#             f"The 'init.colors' only accepts an instance of "
#             f"<class '{PURPLE}Color{RESET}'>. Received: {GRAY}{self.value}{RESET} "
#             f"(type: {GRAY}{type(error_value).__name__}{RESET})."
#         )
#         self._int = 0
#         super().__init__(error_value, keyWord=self.keyWord)

#     def __generate_message__(self) -> str:
#         return ( # An unknown error occurred with value: 
#             f"{PURPLE}ColorsValueError{RESET}: {self._message}"
#         )

#     def find_argument_match(self, line: str):
#         """
#         Unified robust match for ColorsValueError:
#         - Handles: 
#         color = "red"
#         color = 123
#         color = (123, 255, 0)
#         color = ("red", "#abc", (120,150,200))
#         color = ["red", "#abc", (120,150,200)]
#         - Uses multi-pattern fallback:
#         1) container pattern
#         2) kw=value with error embedded
#         3) raw error fallback
#         """
#         kw = self.keyWord or ''
#         err = self.value
#         val = str(err).strip()
#         # Always normalize to string
#         err_str = str(err).strip()

#         # 1️⃣ Container: color = [ ... ] or color = ( ... )
#         # container = self.balanced_arg_span(line)

#         for key  in ['color', 'Colors', 'background']:
#             container = self.balanced_arg_span(line, key=key)
#             if container and val in container:
#                 return search(escape(val), container)

#         container = self.balanced_arg_span(line)

#         if container:
#             match = search(escape(container.strip()), line)
#             if match:
#                 return match
                
#         match = search(
#             rf'\b{kw}s?\s*=\s*(\[[^\]]*\]|\([^\)]*\))',
#             line
#         )
#         if match:
#             return match

#         # 2️⃣ Scalar or literal: try to find exact value embedded
#         if isinstance(err, str):
#             # print("val == str")
#             val = err.strip('"').strip("'")
#             err_pattern = (
#                 rf'\b{kw}s?\s*=\s*(?:'
#                 rf'"([^"]*{val}[^"]*)"|'
#                 rf"'([^']*{val}[^']*)'|"
#                 rf'([^\s,)\]]*{val}[^\s,)\]]*)'
#                 r')'
#             )
#         else:
#             # print("Else")
#             val = err_str
#             err_pattern = (
#                 rf'\b{kw}s?\s*=\s*(?:'
#                 rf'"([^"]*{val}[^"]*)"|'
#                 rf"'([^']*{val}[^']*)'|"
#                 rf'([^\s,)\]]*{val}[^\s,)\]]*)'
#                 r')'
#             )

#         match = (
#                search(err_pattern, line)
#             or search(rf'\b{kw}s?\s*=\s*(\[[^\]]*\]|\([^\)]*\))',
#                     line
#                 )
#         )
#         if match:
#             return match

#         # 3️⃣ Fallback: raw error value anywhere
#         return search(escape(val), line)

#     def balanced_arg_span(self, line: str, key=None):
#         """
#         Finds kw = ... with balanced brackets.
#         """
#         kw: str = key or self.keyWord
#         m = search(rf'\b{kw}s?\s*=', line)
#         if not m:
#             return None

#         pos = m.end()
#         while pos < len(line) and line[pos] in "=": # was " =" (1 space befor only)
#             pos += 1

#         opener = line[pos]
#         if opener not in "([\"'":
#             # Scalar fallback: grab up to next comma or )
#             end = line.find(",", pos)
#             if end == -1:
#                 end = line.find(")", pos)
#             if end == -1:
#                 end = len(line)
#             return line[m.start():end].strip()

#         if opener in "\"'":
#             # String literal
#             quote = opener
#             end = pos + 1
#             while end < len(line) and line[end] != quote:
#                 end += 1
#             return line[m.start():end+1].strip()

#         # Balanced bracket scan
#         pairs = {"(": ")", "[": "]"}
#         closer = pairs[opener]
#         depth = 1
#         end = pos + 1

#         while end < len(line) and depth:
#             c = line[end]
#             if c == opener:
#                 depth += 1
#             elif c == closer:
#                 depth -= 1
#             end += 1

#         return line[m.start():end].strip() if depth == 0 else None
    







# from re import escape, search
# import ast # Need to import ast for type hinting the node
# from typing import Optional, Tuple

# # Assuming these imports are correctly defined elsewhere
# from ._base_exception import dvs_BaseException
# from ._colored_vars  import PURPLE, RESET, GRAY, PURPLE 


# class ColorsValueError(dvs_BaseException):
#     """
#     Exception raised when an invalid color value is passed to a function.
    
#     This class customizes the argument matching to check for 'color', 'Colors', 
#     or 'background' as the keyword argument that caused the error.
#     """
#     def __init__(self, error_value=None, message: str = None, ):
#         self.value = error_value
#         self._error_value_type = type(error_value)
        
#         # Setting a default keyword for the base class fallback logic
#         self.keyWord = "Colors" 
#         print('message:', message)
#         self._message = message or (  
#             f"The 'init.colors' only accepts an instance of "
#             f"<class '{PURPLE}Color{RESET}'>. Received: {GRAY}{self.value}{RESET} "
#             f"(type: {GRAY}{type(error_value).__name__}{RESET})."
#         )
#         self._int = 0
        
#         super().__init__(error_value, keyWord=self.keyWord)

#     def __generate_message__(self) -> str:
#         print('M',self._message)
#         return ( 
#             f"{PURPLE}ColorsValueError{RESET}: {self._message}"
#         )

#     def find_argument_match(self, node: ast.Call, lines, start_lineno) -> Optional[Tuple[int, int, int]]:
#         """
#         Overrides the base method to check for multiple possible keyword argument names 
#         ('color', 'Colors', 'background') in the AST node.
        
#         Returns a tuple of (lineno, col_offset, length) if a match is found.
#         """
#         if node is None:
#             return None
            
#         # The list of keywords this exception should target
#         color_keywords = ['color', 'Colors', 'background']
        
#         # 1. Check for a matching keyword argument in the AST node
#         for kw in node.keywords:
#             if kw.arg in color_keywords:
#                 # We found the keyword that maps to this color exception.
#                 val = kw.value
                
#                 # Ensure all necessary attributes for span calculation exist
#                 if (hasattr(kw, 'lineno') and hasattr(kw, 'col_offset') and 
#                     hasattr(val, 'end_col_offset')):
                    
#                     start_col = kw.col_offset
#                     # Calculate length from the start of the keyword name (e.g., 'color') 
#                     # to the end of the argument value (e.g., '8"' in color="8").
#                     length = val.end_col_offset - kw.col_offset
                    
#                     return (kw.lineno, start_col, length)
        
#         # 2. Fallback to the base class logic for positional argument checks 
#         # or other general fallbacks (like highlighting the function name).
#         return super().find_argument_match(node, lines, start_lineno)

# # Removed the string-parsing 'balanced_arg_span' as it's not needed with AST















# from re import escape, search
# import ast # Need to import ast for type hinting the node
# from typing import Optional, Tuple, List

# # Assuming these imports are correctly defined elsewhere
# from ._base_exception import dvs_BaseException
# from ._colored_vars  import PURPLE, RESET, GRAY, PURPLE 


# class ColorsValueError(dvs_BaseException):
#     """
#     Exception raised when an invalid color value is passed to a function.
    
#     This class customizes the argument matching to check for 'color', 'Colors', 
#     or 'background' as the keyword argument that caused the error.
#     """
#     def __init__(self, error_value=None, message: str = None, ):
#         self.value = error_value
#         self._error_value_type = type(error_value)
        
#         # Setting a default keyword for the base class fallback logic
#         self.keyWord = "Colors" 
        
#         # 1. Calculate and store the message in the derived class
#         # (Using the provided message, or the custom default message)
#         self._message = message or (  
#             f"The 'init.colors' only accepts an instance of "
#             f"<class '{PURPLE}Color{RESET}'>. Received: {GRAY}{self.value}{RESET} "
#             f"(type: {GRAY}{type(error_value).__name__}{RESET})."
#         )
#         self._int = 0
        
#         # 2. FIX: Pass the calculated self._message to the base class's 'message' parameter.
#         # This ensures the base class initializes its internal state with the correct message.
#         super().__init__(error_value, message=self._message, keyWord=self.keyWord)

#     def __generate_message__(self) -> str:
#         # This method uses the corrected self._message, which is now properly set 
#         # in the base class's internal state.
#         return ( 
#             f"{PURPLE}ColorsValueError{RESET}: {self._message}"
#         )

#     def find_argument_match(self, node: ast.Call, full_lines: List[str], start_lineno: int) -> Optional[Tuple[int, int, int]]:
#         """
#         Overrides the base method to check for multiple possible keyword argument names 
#         ('color', 'Colors', 'background') in the AST node.
        
#         Returns a tuple of (lineno, col_offset, length) if a match is found.
#         """
#         if node is None:
#             # Fall back to base class's string search if no AST node is found
#             return super().find_argument_match(node, full_lines, start_lineno)
            
#         color_keywords = ['color', 'Colors', 'background']
        
#         # 1. Check for a matching keyword argument in the AST node
#         for kw in node.keywords:
#             if kw.arg in color_keywords:
#                 val = kw.value
                
#                 if (hasattr(kw, 'lineno') and hasattr(kw, 'col_offset') and 
#                     hasattr(val, 'end_col_offset')):
                    
#                     start_col = kw.col_offset
#                     length = val.end_col_offset - kw.col_offset
                    
#                     return (kw.lineno, start_col, length)
        
#         # 2. Fallback to the base class logic (positional arguments, string search, etc.)
#         return super().find_argument_match(node, full_lines, start_lineno)






from re import escape, search
import ast # Need to import ast for type hinting the node
from typing import Optional, Tuple, List

# Assuming these imports are correctly defined elsewhere
from ._base_exception import dvs_BaseException
from ._colored_vars  import PURPLE, RESET, GRAY, PURPLE


class ColorsValueError(dvs_BaseException, ValueError):
    """
    Exception raised when an invalid or improperly typed color value is passed to a function.
    
    This class extends `dvs_BaseException` by customizing argument matching to 
    specifically target parameters related to color, such as **'color'**, 
    **'Colors'**, or **'background'**, for precise traceback highlighting.
    """
    def __init__(self, error_value=None, message: str = None, ):
        """
        Initializes the color validation exception.

        It sets a custom default error message if none is provided, specifically 
        informing the user that the value must be a `Color` instance. It then 
        passes the calculated message to the base class for traceback generation.

        Args:
            error_value: The invalid value that caused the error.
            message: An optional custom error message string.
        """
        self.value = error_value
        self._error_value_type = type(error_value)
        
        # Setting a default keyword for the base class fallback logic
        self.keyWord = "Colors" 
        
        # 1. Calculate and store the message in the derived class
        self._message = message or (  
            f"The 'init.colors' only accepts an instance of "
            f"<class '{PURPLE}Color{RESET}'>. Received: {GRAY}{self.value}{RESET} "
            f"(type: {GRAY}{type(error_value).__name__}{RESET})."
        )
        self._int = 0
        
        # 2. Pass the calculated self._message to the base class's 'message' parameter.
        super().__init__(error_value, message=self._message, keyWord=self.keyWord)

    def __generate_message__(self) -> str:
        """
        Overrides the base class method to provide the final, formatted exception 
        message, prepended with the specific exception title: `ColorsValueError`.
        
        Returns:
            The complete, formatted exception message string.
        """
        return ( 
            f"{PURPLE}ColorsValueError{RESET}: {self._message}"
        )

    def find_argument_match(self, node: ast.Call, full_lines: List[str], start_lineno: int) -> Optional[Tuple[int, int, int]]:
        """
        Overrides the base method to implement specialized argument searching. 
        
        It iterates over the AST call node's keyword arguments, specifically 
        looking for keys in the hardcoded list: 'color', 'Colors', or 'background'. 
        If a match is found, it calculates the precise span for highlighting the 
        invalid input in the source code. If no match is found, it delegates 
        to the base class's matching logic.

        Args:
            node: The `ast.Call` node representing the function invocation.
            full_lines: All source lines of the function call.
            start_lineno: The absolute line number where the function call starts.

        Returns:
            A tuple of (absolute_lineno, col_offset, length) for the highlight span, 
            or None if no match is found.
        """
        if node is None:
            # Fall back to base class's string search if no AST node is found
            return super().find_argument_match(node, full_lines, start_lineno)
            
        # The list of keywords this exception should target
        color_keywords = ['color', 'Colors', 'background']
        
        # 1. Check for a matching keyword argument in the AST node
        for kw in node.keywords:
            if kw.arg in color_keywords:
                val = kw.value
                
                if (hasattr(kw, 'lineno') and hasattr(kw, 'col_offset') and 
                    hasattr(val, 'end_col_offset')):
                    
                    start_col = kw.col_offset
                    length = val.end_col_offset - kw.col_offset
                    
                    return (kw.lineno, start_col, length)
        
        # 2. Fallback to the base class logic (positional arguments, string search, etc.)
        return super().find_argument_match(node, full_lines, start_lineno)
