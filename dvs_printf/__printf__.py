"""
The core animation execution module for dvs_printf.

This file defines the public `printf` API function. Its responsibilities include:
1. Input validation (style, speed, color, etc.).
2. Dynamic speed calculation based on style and user input.
3. Applying complex color/gradient configurations via the Colors class.
4. Dynamically loading (lazy importing) required animation functions (like matrix or wave).
5. Executing the chosen animation style.
"""

import importlib

from typing import Callable
from .console import _write, _flush, print_args_2 as print2ln
from ._printf_helper import list_of_str, help, Modifier, modifyed
from .colors         import Colors, Font_Styles
from .exceptions     import dvs_BaseException
from ._validator     import *
from ._core_styles   import (
    _typing,
    _center,
    _async ,
    _left  ,
    _right ,
    _headline,    
)

# numpy.amin

map_Funcs = {
        "left"    : _left     ,
        "right"   : _right    ,
        "headline": _headline ,
    }

# =======================================================================
map_import_func = {
        "newsline": "_newsline",
        "mid"     : "_mid"     ,
        "gunshort": "_gunshort",
        "snip"    : "_snip"    ,
        "matrix"  : "_matter"  ,
        "matrix2" : "_matter"  ,
        "scatter" : "_matter"  ,
        "blink"   : "_blwafi"  ,
        "wave"    : "_blwafi"  ,
        "fire"    : "_blwafi"  ,
        "f2b"     : "_f2b2f"   ,
        "b2f"     : "_b2f2f"   ,
        "glitch"  : "_glitch"  ,
     "silverfade" : "_silver_fade",
    }

def load_function(func_name: str) -> Callable:
    """
    Dynamically imports an animation function from the _other_styles module and caches it.

    This function implements a lazy-loading strategy to only load specific, 
    potentially large animation functions (like matrix, wave, glitch) when they are 
    explicitly requested, saving memory at startup.

    Args:
        func_name (str): The requested style name (e.g., 'glitch', 'matrix').

    Returns:
        Callable: The imported function object for the animation style.

    Raises:
        ImportError: If the module or function cannot be found.
    """
    for name in ['glitch','silverfade']:
        if name in func_name:
            func_name = name
            break
    try: 
        module=importlib.import_module('dvs_printf._other_styles')
        get_func=getattr(module, map_import_func[func_name])
        add_func=map_import_func[func_name]

        for k,v in map_import_func.items():
            if v==add_func:
                map_Funcs[k]=get_func
    except: 
        # Fallback in case module import or attribute fetching failed the first time
        map_Funcs[func_name]=getattr(module,map_import_func[func_name])
    finally: return map_Funcs[func_name]
# =======================================================================

speed_key = {
    'typing'   : .08 ,
    'headline' : .08 ,
    'center'   : .08 ,
    'right'    : .032,
    'left'     : .032,
    'async'    : .045,
    'gunshort' : .064,
    'snip'     : .016,
    'scatter'  : .3  ,
    'newsline' : .18 ,
} 

def printf(
    *values: object, 
    style : str|         None = 'typing' ,
    speed : int| float | None = 3        ,
    delay : int| float | None = 0        ,
    stay  :      bool  | None = True     ,
    getmat: str| bool  | None = False    ,
    attrs : list[str]  = [],
    color:            tuple[str|tuple] | None = None,
    backgroung_color: tuple[str|tuple] | None = None,
    reset_color: bool | None = True,
    **kwargs
    )  ->   None:
    """
    The main public API function for animated terminal output.

    Processes, validates, and animates input values using the specified style, 
    speed, and color configuration.

    Args:
        *values (object): Positional arguments (strings, lists, arrays) to be animated.
        style (str, optional): The animation style to use (e.g., 'typing', 'glitch'). 
                               Can be 'help' to display help documentation.
        speed (int | float, optional): Speed multiplier (1-6) or explicit duration (7).
        delay (int | float, optional): Delay between animated lines.
        stay (bool, optional): If True, keeps the final output visible; otherwise, clears it.
        getmat (str | bool, optional): Enables/configures complex array formatting (e.g., NumPy).
        attrs (list[str], optional): List of text attributes (e.g., 'bold', 'italic').
        color (tuple | str, optional): Foreground color or color gradient configuration.
        backgroung_color (tuple | str, optional): Background color or gradient configuration.
        **kwargs: Internal keyword arguments (like _validated_kwargs) or those used by the Init class.

    Returns:
        None: This function primarily produces output to the console.

    Raises:
        dvs_BaseException: For any validation error (e.g., invalid style, speed, color format).
    """

    style=str(style).lower()
    if values==(): return 
    elif style=="help": return help()
    
    # --- 1. Validation ---
    elif not kwargs.get("_validated_kwargs"):          
        if style  != 'typing': _validate_style (style )
        if speed  != 3       : _validate_speed (speed )
        if delay  != 0       : _validate_delay (delay )
        if attrs  != []      : _validate_attrs (attrs )
        if getmat != False   : _validate_getmat(getmat)

    # --- 2. Input and Color Processing ---
    values = list_of_str(values, getmat=getmat)
    if (color or backgroung_color) and "silverfade" not in style:
        if  (   type(color).__name__ == "Colors" 
             or kwargs.get("_validated_colors", False)
        ):      values = color.apply(values, reset=reset_color) 
        else:   values = Colors(color, 
                                background=backgroung_color
                            ).apply(values, reset=reset_color)
        modifyed.color = True # Set modifier flag for colored output
            
    # --- 3. Speed Calculation ---
    try: 
        if    speed == 7: speed = 0.003
        else: speed = round(speed_key.get(style, .16) / (
                    speed if speed >= 1 and speed <= 6 else 3 
                ), 3)    
    except: speed = .028

    delay=abs(delay)
    
    # --- 4. Configuration and Execution ---
    _attrs, _attrs_reset = Font_Styles.get(attrs)

    try:
        # Update the global modifier state for the chosen animation
        modifyed.parameters(style, speed, delay, stay)

        print2ln(_attrs, end='\033[?25l') # Apply attributes and hide cursor

        # Execute the correct animation function (Dynamic Dispatch)
        if   "typing" in style:_typing(values)
        elif "center" in style:_center(values)
        elif "async"  in style:_async (values)
        elif  style   in map_Funcs:map_Funcs[style](values) # Core styles (left, right, headline)
        else: load_function(style)(values) # Dynamically loaded styles

    except dvs_BaseException:
        raise

    except Exception as E:
        raise dvs_BaseException(message=E)

    finally:
        print2ln(_attrs_reset, end='\033[?25h') # Reset attributes and show cursor

        # Clean up local variables to free memory
        del values, style, speed, delay, stay, color, _attrs, _attrs_reset
