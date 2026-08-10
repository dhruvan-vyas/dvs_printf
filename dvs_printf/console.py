from sys          import stdout
from .colors.ansi import console_EnvType

_write = stdout.write
_flush = stdout.flush


def get_print_function(args=1, color=None): # font_style:str=None
    '''
    return the print function. 
    - print<...>    : for non Colored text, not using ''.join 
        - print_args
        - print_join
        - println
    - Co_print<...> : for Colored text, using ''.join 
        - Co_print_args
        - Co_print_join
        - Co_println
    '''
    if   args==1: return println      if not color else Co_println
    elif args==2: return print_args_2 if not color else Co_print_args_2
    else:         return print_args_3 if not color else Co_print_args_3


# prints without join for non colored text 
def println(text=''):
    """prints simple text: (text)"""
    _write(text)
    _flush()

def print_args_2(text, end=''):
    """prints two args: (text + end=('\\n' or any))"""
    _write(text+end)
    _flush()

def print_args_3(frent='', text='', end=''):
    """prints three args: (frent + text + end)"""
    _write(f"{frent}{text}{end}")
    _flush()


# prints with join for colored text
def Co_println(text=''):
    """prints simple text: ''.join(text)"""
    _write(''.join(text))
    _flush()

def Co_print_args_2(text='', end=''):
    """prints two args: (''.join(text) + end='' or any)"""
    _write(''.join(text)+end)
    _flush()

def Co_print_args_3(frent='', text='', end=''):
    _write(f"{frent}{''.join(text)}{end}")
    _flush()



