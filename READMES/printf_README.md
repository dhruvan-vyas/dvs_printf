# The printf() Function: Animated Output Core (`dvs_printf.printf`)

The `printf()` function is the heart of the `dvs_printf` module. It is a high-performance replacement for Python's built-in `print()`, designed to transform static text into expressive, animated terminal output.

---

## Exhaustive `printf()` Parameter Reference

```python
from dvs_printf import printf

printf(
    *values: object,
    style: str | None = 'typing',
    speed: int | float | None = 3,
    delay: int | float | None = 0,
    stay: bool | None = True,
    getmat: str | bool | None = False,
    attrs: list[str] = [],
    color: tuple | str | Colors | None = None,
    background_color: tuple | str | None = None,
    reset_color: bool | None = True,
    **kwargs
) -> None
```

### Parameter Breakdown

| Parameter | Type | Default | Deep Technical Explanation |
| :--- | :--- | :--- | :--- |
| `*values` | `object` | *Required* | Positional arguments (strings, lists, dictionaries, tuples, matrices) to be animated.<br>Non-string objects are automatically converted to clean multiline text streams via the `list_of_str()` generator. |
| `style` | `str` | `'typing'` | Animation style key. Controls character rendering pattern (`typing`, `glitch`, `matrix`, `matrix2`, `headline`, `async`, `wave`, `fire`, `newsline`, `gunshort`, `snip`, `silverfade`, `scatter`, `blink`, `f2b`, `b2f`). Pass `"help"` to display module documentation. |
| `speed` | `int \| float` | `3` | Speed multiplier.<br>• Values `1` to `6`: `1` is slowest, `6` is fastest.<br>• Value `7`: Instantaneous high-speed output.<br>Character delay $\Delta t$ is calculated as `speed_key[style] / speed`. |
| `delay` | `int \| float` | `0` | Pause duration in seconds after rendering or between line transitions. Automatically normalized using `abs(delay)`. |
| `stay` | `bool` | `True` | Controls output persistence.<br>• `True`: Output remains visible on screen.<br>• `False`: Line is erased (`\x1b[2K`) after animation completes. |
| `getmat` | `str \| bool` | `False` | Array/matrix serialization formatting mode.<br>• `True`: Formats NumPy, TensorFlow, PyTorch, Pandas objects line-by-line.<br>• `"show"`: Appends class name, data type (`dtype`), and shape (`shape`) metadata lines beneath output. |
| `attrs` | `list[str]` | `[]` | List of ANSI text attributes (`["bold"]`, `["italic"]`, `["underline"]`, `["reverse"]`, `["strike"]`, `["hidden"]`). |
| `color` | `tuple \| str \| Colors` | `None` | Foreground color scheme. Accepts color name (`"cyan"`), HEX (`"#FF0000"`), RGB tuple `(255, 0, 0)`, HSL/HSV/CMYK strings, or a `Colors` gradient instance. |
| `background_color` | `tuple \| str` | `None` | Background color scheme. Accepts color name, HEX string, RGB tuple, or list of background gradient colors. |
| `reset_color` | `bool` | `True` | Appends ANSI reset code (`\033[0m`) at end of animation to prevent color leakage into standard terminal text. |

---

## Available Animation Styles (20+ Styles)

| Style Key | Description | Category | Base Delay Constant |
| :--- | :--- | :--- | :---: |
| `"typing"` | Sequential character-by-character typewriter animation (default) | Core | `0.08 s` |
| `"async"` | High-speed simulated parallel line rendering | Core | `0.045 s` |
| `"headline"` | Centered bold section heading animation | Alignment | `0.08 s` |
| `"center"` | Horizontally centered static line layout | Alignment | `0.08 s` |
| `"left"` / `"right"` | Aligned text slide animations | Alignment | `0.032 s` |
| `"glitch"` | Electronic noise and random character distortion | Advanced | `0.05 s` |
| `"matrix"` / `"matrix2"` | Iconic falling digital code streams and rain | Advanced | `0.03 s` |
| `"scatter"` | Fragmented characters coalescing into final string | Advanced | `0.30 s` |
| `"newsline"` | Scrolling ticker-tape bracketed animation | Advanced | `0.18 s` |
| `"silverfade"` | Multi-stage grayscale fading text effect | Cinematic | `0.05 s` |
| `"gunshort"` | High-velocity character firing motion effect | Motion | `0.064 s` |
| `"snip"` | Horizontal scissors trimming motion effect | Motion | `0.016 s` |
| `"wave"` | Oscillating case-swapping ripple effect | Motion | `0.05 s` |
| `"fire"` | Flickering intense color glow effect | Motion | `0.05 s` |
| `"blink"` | Rapid visibility flash animation | Motion | `0.05 s` |
| `"f2b"` / `"b2f"` | Front-to-back and back-to-front sliding persistence | Motion | `0.05 s` |

---

## Code Examples

### 1. Simple Animated Printing
```python
from dvs_printf import printf, Colors

# Print typewriter text in green
printf("Connecting to remote server...", style="typing", color="green", speed=4)

# Glitch animation with gradient foreground
gradient_theme = Colors("cyan", "magenta", angle=45)
printf(
    "CRITICAL SYSTEM WARNING",
    style="glitch",
    speed=5,
    color=gradient_theme,
    attrs=["bold"]
)
```

### 2. Complex Data Matrix Formatting (`getmat`)
`printf` formats nested structures, lists, dictionaries, NumPy arrays, PyTorch tensors, and Pandas dataframes:

```python
from dvs_printf import printf

matrix_data = [
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
]

printf("Transformation Matrix:", matrix_data, style="typing", getmat="show", color="cyan")
```

---

## Internal Architecture

1. **Validation Gate:** Validates arguments (`_validate_style`, `_validate_speed`, `_validate_delay`, `_validate_attrs`, `_validate_getmat`) before execution.
2. **Dynamic Speed Calc:** Speed is calculated as `target_constant / speed_multiplier`. Different styles have tuned constants so they look natural at the same speed level.
3. **Lazy Style Loading:** Logic for complex styles (like `matrix`, `glitch`, `wave`) resides in `_other_styles.py` and is dynamically imported via `load_function()` only when explicitly called.
4. **ANSI Buffering:** Uses low-level `sys.stdout.write` and `flush` directly for high-frequency updates, minimizing CPU overhead compared to standard Python `print()`.

---
*© 2026 dvs-printf Team • Professional Console Animation*