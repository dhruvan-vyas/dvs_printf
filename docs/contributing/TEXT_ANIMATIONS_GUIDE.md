# Text Animations Contributor Guide (`dvs_printf.printf`)

This guide explains the architecture of the `printf` animation engine and provides technical instructions for implementing new streaming text animation styles and preset configurations.

---

## 1. Animation Engine Architecture

```
printf(*values, style="my_style", speed=3)
                 │
                 ▼
     [ Input Normalization ]
    (list_of_str generator)
                 │
                 ▼
  [ Is Style Core or Lazy-Loaded? ]
     ┌───────────┴───────────┐
     ▼                       ▼
 Core Style             Lazy-Loaded Style
(_core_styles.py)       (_other_styles.py via load_function)
     │                       │
     └───────────┬───────────┘
                 ▼
    [ Animation Loop Execution ]
   (Writes ANSI sequences to sys.stdout)
```

---

## 2. Exhaustive `printf()` Parameter Reference

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

| Parameter | Type | Default | Deep Technical Explanation |
| :--- | :--- | :--- | :--- |
| `*values` | `object` | *Required* | Positional arguments (strings, lists, dictionaries, tuples, matrices) to be animated.<br>Converted via the `list_of_str()` generator. |
| `style` | `str` | `'typing'` | Animation style key (`typing`, `glitch`, `matrix`, `matrix2`, `headline`, `async`, `wave`, `fire`, `newsline`, `gunshort`, `snip`, `silverfade`, `scatter`, `blink`, `f2b`, `b2f`). |
| `speed` | `int \| float` | `3` | Speed multiplier (1 to 6, or 7 for instant output). Character delay $\Delta t = \text{speed\_key}[style] / \text{speed}$. |
| `delay` | `int \| float` | `0` | Pause duration in seconds after rendering or between line transitions (`abs(delay)`). |
| `stay` | `bool` | `True` | `True` to keep output visible on screen; `False` to erase line (`\x1b[2K`) after animation completes. |
| `getmat` | `str \| bool` | `False` | Array/matrix serialization formatting mode (`True`, `False`, `"show"`). |
| `attrs` | `list[str]` | `[]` | List of ANSI text attributes (`["bold"]`, `["italic"]`, `["underline"]`, `["reverse"]`, `["strike"]`, `["hidden"]`). |
| `color` | `tuple \| str \| Colors` | `None` | Foreground color scheme (name, HEX, RGB tuple, HSL/HSV/CMYK, or `Colors` instance). |
| `background_color` | `tuple \| str` | `None` | Background color scheme (name, HEX, RGB tuple, or list of background gradient colors). |
| `reset_color` | `bool` | `True` | Appends ANSI reset code (`\033[0m`) at end of animation to prevent color leakage. |

---

## 3. Exhaustive `Init` Class Parameter Reference

```python
class Init:
    def __init__(
        self,
        style: str | None = 'typing', 
        speed: int | float | None = 3, 
        delay: int | float | None = 0,  
        stay: bool | None = True,
        attrs: list[str] | None = [],
        colors: Colors | None = None,
        getmat: bool | str | None = False,
    ): ...
```

| Property | Type | Default | Property Setter Validation & Description |
| :--- | :--- | :--- | :--- |
| `style` | `str` | `'typing'` | Validates against `_validate_style(value)` in `_validator.py`. |
| `speed` | `int \| float` | `3` | Validates against `_validate_speed(value)` (1 to 7). |
| `delay` | `int \| float` | `0` | Validates against `_validate_delay(value)`. |
| `stay` | `bool` | `True` | Sets default persistence behavior for `Init.printf()`. |
| `attrs` | `list[str]` | `[]` | Validates against `_validate_attrs(value)`. |
| `colors` | `Colors` | `None` | Validates that input is `None` or an instance of `Colors` class. Raises `ColorsValueError` otherwise. |
| `getmat` | `bool \| str` | `False` | Validates against `_validate_getmat(value)`. |

---

## 4. How to Implement a New Animation Style

Follow these 5 steps to add a new animation style (e.g., `"pulse"`):

### Step 1: Write the Style Function in `_other_styles.py`

```python
from time import sleep
from .console import _write, _flush
from ._printf_helper import modifyed

def _pulse(values: list[str]) -> None:
    speed = modifyed.speed
    stay_str = modifyed._stay

    for line in values:
        _write(f"\r\033[2K\033[2m{line}\033[0m")
        _flush()
        sleep(speed * 2)

        _write(f"\r\033[2K\033[1m{line}\033[0m{stay_str}")
        _flush()
        sleep(speed)
```

### Step 2: Register in `map_import_func` (`__printf__.py`)

```python
map_import_func = {
    # Existing styles...
    "pulse": "_pulse",
}
```

### Step 3: Set Base Speed Constant in `speed_key` (`__printf__.py`)

```python
speed_key = {
    # Existing speeds...
    "pulse": 0.05,
}
```

### Step 4: Register in `available_styles` (`_printf_helper.py`)

```python
available_styles = [
    'typing', 'headline', 'async', 'center', 'left', 'right',
    'wave', 'fire', 'scatter', 'blink', 'mid', 'gunshort',
    'snip', 'matrix', 'matrix2', 'silverfade', 'glitch',
    'newsline', 'b2f', 'f2b', 'help',
    'pulse'
]
```

### Step 5: Document & Add Unit Test

1. Add your style description to `READMES/printf_README.md`.
2. Add unit test under `tests/test__Functionlity/test_printf.py`.
