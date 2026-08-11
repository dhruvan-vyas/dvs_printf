import os
from threading  import Thread
from typing     import Callable, Tuple
from sys        import stdout
from ..colors   import rgb_to_ansi_func, rgb_to_bg_ansi_func
from ..colors   import get_RGB_values


def color_function(name):
    return rgb_to_ansi_func(
        *get_RGB_values(name)
    )

def bg_color_function(name):
    return rgb_to_bg_ansi_func(
        *get_RGB_values(name)
    )   

def println(text=""):
    """Prints text to stdout without a newline."""
    stdout.write(text)
    stdout.flush()


def get_dedicated_console_writer() -> Tuple[Callable[[str], None], Callable[[], None]]:
    """
    Creates and returns dedicated write and flush functions for direct console output.
    """
    try:
        dedicated_fd = os.dup(1)
        dedicated_stream = os.fdopen(dedicated_fd, 'w', encoding='utf-8', errors='replace')
        return dedicated_stream.write, dedicated_stream.flush
    except Exception:
        return stdout.write, stdout.flush

# Get our dedicated print functions at the start of the program.
_write, _flush = get_dedicated_console_writer()



class ProgressUpdater:
    """A simple object for the user to update the progress."""
    def __init__(self):
        self._value = 0.0

    def set_progress(self, value: float):
        """Sets the progress value (0.0 to 100.0)."""
        self._value = max(0.0, min(100.0, value))

    
    def update(self, value: float):
        """Sets the progress value (0.0 to 100.0)."""
        self._value = max(0.0, min(100.0, value))
        
    @property
    def value(self):
        return self._value

    def __add__(self, value: float):
        self._value += value

    def __sub__(self, value: float):
        self._value -= value

class MyThread(Thread):
    """
    A Thread subclass that stores the result of its target function.
    """
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs or {}
        self.result = None
        self._exception = None

    def run(self):
        try:
            # The _target and its arguments are stored on the thread instance.
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self._exception = e
        finally:
            del self._target, self._args, self._kwargs

