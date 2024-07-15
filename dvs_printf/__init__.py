"""
[dvs_printf](https://github.com/dhruvan-vyas/dvs_printf) module. A simple and dynamic pritning animation function for python.

Using printf function of this modyul you to create nice & clean printing animation in \\
terminal-based python project.suport any Data type. IF `list, set, tuple, dict` \\
is given Then the output animation work with each items. 

---
### Module include functions
+ [printf](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#printf-function): the core of the module. use to create animation
+ [init](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#dvs_printfinit-method): A dynamic initializer for printf that allows users to preset parameters
+ [showLoading](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#showLoading-function): create Loading bar with backgrond function runner
+ [list_of_str](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#list_of_str): An additional function used by printf to create list[str] based on input values.
"""

__all__ = ("init", "printf", "list_of_str", "showLoading") 
__version__ = '2.2'
__author__  = 'Dhruvan Vyas'

from .__printf__ import printf, list_of_str
from .__init import init
from .__Loading import showLoading


