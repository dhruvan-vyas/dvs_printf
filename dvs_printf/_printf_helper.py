
# import importlib
# from os import get_terminal_size
# from re import compile

# chack_styles     = ['typing', 'async'   , 'center', 'glitch', 'silverfade']
# available_styles = ['typing', 'headline', 'async' , 'center', 'centerAL', 'centerAR'  , 
#                     'left'  , 'right'   , 'wave'  , 'fire'  , 'scatter' , 'blink'     ,
#                     'mid'   , 'gunshort', 'snip'  , 'matrix', 'matrix2' , 'silverfade', 
#                     'glitch', 'newsline', 'b2f'   , 'f2b'   , 'help'
#                 ]


# from typing import Optional, Any

# class Modifier:
#     """
#     The Modifier class implements the Singleton pattern and uses __slots__ 
#     for maximum efficiency and minimal memory footprint. 
    
#     It serves as a highly performant global configuration manager.
#     """
    
#     # 1. Efficiency Boost: Using __slots__
#     # This tells Python not to create an instance dictionary (__dict__).
#     # This saves memory and makes attribute access slightly faster.
#     __slots__ = (
#         'style', 'speed', 'delay', 'stay', '_stay', 
#         'maxStrLen', 'color', '_initialized'
#     )

#     # Private class variable for the Singleton instance
#     _instance: Optional['Modifier'] = None

#     # 2. Singleton Enforcement
#     @staticmethod
#     def __new__(self, *args, **kwargs):
#         """Ensures only a single instance of Modifier is ever created."""
#         if self._instance is None:
#             # Create the single instance using the standard object constructor
#             self._instance = super().__new__(self)
#         return self._instance

#     # 3. Lean Initialization
#     def __init__(self):
#         """Initializes attributes only once, during the first call."""
#         # Check if the attributes have been set during the first __new__ run.
#         # This prevents redundant initialization on subsequent calls.
#         if not hasattr(self, '_initialized'):
#             self.style: Optional[Any] = None
#             self.speed: Optional[float] = None
#             self.delay: Optional[float] = None
#             self.stay: Optional[bool] = None
#             self._stay: Optional[str] = None
#             self.maxStrLen: Optional[int] = None
#             self.color: bool = False
#             self._initialized: bool = True

#     # 4. Configuration Method
#     def parameters(self, style: Any, speed: float, delay: float, stay: bool, color: bool = None) -> None:
#         """
#         Sets the core operational parameters of the Modifier instance.
        
#         Args:
#             style (Any): The display style configuration.
#             speed (float): The playback speed.
#             delay (float): The starting delay.
#             stay (bool): If True, a newline ('\\n') is used.
#             maxStrLen (Optional[int]): Maximum string length to process.
#             color (bool): Flag indicating if color is enabled.
#         """
#         # Assigning values directly to the instance's pre-slotted attributes
#         self.style = style
#         self.speed = speed
#         self.delay = delay
#         self.stay = stay
        
#         # Calculate the internal _stay value based on the input 'stay' flag
#         self._stay = "\n" if stay else "\x1b[2K" 
        
#         # self.maxStrLen = maxStrLen
#         if color != None:
#             self.color = color

# modifyed: Modifier = Modifier()



# # ================================================================================
# # map_Funcs = {
# #         "left"    : __left__     ,
# #         "right"   : __right__    ,
# #         "headline": __headline__ ,
# #     }

# # map_import_func = {
# #         "newsline": "__newsline__",
# #         "mid"     : "__mid__"     ,
# #         "gunshort": "__gunshort__",
# #         "snip"    : "__snip__"    ,
# #         "matrix"  : "__matter__"  ,
# #         "matrix2" : "__matter__"  ,
# #         "scatter" : "__matter__"  ,
# #         "blink"   : "__blwafi__"  ,
# #         "wave"    : "__blwafi__"  ,
# #         "fire"    : "__blwafi__"  ,
# #         "f2b"     : "__f2b2f__"   ,
# #         "b2f"     : "__f2b2f__"   ,
# #     }

# # def load_function(func_name):
# #     try:
# #         module=importlib.import_module('dvs_printf.other_styles') # module_file
# #         get_func=getattr(module, map_import_func[func_name])
# #         add_func=map_import_func[func_name]
# #         for k,v in map_import_func.items():
# #             if v==add_func:
# #                 map_Funcs[k]=get_func
# #     except:map_Funcs[func_name]=getattr(module,map_import_func[func_name])
# #     finally:return map_Funcs[func_name]
# # ================================================================================



# pattern = compile(r'[\x00-\x09\x0B-\x1F\x7F-\x9F]')

# def divide_line(string: str, tem_len: int | None = 80) -> list[str]:
#     list_ = []
#     if len(string) >= tem_len:
#         i = 1
#         while i < 10:
#             if string[:tem_len][-i] == " ":
#                 i -= 1
#                 break
#             i += 1
#         else:
#             i = 0
#         list_.append(string[:tem_len - i])
#         list_.extend(divide_line(string[tem_len - i:], tem_len))
#     else:
#         list_.append(string)
#     return list_


# try:
#     tem_len = get_terminal_size()[0] - 2
# except:
#     tem_len = 80

# def list_of_str(values: tuple, getmat: bool | str | None = False):
#     """Generator version of list_of_str."""
#     for value in values:
#         # print("start list_of_str Gen")

#         var_type = type(value)
#         if getmat:
#             try:
#                 getmat = str(getmat).lower()
#                 if "numpy" in str(var_type):
#                     for sublist in value.reshape(-1, value.shape[-1]):
#                         yield str(sublist.tolist())
#                     if "show" in getmat:
#                         yield "<class 'numpy.ndarray' "
#                         yield f" dtype={value.dtype} "
#                         yield f" shape={value.shape}>"

#                 elif "tensorflow" in str(var_type):
#                     from tensorflow import reshape, shape
#                     for sublist in reshape(value, [-1, shape(value)[-1]]):
#                         yield str(sublist.numpy().tolist())
#                     if "show" in getmat:
#                         yield "<class 'Tensorflow' "
#                         yield f" {str(value.dtype).replace('<', '').replace('>', '')} "
#                         yield f" shape: {value.shape}>"

#                 elif "torch" in str(var_type):
#                     for sublist in value.view(-1, value.size(-1)):
#                         yield str(sublist.tolist())
#                     if "show" in getmat:
#                         yield from (
#                                     "<class 'torch.Tensor' ",
#                                 f" dtype={value.dtype} ",
#                                 f" shape={value.shape}>")

#                 elif "pandas" in str(var_type):
#                     for item in value.stack().apply(lambda x: str(x)).tolist():
#                         yield item
#                     if "show" in getmat:
#                         yield "<class 'pandas' "
#                         yield f" shape={value.shape}>"
#                         for dtype in (
#                             str(value.dtypes).replace("\n", "@#$@")
#                             .replace("    ", ": ")
#                             .split("@#$@")
#                         ):
#                             yield dtype

#                 else:
#                     # Log("Entered GetMat", f"{value}")
#                     if isinstance(value, list) and isinstance(value[0], list):
#                         # Log("Entered GetMat", f"{value}")
#                         yield from list_of_str(value, getmat=getmat)

#                     elif isinstance(value, list):
#                         yield str(value).replace("\n", " ")
#                 continue
#             except:
#                 pass

#         if var_type == dict:
#             for key, val in value.items():
#                 for var in f"{key}: {val}".split("\n"):
#                     if len(var) >= tem_len:
#                             yield from divide_line(var, tem_len)
#                     else:   yield var
                                
#         elif var_type in [tuple, list, set]:
#             yield from list_of_str(value, getmat=False)

#         else:
#             if var_type != str:value = str(value)
#             else:value = pattern.sub("", value)
            
#             for vel in value.split("\n"):
#                 if len(vel) >= tem_len:
#                         yield from divide_line(vel, tem_len)
#                 else:   yield vel




# def help() -> None:
#     from os import get_terminal_size
#     from ._printf_helper import modifyed as self
#     from ._core_styles import _async


#     tem_len_line=get_terminal_size()[0]
#     mid_len_line=int(tem_len_line/2 - 9)

#     print(f"\n{'='*tem_len_line}\n"
#             f"{' '*mid_len_line}>>> DVS_PRINTF <<<\n"
#             f"{'='*tem_len_line}"
#         )
    
#     self.parameters("16", .003, 0, "\n", 78)
#     with open('dvs_printf/help.txt', 'r') as file:
#         _async(tuple(file.read().split("\n")))

#     print("="*tem_len_line+"\n")

#     del (_async, self,
#         mid_len_line, 
#         tem_len_line, 
#         get_terminal_size)












"""
UPURPLEity functions and configuration for the main dvs_printf module.

This file contains the global state manager (Modifier), input processing (list_of_str),
terminal geometry calculations, and documentation retrieval.
"""
import importlib
from os import get_terminal_size
from re import compile
from typing import Optional, Any, Tuple, List, Dict, Generator, Iterator
import inspect # For robust asset loading

# Global constants for available styles and validation checks.
# These lists are used by the _validator module.
chack_styles: List[str] = ['typing', 'async'   , 'center', 'glitch', 'silverfade']
available_styles: List[str] = ['typing', 'headline', 'async' , 'center', 'centerAL', 'centerAR'  , 
                    'left'  , 'right'   , 'wave'  , 'fire'  , 'scatter' , 'blink'     ,
                    'mid'   , 'gunshort', 'snip'  , 'matrix', 'matrix2' , 'silverfade', 
                    'glitch', 'newsline', 'b2f'   , 'f2b'   , 'help'
                ]


class Modifier:
    """
    The Modifier class implements the Singleton pattern and uses __slots__ 
    for maximum efficiency and minimal memory footprint. 
    
    It serves as a highly performant global configuration manager used by the 
    core animation functions to read transient settings (speed, style, color state).
    """
    
    # 1. Efficiency Boost: Using __slots__
    __slots__ = (
        'style', 'speed', 'delay', 'stay', '_stay', 
        'maxStrLen', 'color', '_initialized'
    )

    # Private class variable for the Singleton instance
    _instance: Optional['Modifier'] = None

    # 2. Singleton Enforcement
    def __new__(self, *args, **kwargs):
        """Ensures only a single instance of Modifier is ever created."""
        if self._instance is None:
            # Create the single instance using the standard object constructor
            self._instance = super().__new__(self)
        return self._instance

    # 3. Lean Initialization
    def __init__(self):
        """Initializes attributes only once, during the first call."""
        if not hasattr(self, '_initialized'):
            self.style: Optional[Any] = None
            self.speed: Optional[float] = None
            self.delay: Optional[float] = None
            self.stay: Optional[bool] = None
            self._stay: Optional[str] = None
            self.maxStrLen: Optional[int] = None
            self.color: bool = False
            self._initialized: bool = True

    # 4. Configuration Method
    def parameters(self, style: Any, speed: float, delay: float, stay: bool, color: bool = None) -> None:
        """
        Sets the core operational parameters of the Modifier instance.
        
        Args:
            style (Any): The display style configuration.
            speed (float): The playback speed.
            delay (float): The starting delay.
            stay (bool): If True, the output line is preserved; otherwise, it is cleared.
            color (bool): Flag indicating if color is enabled (used for internal animation logic).
        """
        # Assigning values directly to the instance's pre-slotted attributes
        self.style = style
        self.speed = speed
        self.delay = delay
        self.stay = stay
        
        # Calculate the internal _stay value based on the input 'stay' flag
        self._stay = "\n" if stay else "\x1b[2K" 
        
        # self.maxStrLen = maxStrLen # NOTE: This should be set by the calling animation function if needed.
        if color is not None:
            self.color = color

modifyed: Modifier = Modifier() # Instantiate the Singleton globally for external access


# Regular expression to clean control characters from strings
pattern = compile(r'[\x00-\x09\x0B-\x1F\x7F-\x9F]')


def divide_line(string: str, tem_len: int | None = 80) -> list[str]:
    """
    Performs basic word wrapping on a long string to fit the terminal width.
    
    This function splits the string at the nearest space before the terminal length
    is exceeded. It is used internally for text formatting.

    Args:
        string (str): The input string to wrap.
        tem_len (int): The maximum line length (terminal width - padding).

    Returns:
        list[str]: A list of wrapped string segments.
    """
    list_ = []
    if len(string) >= tem_len:
        i = 1
        while i < 10:
            if string[:tem_len][-i] == " ":
                i -= 1
                break
            i += 1
        else:
            i = 0
        list_.append(string[:tem_len - i])
        list_.extend(divide_line(string[tem_len - i:], tem_len))
    else:
        list_.append(string)
    return list_


try:
    # Attempt to determine terminal width, falling back to 80 characters
    tem_len = get_terminal_size()[0] - 2
except:
    tem_len = 80


def list_of_str(values: tuple, getmat: bool | str | None = False) -> Generator[str, None, None]:
    """
    Normalizes complex input values (NumPy arrays, lists, dictionaries) into an 
    iterable stream of strings for the animation functions.

    This is implemented as a generator for memory efficiency.

    Args:
        values (tuple): The positional arguments passed to printf.
        getmat (bool | str, optional): If True or "show", enables formatting for 
                                       complex matrix objects (NumPy, TensorFlow, etc.).

    Yields:
        Generator[str, None, None]: A sequence of strings ready for terminal output.
    """
    for value in values:
        var_type = type(value)
        if getmat:
            try:
                getmat = str(getmat).lower()
                if "numpy" in str(var_type):
                    for sublist in value.reshape(-1, value.shape[-1]):
                        yield str(sublist.tolist())
                    if "show" in getmat:
                        yield "<class 'numpy.ndarray' "
                        yield f" dtype={value.dtype} "
                        yield f" shape={value.shape}>"

                elif "tensorflow" in str(var_type):
                    from tensorflow import reshape, shape
                    for sublist in reshape(value, [-1, shape(value)[-1]]):
                        yield str(sublist.numpy().tolist())
                    if "show" in getmat:
                        yield "<class 'Tensorflow' "
                        yield f" {str(value.dtype).replace('<', '').replace('>', '')} "
                        yield f" shape: {value.shape}>"

                elif "torch" in str(var_type):
                    for sublist in value.view(-1, value.size(-1)):
                        yield str(sublist.tolist())
                    if "show" in getmat:
                        yield from (
                                    "<class 'torch.Tensor' ",
                                f" dtype={value.dtype} ",
                                f" shape={value.shape}>")

                elif "pandas" in str(var_type):
                    for item in value.stack().apply(lambda x: str(x)).tolist():
                        yield item
                    if "show" in getmat:
                        yield "<class 'pandas' "
                        yield f" shape={value.shape}>"
                        for dtype in (
                            str(value.dtypes).replace("\n", "@#$@")
                            .replace("    ", ": ")
                            .split("@#$@")
                        ):
                            yield dtype

                else:
                    # Log("Entered GetMat", f"{value}")
                    if isinstance(value, list) and isinstance(value[0], list):
                        # Log("Entered GetMat", f"{value}")
                        yield from list_of_str(value, getmat=getmat)

                    elif isinstance(value, list):
                        str_value = str(value).replace("\n", " ")    

                        if len(str_value) >= tem_len:
                                yield from divide_line(str_value, tem_len)
                        else:   yield str_value

                        # yield str(value).replace("\n", " ")

                continue
            except:
                pass

        if var_type == dict:
            for key, val in value.items():
                for var in f"{key}: {val}".split("\n"):
                    if len(var) >= tem_len:
                            yield from divide_line(var, tem_len)
                    else:   yield var
                                
        elif var_type in [tuple, list, set]:
            yield from list_of_str(value, getmat=False)

        else:
            if var_type != str:value = str(value)
            else:value = pattern.sub("", value)
            
            for vel in value.split("\n"):
                if len(vel) >= tem_len:
                        yield from divide_line(vel, tem_len)
                else:   yield vel

def help() -> None:
    """
    Prints the comprehensive help documentation for the dvs_printf module to the console.

    The help content is read from an external file (`help.txt`) and is displayed
    with an animated effect (using the '_async' style and centered layout).
    """
    from ._core_styles import _async
    from os import get_terminal_size
    from ._printf_helper import modifyed as self
    from .colors.ansi import Font_Styles, RESET

    tem_len_line = get_terminal_size()[0]
    mid_len_line = int(tem_len_line/2 - 9)

    print(f"\n{'='*tem_len_line}\n"
            f"{' '*mid_len_line}{Font_Styles.BOLD}>>> DVS_PRINTF <<<{RESET}\n"
            f"{'='*tem_len_line}"
        )
    
    # Configure the modifier for the help animation
    self.parameters("center", .002, 0, True, True)
    self.maxStrLen = tem_len_line - 4

    help_content_text = inspect.cleandoc(f"""
        {Font_Styles.BOLD}High-Performance Animated Console Engine{RESET}
        
        {Font_Styles.ITALIC}A powerful, optimized replacement for Python's print().{RESET}

        {Font_Styles.BOLD}1. CORE ANIMATIONS{RESET}
           - typing  : Character-by-character typewriter effect.
           - glitch  : Realistic digital distortion and electronic noise.
           - matrix  : Iconic falling green code streams.
           - newsline: Professional scrolling ticker-tape bracketed animation.
           - snip/gunshort: Motion-based character-firing effects.

        {Font_Styles.BOLD}2. TRUECOLOR ENGINE{RESET}
           - Full 24-bit RGB, HEX, HSL, and 345+ named colors support.
           - Angular gradients with per-degree precision.

        {Font_Styles.BOLD}3. LOADERS & SPINNERS{RESET}
           - LoadingBar: Multi-threaded progress tracking with I/O suppression.
           - Spinner: 40+ unique frame styles for background tasks.

        {Font_Styles.BOLD}4. INTELLIGENT DEBUGGING{RESET}
           - Fancy Tracebacks: AST-based arg highlighting for fast debugging.

        {Font_Styles.BOLD}5. DOCUMENTATION & LINKS{RESET}
           - GitHub: https://github.com/dhruvan-vyas/dvs_printf
           - PyPI  : https://pypi.org/project/dvs-printf/
           - Docs  : Check the /READMES folder for module-specific deep dives.
        """)
    
    _async(tuple(help_content_text.split("\n")))

    print("="*tem_len_line+"\n")

    del (
        mid_len_line, 
        tem_len_line, 
        get_terminal_size)
