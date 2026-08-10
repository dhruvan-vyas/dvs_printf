"""
The core module for the Spinner system.

Contains the Spinner class, which manages threading, console I/O suppression, 
dynamic animation execution, and state management for showing a spinning 
progress indicator while a target function runs in the background.
"""

import sys, os, io
from time        import time , sleep
from threading   import Thread, Event
from functools   import wraps
from typing      import Callable, Any, Iterable, Mapping, Optional, Union, Tuple, List, Dict

# custom imports (Assuming these are accessible via relative imports)
from .spinner_config import  ColorInput, GredinatInput, SpinnerConfig
from .spinner_frems  import  Get_SPINNERS, SpinnerFrems
from .system_tools   import  color_function, MyThread, ProgressUpdater, _write, _flush
from ..exceptions    import (dvs_BaseException,
                             TimeOutError, 
                             SpinnerValueError, 
                             SpinnerAttributeError, 
                             PEACH, RESET)
from ..colors.colors import  Colors, ColorSequence, Log, ColorInput
from ..colors.ansi   import (Font_Styles, 
        RESET_BACKGROUND as RESET_FG, 
        RESET_FOREGROUND as RESET_BG,
    )

RESET = RESET_FG + RESET_BG


def ShowSpinner(
        target: Optional[Callable],
        args: Iterable[Any],
        kwargs: Optional[Mapping[str, Any]],
        timeout: Optional[int] = 80,
        daemon: Optional[bool] = None,
        name: Optional[str] = None,
        *,
        inject_progress:        bool = False,
        style:  SpinnerFrems | str  = "arrow",
        animation_position:     str  = "before",

        # Messages,
        title:      str  = "Loading",
        attrs: list[str] = [],
        final_message: Optional[str] = None,
        error_message: Optional[str] = None,

        # Other settings,
        stay:           bool = True,
        show_progress:  bool = True,
        show_timer:     bool = True,
        reversed_timer: bool = False,

        # Colors linked to messages/elements,
        spinner_color:       Colors | ColorInput | ColorSequence  = None,
        title_color:         Colors | ColorInput | ColorSequence  = None,
        final_message_color: Colors | ColorInput = "springgreen",
        error_message_color: Colors | ColorInput = "scarlet",
        timer_color:         Colors | ColorInput = "pink",
        progress_color:      Colors | ColorInput = "gray",
        config: Optional[Mapping] = None,
    ) -> Any:
    """
    Convenience function to initialize and run the Spinner animation immediately.

    This function collects all provided arguments, configures the Spinner class, 
    and executes the `run` method to start the background process.

    Args:
        target (Callable): The function to execute in a separate worker thread.
        args (Iterable[Any]): Positional arguments for the target function.
        kwargs (Mapping[str, Any]): Keyword arguments for the target function.
        timeout (int, optional): Maximum time (in seconds) to wait for the task. Defaults to 80.
        style (SpinnerFrems | str, optional): The animation style to use (e.g., 'dots', 'arrow').
        animation_position (str, optional): Position of the spinner ('before', 'after', 'dual').
        inject_progress (bool, optional): If True, a ProgressUpdater is passed to the target function.
        title (str, optional): The message displayed next to the spinner.
        show_progress (bool, optional): If True, displays percentage progress.
        show_timer (bool, optional): If True, displays elapsed time.
        reversed_timer (bool, optional): If True, displays time remaining (based on timeout).
        spinner_color (ColorInput | ColorSequence, optional): Color for the spinner frames.
        title_color (ColorInput | ColorSequence, optional): Color for the title text.
        config (Mapping, optional): An existing configuration mapping to merge settings from.

    Returns:
        Any: The result returned by the `target` function upon completion.
    
    Raises:
        TimeOutError: If the task exceeds the specified `timeout`.
    """

    if kwargs is None:
        kwargs = {}
    elif not isinstance(kwargs, dict):
        kwargs = dict(kwargs)

    if args is None:
        args = ()
    elif not isinstance(args, Iterable) or isinstance(args, (str, bytes)):
        args = (args,)

    KEY_WORDS = vars()
    for remove_keys in ['target','config', 'args', 'kwargs', 'timeout']:
        del KEY_WORDS[remove_keys]

    spinner = Spinner(
                    config=config,
                    **KEY_WORDS
        )
    return spinner.run(target, *args, **kwargs, timeout=timeout)




# --- The Main Spinner Class ---
class Spinner(SpinnerConfig):
    """
    A customizable and reusable console spinner controller.

    This class manages the lifecycle of a background worker thread, an animation 
    thread, aggressive I/O suppression, and dynamic animation rendering using 
    compiled Python code (`exec`).

    It is configured via inheritance from SpinnerConfig.
    """
    def __init__(self, config: Optional[SpinnerConfig] = None, **kwargs):
        """
        Initializes the Spinner instance, merging configuration from a config 
        object and keyword arguments.

        Args:
            config (SpinnerConfig, optional): An existing configuration object 
                                              to inherit settings from.
            **kwargs: Overrides for any settings defined in SpinnerConfig.
        """
        super().__init__()
        if config: self.update(config)
        if kwargs: self.update(kwargs)

        try:self._setup_styles()
        except dvs_BaseException: raise
        except: raise SpinnerValueError(
                    error_value=config,
                    message="Something Went Wrong While Applying Configuration!"
                ) 
        
        self.start_time: float = 0
        self._progress_updater = ProgressUpdater()
        self.task_completed = Event()
        self.task_thread: Optional[MyThread] = None
        self.animation_thread: Optional[Thread] = None
        self.final_message = None

    def _setup_styles(self):
        """
        Pre-calculates all necessary ANSI color codes, text formatting, and 
        spinner frames based on configuration.
        """
        # Determine the message color and text
        try:    self._attrs, self._attrs_reset = Font_Styles.get(self.attrs)
        except: self._attrs, self._attrs_reset = '', ''
        
        self.title_color_code = color_function(self.title_color) if self.title_color else ''
        self.colored_message = f"{self._attrs}{self.title_color_code}{self.title }{self._attrs_reset}{RESET}"

        # Determine Colors
        self.timer_color_code    = color_function(self.timer_color        ) if self.timer_color         else ''
        self.progress_color_code = color_function(self.progress_color     ) if self.progress_color      else ''
        self.final_color_code    = color_function(self.final_message_color) if self.final_message_color else ''
        self.error_color_code    = color_function(self.error_message_color) if self.error_message_color else ''

        # Get the spinner frames and apply color
        try:
            self.spinner_interval, self.spinner_frames = (
                self.style if type(self.style).__name__ == "Spinner_Frem" else 
                Get_SPINNERS(self.style)
            )
        except SpinnerValueError: raise
        except: raise SpinnerValueError(
                    error_value = self.style,
                    keyWord='style',
                    message=f"The style name {PEACH}{self.style}{RESET} is not defined.",
                )
        
        self.spinner_interval /= 1000

        if self.spinner_color:
            _color_ = (self.spinner_color if type(self.spinner_color) == Colors 
                else Colors(self.spinner_color)
            )

            if _color_._gradient: 
                # Apply gradient to the list of frames
                self.spinner_frames = [ 
                    list(_color_.apply((self.spinner_frames,), angle=90, reset=True))[0] 
                ][0]
            else:
                # Apply uniform color to each frame
                self.spinner_frames = [
                    "".join(
                        list(_color_.apply((Frame,), reset=True))[0]
                    ) for Frame in self.spinner_frames
                ]


    def Get_animator(self) -> Callable:
        """
        Dynamically generates and compiles the `_run_animation_loop` function using `exec`.
        
        This technique optimizes runtime performance by injecting constant state (colors, 
        timing, style) into a single, highly efficient function run by the animation thread.

        Returns:
            Callable: The compiled `_run_animation_loop` function.
        """
        # Determine progress and timer display strings based on configuration
        progresh_str = ( fr'{self.progress_color_code}{{self._progress_updater.value:.1f}}%{RESET}'
            if self.inject_progress else fr'{self.progress_color_code}{{(elapsed_time / timeout_ratio):.1f}}%{RESET}' 
        )   if self.show_progress   else ''

        Timer_str = (
            rf'{self.timer_color_code}({{max(0, self.timeout - elapsed_time):.1f}}s remaining){RESET}' 
            if self.reversed_timer else rf'{self.timer_color_code}({{elapsed_time:.1f}}s){RESET}' 
        )   if self.show_timer     else ''

        # Determine how the spinner is positioned relative to the message
        if   self.animation_position == 'after': animation_type = rf"{self.colored_message} {{self.spinner_frames[spinner_index]}}"
        elif self.animation_position == 'dual' : animation_type = rf"{{self.spinner_frames[spinner_index]}} {self.colored_message} {{self.spinner_frames[spinner_index]}}"
        else:                                    animation_type = rf"{{self.spinner_frames[spinner_index]}} {self.colored_message}"

        # Initialize progress status for final message display
        self.current_progresh_status = ''
        
        # --- Dynamic Code Generation (Injection of Constants/Logic) ---
        func_code  = rf'''
def _run_animation_loop():
    spinner_index = 0
    spinner_frames_Len = len(self.spinner_frames)
    spinner_interval = self.spinner_interval
    animaiton_exception = None

    {'timeout_ratio = self.timeout / 100' if not self.inject_progress else ''}

    start_time = time()
    try:    
        while not self.task_completed.is_set():
            elapsed_time = time() - start_time

            _write(f'\r{animation_type} {progresh_str} {Timer_str}{RESET} ')
            _flush()

            sleep(spinner_interval)
            spinner_index = (spinner_index + 1) % spinner_frames_Len

    except Exception as e:
        self.animaiton_exception = e
        

    finally:
        # Capture final status for potential error/timeout message display
        self.current_progresh_status = f"{progresh_str} {Timer_str}{RESET}"

        # Final cleanup and success message display
        if self.stay and not self.exception and not self.task_thread.is_alive():    
                _write(f'\033[2K\r{self.title_color_code}✓ {self.colored_message} {f'{self.progress_color_code} 100.0%' if self.show_progress else ''} {Timer_str} {RESET}\n')
        else:   _write("\r\033[2K") # Clear the line if stay is False

        _flush()
        self.task_completed.set()
'''
        # Define the execution scope (mapping instance attributes to local vars)
        exec_globals = {
            'self'             : self,
            'time'             : time,
            'sleep'            : sleep,
            '_write'           : _write,
            '_flush'           : _flush,
            'color_function'   : color_function,
            'task_thread'      : self.task_thread,
            'stay'             : self.stay,
            'start_time'       : self.start_time,
            'timeout'          : self.timeout,
        }

        # Compile and execute the function code
        compiled_code = compile(func_code, "<dynamic_spinner_runner>", "exec")
        local_scope: Dict[str, Any] = {}
        exec(compiled_code, exec_globals, local_scope)

        return local_scope["_run_animation_loop"]


    def run(self, target: Callable, *args, timeout=None, **kwargs) -> Any:
        """
        The main execution method. Runs the target function in a background worker 
        thread while displaying the animated spinner.

        The method implements aggressive I/O Suppression to prevent console output 
        from the target function from corrupting the animation.

        Args:
            target (Callable): The function to execute.
            *args: Positional arguments for the target.
            timeout (int, optional): Maximum time to wait. Overrides the configured timeout.
            **kwargs: Keyword arguments for the target (including optional 'progress_updater').

        Returns:
            Any: The result of the `target` function.

        Raises:
            Exception: Re-raises any exception caught from the target thread.
            TimeOutError: If the task exceeds the specified `timeout`.
        """
        self.exception = None
        self.animaiton_exception = None
        self.result = None

        if type(timeout) is int and timeout > 0:
            self.timeout = timeout

        if  kwargs.get('progress_updater'):
            kwargs['progress_updater'] = self._progress_updater
            self.inject_progress = True

        def wrapped_target():
            """Worker function executed in the background thread."""
            try:
                self.result = target(*args, **kwargs)
            except Exception as e:
                self.exception = e

        # --- I/O Suppression Setup (File Descriptor Redirection) ---
        original_stdout_fd = os.dup(sys.stdout.fileno())
        original_stderr_fd = os.dup(sys.stderr.fileno())
        null_fd = os.open(os.devnull, os.O_WRONLY)

        try:
            # 1. Redirect low-level file descriptors (fd 1 & 2) to a null device.
            os.dup2(null_fd, sys.stdout.fileno())
            os.dup2(null_fd, sys.stderr.fileno())

            # 2. Redirect high-level Python streams to dummy buffers.
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            dummy_stream = io.StringIO()
            sys.stdout = dummy_stream
            sys.stderr = dummy_stream

            self.start_time = time()

            self.task_thread = MyThread(target=wrapped_target, daemon=True)
            self.animation_thread = Thread(target=self.Get_animator(), daemon=False)
            
            self.task_thread.start()
            self.animation_thread.start()

            # Wait for task completion or timeout
            self.task_thread.join(timeout=self.timeout)
            self.task_completed.set() # Signal animation thread to stop
            self.animation_thread.join(timeout=self.timeout) # Wait for animation cleanup

        except Exception as e:
            self.exception = e

        finally:
                # --- I/O Restoration (CRITICAL STEP) ---
                sys.stdout = original_stdout
                sys.stderr = original_stderr
                os.dup2(original_stdout_fd, sys.stdout.fileno())
                os.dup2(original_stderr_fd, sys.stderr.fileno())
                os.close(null_fd)
                os.close(original_stdout_fd)
                os.close(original_stderr_fd)
                self.task_completed.set() # Final cleanup signal

        # --- Post-Execution Check and Error Handling ---
        
        # 1. Check for timeout
        if self.task_thread.is_alive():
            _write(f"\r\033[2K{self.error_color_code}✖\033[0m {self.colored_message} {self.current_progresh_status} {self.error_color_code}timed out after {self.timeout}s{RESET}\n")
            _flush()
            raise TimeOutError(self.timeout)
        
        # 2. Check for exception from the worker thread
        if self.exception:
            if self.error_message:
                    _write(f"\r\033[2K{self.error_color_code}✖\033[0m {self.colored_message } {self.current_progresh_status} {self.error_color_code}{self.error_message}{RESET}\n")
            else:   _write(f"\r\033[2k{self.error_color_code}✖\033[0m {self.colored_message } {self.current_progresh_status} {self.error_color_code}failed with error: {self.exception}{RESET}\n")
            _flush()
            raise self.exception
        
        # 3. Check for animation thread exception (should be rare)
        if self.animaiton_exception:
            _write(f"\r{self.error_color_code}✖ failed during animation: {self.animaiton_exception}{RESET}\n")
            _flush()
            raise SpinnerValueError(
                error_value=target.__name__,
                keyWord="target",
                message= f"Something Went Wrong, Maybe While Running {PEACH}Animation Loop{RESET} Function.\n{self.animaiton_exception}"
            )
        

        # 4. Success message display
        if self.final_message:
            _write(f"\r\033[2K{self.final_color_code}✓\033[0m {self.colored_message} completed successfully!{RESET}\n")
        _flush()

        return self.result


    def __call__(self, target: Callable, *args, **kwargs):
        """
        Makes the instance callable, allowing it to be used directly like a function.
        """
        try:
            return self.run(target, *args, **kwargs)
        except Exception as E:
            raise E

    def decorator(self, target: Callable) -> Callable:
        """
        A decorator to easily apply the spinner to a function.

        Usage:
            @Spinner(title="Calculating", style='dots').decorator
            def compute_task(): ...
        """
        @wraps(target)
        def wrapper(*args, **kwargs):
            return self.run(target, *args, **kwargs)
        return wrapper
