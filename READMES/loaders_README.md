# Loaders & Spinners: Multi-Threaded Progress (`dvs_printf.loaders`)

The `dvs_printf.loaders` module provides professional-grade tools for visual feedback during background tasks, featuring **Aggressive I/O Suppression** and non-blocking dual-thread execution.

---

## Dual-Thread Architecture & I/O Suppression

```
[ Main Thread ]
      │
      ├──> Worker Thread (MyThread: Executes target function)
      │
      └──> Animation Thread (Renders spinner/loader frames)
                │
                ▼ (Polls task_completed Event)
```

1. **Dual-Thread Execution:** A worker thread (`MyThread`) executes background functions, while a separate animation thread renders high-FPS visual updates.
2. **I/O Suppression:** Redirects standard output/error stream file descriptors (`os.dup2`) to a null stream during animation, preventing stray `print()` calls from breaking UI layout.

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

---
*© 2026 dvs-printf Team • Smooth Background Tasks*
