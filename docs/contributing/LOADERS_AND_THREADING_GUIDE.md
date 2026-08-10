# Loaders & Threading Contributor Guide (`dvs_printf.loaders`)

This guide explains the multi-threaded architecture of the `loaders` subsystem and provides technical instructions for contributing new progress bar styles, spinner animation frames, parameter options, and thread synchronization features.

---

## 1. Multi-Threaded Architecture Overview

```
[ Consumer Call: loader.run(target_func, *args) ]
                       │
                       ├─────────────────────────────────────┐
                       ▼                                     ▼
        [ Worker Thread: MyThread ]            [ Animation Thread ]
        Executes target_func(*args)            Renders Spinner / LoadingBar
        Sets result or exception               Polls task_completed Event
                       │                                     │
                       └──────────────────┬──────────────────┘
                                          ▼
                             [ Join & Post-Check ]
                       Re-raises target exception or returns result
```

---

## 2. Exhaustive Parameter Reference

### `LoadingBar` & `LoadingBarConfig` Parameters

| Parameter | Type | Default | Deep Technical Explanation |
| :--- | :--- | :--- | :--- |
| `target` | `Callable` | *Required in `.run()`* | Background function to execute concurrently in `MyThread`. |
| `args` | `Iterable[Any]` | `()` | Positional arguments passed directly to `target(*args)`. |
| `kwargs` | `Mapping[str, Any]` | `{}` | Keyword arguments passed directly to `target(**kwargs)`. |
| `timeout` | `int \| float \| None` | `80` | Maximum execution time in seconds before raising `TimeOutError`. |
| `title_text` | `str` | `"Loading"` | Message string displayed alongside or above progress bar. |
| `title_color` | `ColorInput` | `(255, 255, 255)` | Color applied to `title_text`. |
| `style` | `str` | `"grow"` | Visual bar component style (`"grow"`, `"line"`, `"growvertical"`, `"mesh"`, `"numbers"`, `"spinner"`). |
| `bar_color` | `ColorInput \| GredinatInput` | `"green"` | Color for filled bar blocks. Accepts single color or gradient color list (e.g. `["pink", "orange"]`). |
| `unfilled_bar_color` | `ColorInput` | `"#2B2B2B"` | Color for unfilled bar track characters. |
| `bar_borders` | `str \| None` | `None` | Custom border characters surrounding bar (e.g. `"-+"`, `"[]"`). |
| `bar_borders_color` | `ColorInput` | `"#00aeff"` | Color applied to border characters. |
| `percentage_color` | `ColorInput` | `"#ea9329"` | Color applied to numeric percentage readout (`XX.XX%`). |
| `timing_color` | `ColorInput` | `"#00aeff"` | Color applied to elapsed time readout (`in X.Xs`). |
| `error_color` | `ColorInput` | `"scarlet"` | Color applied to error messages if `target` raises an exception. |
| `inject_progress` / `progress_updater` | `bool` | `False` | Injects thread-safe `ProgressUpdater` instance into `kwargs['progress_updater']`. |
| `show_gradient_anyway` | `bool` | `False` | Forces 24-bit gradient bar calculation even in non-TrueColor environments. |
| `grid_rotation_speed` | `int` | `1` | Speed multiplier (1 to 10) for angular gradient shift animation. |
| `stay` | `bool` | `True` | Keeps final progress bar visible (`True`) or erases line (`False`) upon completion. |
| `FPS` | `int \| None` | `None` | Frames per second refresh frequency for animation loop. |
| `full_screen_mode` | `bool \| None` | `False` | Stretches progress bar across full terminal width. |

### `Spinner` & `SpinnerConfig` Parameters

| Parameter | Type | Default | Deep Technical Explanation |
| :--- | :--- | :--- | :--- |
| `target` | `Callable` | *Required in `.run()`* | Background function to execute concurrently in `MyThread`. |
| `args` | `Iterable[Any]` | `()` | Positional arguments passed to `target(*args)`. |
| `kwargs` | `Mapping[str, Any]` | `{}` | Keyword arguments passed to `target(**kwargs)`. |
| `timeout` | `int \| float \| None` | `80` | Maximum execution time in seconds before raising `TimeOutError`. |
| `style` | `SpinnerFrems \| str` | `"arrow"` | Spinner frame sequence preset (e.g. `"dots"`, `"arrow"`, `"moon"`, `"shark"`, `"pong"`, `"bounce"`, `"line"`). |
| `animation_position` | `str` | `"before"` | Alignment of spinner animation relative to title text (`"before"`, `"after"`, `"dual"`). |
| `title` | `str` | `"Loading"` | Message string displayed next to spinner animation. |
| `title_color` | `ColorInput` | `None` | Color applied to `title` text. |
| `spinner_color` | `ColorInput` | `None` | Color scheme applied to spinner animation frames. |
| `attrs` | `list[str]` | `[]` | Text attributes applied to title (`["bold"]`, `["italic"]`). |
| `show_timer` | `bool` | `True` | Displays elapsed execution time `(X.Xs)` next to spinner. |
| `reversed_timer` | `bool` | `False` | Displays countdown remaining time `(X.Xs remaining)` based on timeout. |
| `show_progress` | `bool` | `True` | Displays percentage progress readout `XX.X%`. |
| `inject_progress` | `bool` | `False` | Injects `ProgressUpdater` into `target` kwargs for manual progress updates. |
| `stay` | `bool` | `True` | Keeps final completion line visible (`True`) or erases line (`False`). |
| `final_message` | `str \| None` | `None` | Custom text string displayed upon successful completion. |
| `final_message_color` | `ColorInput` | `"springgreen"` | Color for success message. |
| `error_message` | `str \| None` | `None` | Custom text string displayed if `target` raises an exception. |
| `error_message_color` | `ColorInput` | `"scarlet"` | Color for error message. |
| `progress_color` | `ColorInput` | `"gray"` | Color applied to percentage progress text. |
| `timer_color` | `ColorInput` | `"pink"` | Color applied to timer readout. |

---

## 3. How `ProgressUpdater` Works

When `progress_updater=True` (or `inject_progress=True`) is passed to `loader.run()`, `dvs_printf` injects a thread-safe `ProgressUpdater` instance:

```python
class ProgressUpdater:
    def __init__(self, value: float = 0.0):
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, val: float) -> None:
        self._value = min(100.0, max(0.0, float(val)))

    def update(self, val: float) -> None:
        self.value = val
```

---

## 4. How to Add New Spinner Frame Presets (`SpinnerFrems`)

Spinner frame sequences are stored in `dvs_printf/loaders/spinner_frems.py`.

### Step 1: Define the Frame Sequence

Open `dvs_printf/loaders/spinner_frems.py` and add your entry to `SPINNERS_FREMS`:

```python
SPINNERS_FREMS["pulse_dot"] = Spinner_Frem((
    100,  # Refresh interval in milliseconds
    ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]  # Frame strings
))
```

### Step 2: Register Class Attribute in `SpinnerFrems`

```python
class SpinnerFrems:
    pulse_dot = "pulse_dot"
```

---

## 5. Thread Synchronization & Exception Guidelines

1. **Completion Signaling:** Always call `self.task_completed.set()` to signal the animation thread to stop when the target function finishes or raises an exception.
2. **Preserving Stack Traces:** Store worker thread exceptions in `self.exception` and re-raise `self.exception` on the main thread after joining worker threads.
3. **Safe I/O Restoration:** File descriptor operations (`os.dup2`, `sys.stdout`) must be enclosed inside `try...finally` blocks to restore standard console streams even if background tasks crash.
