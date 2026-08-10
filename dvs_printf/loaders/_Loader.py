"""
The core module for the LoadingBar system.

Contains the LoadingBar class, which manages threading, console I/O suppression, 
dynamic animation execution, and state management for showing a progress bar 
while a target function runs.
"""

# import io, os, sys
from functools import wraps
from time      import time, sleep
from threading import Event, Thread
from typing    import (Any, Callable, Iterable, 
                       Mapping, Optional, Union, Tuple, List, Dict)

# custom imports (Assuming these are accessible via relative imports)
from ..exceptions import TimeOutError, LoaderValueError, LoaderAttributeError
from ..colors import (  Colors, 
                        get_ansi_color,
                        get_gredinat_style,
                        isgredinat,
                        apply_gradient,
                        console_EnvType, 
                        RESET_FOREGROUND as RESET_FG)

from .loader_config    import ColorInput, GredinatInput, LoadingBarConfig
from .loader_frems     import get_bar_style, LoaderFrems
from .system_tools     import (
    MyThread, ProgressUpdater,
    bg_color_function,
    color_function, _write, _flush
)


def ShowLoading(
        target: Optional[Callable],
        args: Iterable[Any] = (),
        kwargs: Optional[Mapping[str, Any]] = {},
        timeout: Optional[Union[int, float]] = 80,
        daemon: Optional[bool] = None,
        name: Optional[str] = None,
        *,
        inject_progress: Optional[bool] = None,
        title_text: Optional[str] = "Loading",
        style: Optional[str] = "grow",
        show_gradient_anyway: Optional[bool] = False,
        grid_rotation_speed: Optional[int] = 1,
        bar_borders: Optional[str] = None,
        final_message: Union[str, bool, None] = None,
        # error_message:  Union[str, bool, None] = None,
        stay: Optional[bool] = None,
        FPS: Optional[int] = None,
        full_screen_mode: Optional[bool] = None,
        title_color: ColorInput | GredinatInput | None = (255, 255, 255),
        bar_color: Optional[ColorInput] = "green",
        unfilled_bar_color: Optional[ColorInput] = "#2B2B2B",
        bar_borders_color: Optional[ColorInput] = "#00aeff",
        percentage_color: Optional[ColorInput] = "#ea9329",
        timing_color: Optional[ColorInput] = "#00aeff",
        config: Optional[Mapping] = None
    ) -> Any:
    """
    Convenience wrapper function to initialize and run the LoadingBar immediately.

    This function collects all provided arguments, passes them to the LoadingBar
    class for configuration, and calls the `run` method to start the process.

    Args:
        target (Callable): The function to execute in the background.
        args (Iterable[Any]): Positional arguments for the target function.
        kwargs (Mapping[str, Any]): Keyword arguments for the target function.
        timeout (int, optional): Maximum time in seconds to wait for the task. Defaults to 80.
        daemon (bool, optional): Whether the background thread should be a daemon (ignored for run, managed by MyThread).
        name (str, optional): Name of the worker thread.
        
        * (Configuration arguments): All other keyword arguments are passed to the 
            LoadingBarConfig for visual setup.

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

    Loder = LoadingBar(
        config=config,
        **KEY_WORDS
    )

    if kwargs.get('progress_updater', inject_progress):
        kwargs['progress_updater'] = True 

    return Loder.run(
        target, *args, **kwargs, 
        timeout = timeout
    )


def showLoading(*args, **kwargs) -> Any:
    """
    Deprecated alias for `ShowLoading`.

    .. deprecated:: 3.1.0
       `showLoading` has been renamed to `ShowLoading` to adhere to standard 
       PascalCase factory function naming conventions. This function will be 
       removed in a future major release. Please update your codebase to use `ShowLoading`.

    Args:
        *args: Positional arguments forwarded to `ShowLoading`.
        **kwargs: Keyword arguments forwarded to `ShowLoading`.

    Returns:
        Any: The execution result of the background task target.
    """
    print(
        "\033[38;2;255;165;0m[DEPRECATION WARNING] Function 'showLoading' is deprecated and will be removed in the next major update.\n"
        " -> 'showLoading' has been renamed to 'ShowLoading'. Please use 'ShowLoading' from now on.\n"
        " -> Documentation: https://github.com/dhruvan-vyas/dvs_printf/blob/main/READMES/loaders_README.md\033[0m\n"
    )
    # Legacy keyword argument mapping for backward compatibility
    if 'LoadingText' in kwargs:
        kwargs['title_text'] = kwargs.pop('LoadingText')
    if 'progressChar' in kwargs:
        kwargs['bar_borders'] = kwargs.pop('progressChar')
    return ShowLoading(*args, **kwargs)


class LoadingBar(LoadingBarConfig):
    """
    A customizable and reusable console loading bar controller.

    This class manages the lifecycle of a background worker thread, an animation 
    thread, aggressive I/O suppression (via file descriptor redirection), and 
    dynamic animation rendering using compiled Python code (`exec`).

    It can be configured with various colors, styles, and timing options via
    inheritance from LoadingBarConfig.
    """
    def __init__(self, config: Optional[LoadingBarConfig] = None, **kwargs):
        """
        Initializes the LoadingBar instance, merging configuration from a config 
        object and keyword arguments.

        Args:
            config (LoadingBarConfig, optional): An existing configuration object 
                                                 to inherit settings from.
            **kwargs: Overrides for any settings defined in LoadingBarConfig.
        """
        super().__init__()
        if config: self.update(config)
        if kwargs: self.update(kwargs)

        # self.config = config if config else LoadingBarConfig()
        # self.config.update(kwargs)

        self._progress_updater: ProgressUpdater = ProgressUpdater()
        self.task_thread: MyThread = None
        self.task_completed: Event = Event() # Signal for the animation loop to stop
        self.animation_thread = None
        self.start_time = None
        self.result = None
        self.exception = None # Exception raised by the target function
        self.reset_color = '\033[0m'
        self._setup_colors_and_styles()

    # def __getattr__(self, name):
    #     """Allows reading 'loader.timeout' directly"""
    #     return getattr(self.config, name)

    # def __setattr__(self, name, value):
    #     """Allows writing 'loader.timeout = 300' directly"""
    #     # If the attribute exists in config, write it there
    #     if name != 'config' and hasattr(self, 'config') and hasattr(self.config, name):
    #         setattr(self.config, name, value)
    #     else:
    #         # Otherwise, write it to the main class (like 'thread', 'result')
    #         super().__setattr__(name, value)

    def __getattr__(self, name):
        """Allows reading 'loader.timeout' directly"""
        if 'config' not in self.__dict__ or name == 'config':
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        return getattr(self.config, name)

    def __setattr__(self, name, value):
        """Allows writing 'loader.timeout = 300' directly"""
        if name != 'config' and 'config' in self.__dict__ and hasattr(self.config, name):
            setattr(self.config, name, value)
        else:
            # Otherwise, write it to the main class (like 'thread', 'result')
            super().__setattr__(name, value)


    def _setup_colors_and_styles(self):
        """
        Pre-calculates all necessary ANSI color codes, bar components, and gradient 
        configurations.

        This method converts user-friendly color names/tuples into raw ANSI strings 
        and sets up the internal flags (`use_gradient`, `GCo`) required by the 
        dynamic animation runner.
        """
        self.grid_rotation_speed = max(1, min(10, round(self.grid_rotation_speed)))

        # Gradient check for bar color (simplified logic, assumes non-gradient is single color)
        is_bar_color_gradient = isgredinat(self.bar_color)
        if not is_bar_color_gradient:
            self.bar_color = get_ansi_color(self.bar_color)

        # print( "self.bar_color:", [self.bar_color] )
        # Bar styles and components (e.g., '█', '░', '│')
        style_config = get_bar_style(
            self.style,
            bg_color_function(self.unfilled_bar_color),
            get_ansi_color(self.unfilled_bar_color),
            self.reset_color
        )
        self.bar_characters = style_config["characters"]
        self.partial_char_len = style_config["partial_len"]
        self.full_block = style_config["full_block"]
        self.default_borders = style_config["border"]

        if len(self.full_block) > 1:
                self.full_block_main = self.full_block[0]
                self.full_block_fill = self.full_block[1]
        else:   self.full_block_main = self.full_block_fill = self.full_block

        # Pre-calculated text components with colors
        self.title_str                = Colors(self.title_color).apply_to_str(self.title_text)
        self.percentage_color_code    = " " +    get_ansi_color(self.percentage_color)
        self.timer_color_code         = " in " + get_ansi_color(self.timing_color)
        self.unfilled_bar_color_ansi  =          get_ansi_color(self.unfilled_bar_color)
        self.error_color_code         =          get_ansi_color(self.error_color) 

        # Borders and Finalizing Percentage Code
        border_color_ansi = Colors(self.bar_borders_color)._get_ansi_color() if self.bar_borders_color else ""
        borders = "" if self.bar_borders == "" else (  # becouse: "self.bar_borders can be None"
                    self.bar_borders or self.default_borders 
                )
        
        if len(borders) > 1:
                self.border_left  = f"{self.reset_color}{border_color_ansi}{borders[0]}"
                self.border_right = f"{self.reset_color}{border_color_ansi}{borders[1]}"
        elif borders == "":     
                self.border_left  = self.border_right = f"{self.reset_color}"
        else:   self.border_left  = self.border_right = f"{self.reset_color}{border_color_ansi}{borders}"

        self.percentage_color_code = self.border_right + self.percentage_color_code

        # Gradient Setup
        self.is_gradient  = isgredinat(self.bar_color)
        self.use_gradient = (   (console_EnvType == 1 or self.show_gradient_anyway)
                             and self.is_gradient
                        )
        self.GCo = None
        self.grid_len = 180 # Default length for gradient string generation

        if self.use_gradient:
            self.gradient_colors = Colors((self.bar_color + self.bar_color[::-1]))
            
            gradient_block = self.full_block_main * self.grid_len
            if isinstance(self.gradient_colors, Colors):
                self.GCo = list(self.gradient_colors.apply((gradient_block,), angle=90, reset=False))[0]
            else:
                self.GCo = list(apply_gradient([gradient_block], self.gradient_colors, angle=90, reset=False))[0]
            self.grid_len = len(self.GCo)
        
        # Determine bar dimensions
        self.bar_length = 40
        self.use_bar_len = self.bar_length - self.partial_char_len

    def _get_refresh_rate(self) -> float:
        """
        Determines the optimal animation refresh rate (sleep duration) based on 
        the configured `timeout` or `FPS`.
        """
        if self.FPS: return (.9 / self.FPS) 
        # Fallback to predefined mapping based on timeout duration
        if self.timeout <=  20: return 0.05
        if self.timeout <=  40: return 0.03
        if self.timeout <=  60: return 0.02
        if self.timeout <=  80: return 0.1
        if self.timeout <= 100: return 0.2
        if self.timeout <= 120: return 0.24
        return 0.5
    
    def _Get_Animation_Runner(self):
        """
        Dynamically generates and compiles the `_run_animation_loop` function using `exec`.
        
        This technique optimizes runtime performance by compiling the final animation 
        logic—which is dependent on instance state (e.g., gradient mode, colors)—into 
        a single, highly efficient function that is executed by the animation thread.

        Returns:
            Callable: The compiled `_run_animation_loop` function.
        """
        text =  rf"\r\x1b[2K{self.title_str} {self.border_left}" + (
                    rf"{self.bar_color}" if (not self.use_gradient and type(self.bar_color) == str)  
                    else ""
                )

        timeout_ratio = self.timeout / 100

        # Define lambda for getting progress (either time-based or injection-based)
        if self.inject_progress:
                get_progress = lambda _: self._progress_updater.value
        else:   get_progress = lambda elapsed: elapsed / timeout_ratio

        # Define lambda for joining gradient parts (only necessary for gradient)
        if self.use_gradient:   smooth_bar=lambda TL:"".join(TL) 
        else:                   smooth_bar=lambda T :T
            
        
        # --- Dynamic Code Generation (Injection of Constants/Logic) ---
        
        grid_color_bar = rf'''
            _write(
                f"{text}{{''.join((GCo[i:] + GCo[:(i + full_blocks) - grid_len])) if (i + full_blocks) >= grid_len else ''.join(GCo[i:full_blocks + i])}}{{bar_characters[filled_units % Len_barChars]}}{{full_block_fill * (Use_bar_len - full_blocks)}}"
                f"{self.percentage_color_code}{{progress:.2f}}%\033[0m{self.timer_color_code}{{elapsed_time:.1f}}s\033[0m",    
            )
            _flush()
            sleep(refresh_rate)
            if (i-grid_rotation_speed) <= 0: i = grid_len
            i -= grid_rotation_speed'''
        current_grid_color_bar_state = '        bar = GCo[i:]+GCo[:(i+bar_length+1)-grid_len] if (i + bar_length+1) >= grid_len else GCo[i:bar_length+i+1]'


        single_color_bar = rf'''
            _write(
                f'{text}{{full_block * full_blocks}}{{bar_characters[filled_units % Len_barChars]}}{self.unfilled_bar_color_ansi}{{full_block_fill * (Use_bar_len - full_blocks)}}'
                f'{self.percentage_color_code}{{progress:.2f}}%{self.timer_color_code}{{elapsed_time:.1f}}s\033[0m'
            )
            _flush()
            sleep(refresh_rate)'''
        current_single_color_bar_state = '        bar = full_block*(bar_length+1)'

        Errored_bar     = rf"{text}{self.error_color_code}{{full_block * (Use_bar_len+partial_Char_Len)}}{self.percentage_color_code}ERROR\033[0m{self.timer_color_code}{{elapsed_time:.1f}}s \033[0m\n{self.error_color_code}{{e}}\033[0m "
        _smooth_bar     = rf"{text}{'{smooth_bar(bar[:blocks])}' if self.GCo else '{smooth_bar(bar[:blocks])}'}{self.unfilled_bar_color_ansi}{{full_block_fill*(Use_bar_len-blocks+partial_Char_Len)}}{self.percentage_color_code}{{progress:.2f}}%\033[0m{self.timer_color_code}{{elapsed_time:.1f}}s\033[0m"
        finally_massage = rf"{text}{{smooth_bar(bar[:Use_bar_len+partial_Char_Len])}}{self.percentage_color_code}100.0%\033[0m{self.timer_color_code}{{elapsed_time:.1f}}s\033[0m"


        func_code =  rf'''
def _run_animation_loop():
    start_time   = time()
    filled_units = full_blocks = progress = elapsed_time = progress = 0
    Len_barChars = len(bar_characters) 
    bar_pr       = (bar_length * len(bar_characters)) / 100
    animaiton_exception = e = None

    {'i=0' if self.GCo else ''}
    try:
        while not self.task_completed.is_set() {"and progress < 99" if not self.inject_progress else ""}:
            elapsed_time = time() - start_time
            progress   = {f'elapsed_time / {self.timeout / 100}' if not self.inject_progress else 'self._progress_updater.value'} 
            filled_units = int(bar_pr * progress)
            full_blocks  = filled_units // Len_barChars
    {grid_color_bar if self.GCo else single_color_bar}

    {current_grid_color_bar_state if self.GCo else current_single_color_bar_state}

    except Exception as e:
        animaiton_exception = e
    finally:
        if animaiton_exception: 
            self.exception = "LoaderAnimationError"
            _write(f"\r\x1b[2K{{self.error_color_code}}✖ failed during animation: {{e}}{{RESET_FG}}\n")
        elif self.task_thread.is_alive():
            e = "Timeout ERROR"
            _write(f'\r\x1b[2K{Errored_bar}\n')
        elif self.exception:
            e = self.exception
            _write(f'\r\x1b[2K{Errored_bar}\n')
        else:
            for blocks in range(full_blocks, Use_bar_len+2):
                _write(f'\r\x1b[2K{_smooth_bar}')
                sleep(.02)
            if stay:
                _write(f'\r\x1b[2K{finally_massage}\n')
            else:
                sleep(.8)
                _write('\r\x1b[2K')
        _flush()
    '''
        # Define the execution scope (mapping instance attributes to local vars)
        exec_globals = {
            'self'             : self,
            'time'             : time,
            'sleep'            : sleep,
            '_write'           : _write,
            '_flush'           : _flush,
            'smooth_bar'       : smooth_bar,
            'get_progress'     : get_progress,
            'color_function'   : color_function,
            'task_thread'      : self.task_thread,
            'prefix'           : self.title_text,
            'GCo'              : self.GCo,
            'bar_characters'   : self.bar_characters,
            'full_block'       : self.full_block_main,
            'full_block_fill'  : self.full_block_fill,
            'unfilled_color'   : self.unfilled_bar_color_ansi,
            'percent_color'    : self.percentage_color_code,
            'timing_color'     : self.timing_color,
            'stay'             : self.stay,
            'start_time'       : self.start_time,
            'Use_bar_len'      : self.use_bar_len,
            'partial_Char_Len' : self.partial_char_len,
            'bar_length'       : self.bar_length,
            'grid_len'         : self.grid_len,
            'timeout'          : self.timeout,
            'refresh_rate'     : self._get_refresh_rate(),
            'timeout_ratio'    : timeout_ratio,
            'grid_rotation_speed': self.grid_rotation_speed,
            'RESET_FG'         : RESET_FG,
        }
        
        # Compile and execute the function code
        compiled_code = compile(func_code, "<dynamic_loader>", "exec")
        local_scope: Dict[str, Any] = {}
        exec(compiled_code, exec_globals, local_scope)

        return local_scope["_run_animation_loop"]


    def run(self, target: Callable, *args, timeout: Optional[Union[int, float]] = None, **kwargs, ) -> Any:
        """
        The main execution method. Runs the target function in a background worker 
        thread while displaying the animated loading bar.

        The animation thread suppresses all console output from the target function 
        (I/O Suppression) unPURPLE completion.

        Args:
            target (Callable): The function to execute.
            *args: Positional arguments for the target.
            timeout (int, float, optional): Maximum time to wait. Overrides the configured timeout.
            **kwargs: Keyword arguments for the target (including optional 'progress_updater').

        Returns:
            Any: The result of the `target` function.

        Raises:
            Exception: Re-raises any exception caught from the target thread.
            TimeOutError: If the task exceeds the specified `timeout`.
        """
        self.result = None
        self.exception = None

        if isinstance(timeout, (int, float)) and not isinstance(timeout, bool) and timeout > 0:
            self.timeout = timeout

        if  kwargs.get('progress_updater'):
            kwargs['progress_updater'] = self._progress_updater
            self.inject_progress = True


        def run_target_task():
            """Worker function executed in the background thread."""
            try: self.result = target(*args, **kwargs)
            except Exception as e: 
                self.exception = e

        # --- I/O Suppression Setup (File Descriptor Redirection) ---
        # original_stdout_fd = os.dup(sys.stdout.fileno())
        # original_stderr_fd = os.dup(sys.stderr.fileno())
        # null_fd = os.open(os.devnull, os.O_WRONLY)

        try:
            # 1. Redirect low-level file descriptors (fd 1 & 2) to a null device.
            # os.dup2(null_fd, sys.stdout.fileno())
            # os.dup2(null_fd, sys.stderr.fileno())

            # # 2. Redirect high-level Python streams to dummy buffers.
            # original_stdout = sys.stdout
            # original_stderr = sys.stderr
            # dummy_stream = io.StringIO()
            # sys.stdout = dummy_stream
            # sys.stderr = dummy_stream
            
            # --- Thread Execution ---
            self.task_thread      = MyThread(target=run_target_task, daemon=True)
            self.animation_thread = Thread(target=self._Get_Animation_Runner())

            self.task_thread.start()    
            self.animation_thread.start()

            # Wait for task completion or timeout
            self.task_thread.join(timeout=self.timeout)
            self.task_completed.set() # Signal animation thread to stop
            self.animation_thread.join()
       
        except Exception as e:
            self.exception = e
        finally:
            # --- I/O Restoration (CRITICAL STEP) ---
            # sys.stdout = original_stdout
            # sys.stderr = original_stderr
            # os.dup2(original_stdout_fd, sys.stdout.fileno())
            # os.dup2(original_stderr_fd, sys.stderr.fileno())
            # os.close(null_fd)
            # os.close(original_stdout_fd)
            # os.close(original_stderr_fd)
            self.task_completed.set() # Ensure cleanup signal is sent again


        # --- Post-Execution Check ---
        if self.task_thread.is_alive():
            # If thread is sPURPLEl alive after join(timeout), it timed out.
            raise TimeOutError(self.timeout)
        
        if self.exception:
            if (    'progress_updater' in kwargs 
                and type(kwargs['progress_updater']) != ProgressUpdater
                and self.inject_progress == True
            ):  
                raise LoaderAttributeError(error_value=kwargs['progress_updater'], keyWord='progress_updater')
            raise self.exception
        
        return self.result

    def __call__(self, target: Callable, *args, **kwargs):
        """
        Makes the instance callable, allowing it to be used directly like a function.
        """
        return self.run(target, *args, **kwargs)
    
    def decorator(self, target: Callable) -> Callable:
        """
        A decorator to easily apply the loading bar to a function.

        Usage:
            @LoadingBar(title_text="Processing Files").decorator
            def long_task(...): ...
        """
        @wraps(target)
        def wrapper(*args, **kwargs):
            return self.run(target, *args, **kwargs)
        return wrapper
    
    # def __delattr__(self, name):
    #     return super().__delattr__(name)
