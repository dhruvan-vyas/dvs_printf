# Init & Presets: Global Configuration (`dvs_printf.Init`)

The `Init` module manages global default settings and execution parameters for the `dvs_printf` library. It allows developers to define a consistent look and feel for an entire application in one central location.

---

## Why use `Init`?

Instead of passing `style`, `speed`, and `color` to every single `printf` call, you can create a configured `Init` instance and reuse it across your application.

```python
from dvs_printf import Init, Colors

# Define global theme
theme = Init(
    style="wave",
    speed=5,
    colors=Colors("cyan", "white"),
    attrs=["bold"]
)

# Use it throughout your app
theme.printf("System initialized.")
theme.printf("Loading modules...")
```

---

## Singleton Architecture

The `Init` class implements the Thread-Safe Singleton pattern. Instantiating `Init()` multiple times across different modules returns the identical global instance configuration.

```python
from dvs_printf import Init

config1 = Init()
config2 = Init()

assert config1 is config2  # True
```

---

## Exhaustive `Init` Class Parameter Reference

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

### Parameter Breakdown

| Property / Parameter | Type | Default | Property Setter Validation & Description |
| :--- | :--- | :--- | :--- |
| `style` | `str` | `'typing'` | Validates against `_validate_style(value)` in `_validator.py`. Accepts all valid animation style keys (`typing`, `wave`, `glitch`, `matrix`, etc.). |
| `speed` | `int \| float` | `3` | Validates against `_validate_speed(value)`. Accepts values `1` to `6` (or `7` for instant). |
| `delay` | `int \| float` | `0` | Validates against `_validate_delay(value)`. Pause duration in seconds. |
| `stay` | `bool` | `True` | Sets default persistence behavior for `Init.printf()` calls (`True` to keep output, `False` to clear line). |
| `attrs` | `list[str]` | `[]` | Validates against `_validate_attrs(value)`. Text attributes (`["bold"]`, `["italic"]`, etc.). |
| `colors` | `Colors` | `None` | Validates that input is `None` or an instance of the `Colors` class. Raises `ColorsValueError` if non-Colors object is passed. |
| `getmat` | `bool \| str` | `False` | Validates against `_validate_getmat(value)`. Matrix array formatting mode (`True`, `False`, `"show"`). |

---

## Merging Defaults & Overrides

One of the most powerful features of `Init.printf()` is the ability to override specific global settings for a one-off call while retaining all other default parameters.

```python
from dvs_printf import Init, Colors

theme = Init(style="wave", speed=4, colors=Colors("cyan"))

# Uses default 'wave' style and 'cyan' color
theme.printf("Standard system message.")

# Overrides 'wave' with 'glitch' and color with 'red' just for this call
theme.printf("CRITICAL SYSTEM ERROR", style="glitch", colors=Colors("red"))
```

---

## Deprecation Notice

The lowercase `init` class is deprecated in favor of the capitalized `Init` class.

```python
from dvs_printf import init  # WARNING: Deprecated alias

# Use the capital version instead:
from dvs_printf import Init
```

The `Init` class (capital 'I') is more robust, supports property-based validation, and is the standard for version 3.1.0+.

---
*© 2026 dvs-printf Team • Scale with Consistency*
