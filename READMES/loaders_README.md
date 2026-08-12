# Loaders & Spinners: Multi-Threaded Progress (`dvs_printf.loaders`)

The `dvs_printf.loaders` module provides professional-grade tools for visual feedback during background tasks, featuring **Aggressive I/O Suppression** and non-blocking dual-thread execution.

---

## Dual-Thread Architecture & POSIX I/O Suppression (`SafeIOSuppressor`)

```
[ Main Thread ]
      │
      ├──> Worker Thread (MyThread: Executes target funciton in background)
      │
      └──> Animation Thread (High-FPS visual progress loop)
                │
                ▼ (Polls task_completed Event)
      ┌───────────────────────────────────────────────────────────┐
      │ SafeIOSuppressor Context Engine                           │
      ├─────────────────────────────┬─────────────────────────────┤
      │ Standard POSIX Terminal     │ Jupyter / Pytest / IDE      │
      │ (os.dup2 POSIX FD 1 & 2)    │ (sys.stdout Stream Backup)  │
      │ + atexit emergency hook     │ (Zero fileno UnsupportedOp) │
      └─────────────────────────────┴─────────────────────────────┘
```

1. **Dual-Thread Execution:** A dedicated worker thread (`MyThread`) executes background tasks concurrently, while an un-blocked animation thread renders real-time FPS visual updates without lagging the main execution loop.
2. **Kernel-Level POSIX I/O Suppression (`SafeIOSuppressor`):** Uses low-level `os.dup2` file descriptor redirection to route stray C-level `printf` and C++ `std::cout` outputs (from heavy libraries like PyTorch, TensorFlow, NumPy, OpenCV, and database drivers) to `/dev/null` during animations.
3. **Emergency Cleanup (`atexit` Hooks):** Registers `@atexit.register` emergency hooks to guarantee that if Python exits abruptly or encounters an unhandled `SIGINT` (`Ctrl+C`), all process-level file descriptors are restored instantly, preventing terminal freeze or silence.
4. **Environment Auto-Detection Matrix:** Dynamically inspects `sys.modules` for Jupyter (`ipykernel`) or Pytest (`pytest`/`PYTEST_CURRENT_TEST`). In non-POSIX stream environments, it automatically falls back to high-level stream redirection (`sys.stdout`) without raising `io.UnsupportedOperation: fileno`.

---

## `suppress_io` Configuration Modes

Both `LoadingBar` and `Spinner` support the `suppress_io` configuration parameter:

| `suppress_io` Mode | Mechanism | Best Use Case | Safety Guarantee |
| :--- | :--- | :--- | :--- |
| `"auto"` *(Default)* | Auto-detects runtime environment. Uses `"fd"` in standard terminals and `"stream"` in Jupyter/Pytest/IDEs. | General CLI applications, data science scripts, and test suites. | 100% crash-safe across all environments. |
| `"fd"` | Kernel-level POSIX `os.dup2` redirection of File Descriptors 1 & 2. | Suppresses heavy backend C-extension output (PyTorch, TensorFlow, C++ DLLs). | Protected via `atexit` emergency hooks. |
| `"stream"` | High-level `sys.stdout` / `sys.stderr` stream redirection only. | Multi-threaded applications where other background threads log to console. | Eliminates process-wide Thread Bleed. |
| `False` / `"none"` | Disables I/O suppression entirely. | Debugging background task outputs. | Raw stdout/stderr pass-through. |

---

## Exhaustive `LoadingBar` Parameter Reference

The `LoadingBar` class handles deterministic progress tracking (0–100%).

```python
class LoadingBar(LoadingBarConfig):
    def __init__(self, config: Optional[LoadingBarConfig] = None, **kwargs): ...

    def run(self, target: Callable, *args, timeout: int = None, **kwargs) -> Any: ...
```

### `LoadingBar` & `LoadingBarConfig` Parameter Breakdown

| Parameter | Type | Default | Deep Technical Explanation |
| :--- | :--- | :--- | :--- |
| `target` | `Callable` | *Required in `.run()`* | Background function to execute concurrently in `MyThread`. |
| `args` | `Iterable[Any]` | `()` | Positional arguments passed directly to `target(*args)`. |
| `kwargs` | `Mapping[str, Any]` | `{}` | Keyword arguments passed directly to `target(**kwargs)`. |
| `timeout` | `int \| float \| None` | `80` | Maximum execution time in seconds. If `target` exceeds this, `TimeOutError` is raised. |
| `title_text` | `str` | `"Loading"` | Message string displayed alongside or above the progress bar. |
| `title_color` | `ColorInput` | `(255, 255, 255)` | Color applied to `title_text`. Accepts tuple, hex, or color name string. |
| `style` | `str` | `"grow"` | Visual bar component style (`"grow"`, `"line"`, `"growvertical"`, `"mesh"`, `"numbers"`, `"spinner"`). |
| `bar_color` | `ColorInput \| GredinatInput` | `"green"` | Foreground color for filled bar blocks. Accepts single color or gradient color list (e.g. `["pink", "orange"]`). |
| `unfilled_bar_color` | `ColorInput` | `"#2B2B2B"` | Background color for unfilled bar track characters. |
| `bar_borders` | `str \| None` | `None` | Custom border characters surrounding bar (e.g. `"-+"`, `"[]"`, `"<>"`). Defaults to style border. |
| `bar_borders_color` | `ColorInput` | `"#00aeff"` | Color applied to border characters. |
| `percentage_color` | `ColorInput` | `"#ea9329"` | Color applied to the numeric percentage readout (`XX.XX%`). |
| `timing_color` | `ColorInput` | `"#00aeff"` | Color applied to the elapsed time timer readout (`in X.Xs`). |
| `error_color` | `ColorInput` | `"scarlet"` | Color applied to error messages if `target` raises an exception. |
| `inject_progress` / `progress_updater` | `bool` | `False` | If `True`, injects a thread-safe `ProgressUpdater` instance into `kwargs['progress_updater']`. |
| `show_gradient_anyway` | `bool` | `False` | Forces 24-bit gradient bar calculation even if console environment is detected below TrueColor. |
| `grid_rotation_speed` | `int` | `1` | Speed multiplier (1 to 10) for angular gradient shift animation along the bar track. |
| `stay` | `bool` | `True` | Keeps final progress bar visible (`True`) or erases line (`False`) upon completion. |
| `FPS` | `int \| None` | `None` | Frames per second refresh frequency for animation loop. |
| `full_screen_mode` | `bool \| None` | `False` | Automatically calculates terminal width (`get_terminal_size()`) and stretches bar across screen. |
| `suppress_io` | `str \| bool \| None` | `"auto"` | Configures I/O suppression mode (`"auto"`, `"fd"`, `"stream"`, `False`). Prevents C-level & background thread logs from distorting visual progress bar. |

---

## Exhaustive `Spinner` Parameter Reference

The `Spinner` class handles indeterminate progress tracking for tasks of unknown duration.

```python
class Spinner(SpinnerConfig):
    def __init__(self, config: Optional[SpinnerConfig] = None, **kwargs): ...

    def run(self, target: Callable, *args, timeout = None, **kwargs) -> Any: ...
```

### `Spinner` & `SpinnerConfig` Parameter Breakdown

| Parameter | Type | Default | Deep Technical Explanation |
| :--- | :--- | :--- | :--- |
| `target` | `Callable` | *Required in `.run()`* | Background function to execute concurrently in `MyThread`. |
| `args` | `Iterable[Any]` | `()` | Positional arguments passed to `target(*args)`. |
| `kwargs` | `Mapping[str, Any]` | `{}` | Keyword arguments passed to `target(**kwargs)`. |
| `timeout` | `int \| float \| None` | `80` | Maximum execution time in seconds before raising `TimeOutError`. |
| `style` | `SpinnerFrems \| str` | `"arrow"` | Spinner frame sequence preset (e.g. `"dots"`, `"arrow"`, `"moon"`, `"shark"`, `"pong"`, `"bounce"`, `"line"`, `"earth"`, `"runner"`, `"moons"`). |
| `animation_position` | `str` | `"before"` | Alignment of spinner animation relative to title text (`"before"`, `"after"`, `"dual"`). |
| `title` | `str` | `"Loading"` | Message string displayed next to spinner animation. |
| `title_color` | `ColorInput` | `None` | Color applied to `title` text. |
| `spinner_color` | `ColorInput` | `None` | Color scheme applied to spinner animation frames. Supports single colors or gradient objects. |
| `attrs` | `list[str]` | `[]` | Text attributes applied to title (`["bold"]`, `["italic"]`). |
| `show_timer` | `bool` | `True` | Displays elapsed execution time `(X.Xs)` next to spinner. |
| `reversed_timer` | `bool` | `False` | Displays countdown remaining time `(X.Xs remaining)` based on timeout. |
| `show_progress` | `bool` | `True` | Displays percentage progress readout `XX.X%`. |
| `inject_progress` | `bool` | `False` | Injects `ProgressUpdater` into `target` kwargs for manual progress percentage updates. |
| `stay` | `bool` | `True` | Keeps final completion line visible (`True`) or erases line (`False`). |
| `final_message` | `str \| None` | `None` | Custom text string displayed upon successful completion. |
| `final_message_color` | `ColorInput` | `"springgreen"` | Color for success message. |
| `error_message` | `str \| None` | `None` | Custom text string displayed if `target` raises an exception. |
| `error_message_color` | `ColorInput` | `"scarlet"` | Color for error message. |
| `progress_color` | `ColorInput` | `"gray"` | Color applied to percentage progress text. |
| `timer_color` | `ColorInput` | `"pink"` | Color applied to timer readout. |
| `suppress_io` | `str \| bool \| None` | `"auto"` | Configures I/O suppression mode (`"auto"`, `"fd"`, `"stream"`, `False`). Controls POSIX FD vs stream level redirection. |

---

## The `ProgressUpdater` & `progress_updater=True` Pattern

For precise iteration tracking inside background functions:

```python
import time
from dvs_printf.loaders import LoadingBar

def download_task(progress_updater):
    for step in range(101):
        # Update progress percentage instantly
        progress_updater.update(step)
        time.sleep(0.02)

loader = LoadingBar(title_text="Downloading Package Data", bar_color=["cyan", "blue"])
loader.run(download_task, progress_updater=True)
```

---

## Helper Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `ShowLoading()` | `ShowLoading(target, *args, timeout=80, **kwargs)` | Instantiates `LoadingBar` and runs `target` immediately. |
| `ShowSpinner()` | `ShowSpinner(target, *args, timeout=80, **kwargs)` | Instantiates `Spinner` and runs `target` immediately. |

---

## Usage Examples

### 1. Spinner with Decorator Pattern

```python
import time
from dvs_printf.loaders import Spinner

@Spinner(title="Fetching Remote Artifacts", style="dots", spinner_color="cyan").decorator
def fetch_data():
    time.sleep(2)
    return {"status": "success"}

data = fetch_data()
```

### 2. LoadingBar with Custom Borders & Gradient

```python
import time
from dvs_printf.loaders import LoadingBar

def heavy_computation(progress_updater):
    for i in range(1, 101):
        progress_updater.update(i)
        time.sleep(0.01)

loader = LoadingBar(
    title_text="Processing Heavy Matrix",
    bar_borders="[]",
    bar_color=["#FF0000", "#FFFF00", "#00FF00"],
    title_color="cyan"
)
loader.run(heavy_computation, progress_updater=True)
```

### 3. POSIX I/O Suppression (`SafeIOSuppressor`) with Heavy C-Extension Output

```python
import time
import sys
from dvs_printf.loaders import Spinner

def heavy_c_extension_task():
    # Simulates a heavy C++ / PyTorch / C-extension library writing directly to FD 1 & 2
    for step in range(5):
        # Even direct stdout writes bypassing Python sys.stdout are safely silenced to /dev/null
        sys.stdout.write(f"Raw C-level debug log line {step}\n")
        sys.stdout.flush()
        time.sleep(0.3)
    return "Computation Complete"

# 'suppress_io="auto"' uses low-level os.dup2 in standard terminals 
# and automatically falls back to stream mode in Jupyter/Pytest environments.
spinner = Spinner(
    title="Running PyTorch Model Inference", 
    style="dots", 
    spinner_color="cyan",
    suppress_io="auto"
)
result = spinner.run(heavy_c_extension_task)
print(f"Result: {result}")
```

---
*© 2026 dvs-printf Team • Smooth Background Tasks*
