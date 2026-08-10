"""
[dvs_printf](https://github.com/dhruvan-vyas/dvs_printf) module. A simple and dynamic pritning animation function for python.

Using printf function of this modyul you to create nice & clean printing animation in \\
terminal-based python project.suport any Data type. IF `list, set, tuple, dict` \\
is given Then the output animation work with each items. 

---
### Module include functions
- [printf](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#printf-function): the core of the module. use to create animation
- [init](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#dvs_printfinit-method): A dynamic initializer for printf that allows users to preset parameters
- [showLoading](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#showLoading-function): create Loading bar with backgrond function runner
- [list_of_str](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#list_of_str): An additional function used by printf to create list[str] based on input values.
"""


# https://vscode.dev/github/dhruvan-vyas/dvs_printf3_final/blob/main/test_load.py, line 713


__all__ = (
    "Init", "init", "printf", "list_of_str",

    'ProgressUpdater',
    'ShowLoading', 
    'showLoading',
    'LoadingBar',
    'LoadingBarConfig',
    'LoaderFrems',
    'LoaderValueError',
    'LoaderAttributeError',
    'Spinner', 
    'SpinnerConfig' , 
    'SpinnerFrems',
    'SpinnerValueError',
    'SpinnerAttributeError',

    'console_EnvType',

    'Colors', 
    'Font_Styles',
    'GradientStyles', 

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

) 

print("\n\n Wellcome to dvs_printf -e \n\n")
__version__ = '3.1.0'
__author__  = 'Dhruvan Vyas'

from .__printf__ import printf, list_of_str
from .__init     import Init, init
from .colors     import *
from .loaders    import *
from .exceptions import *
from .console import console_EnvType
from . import colors,loaders, exceptions 

