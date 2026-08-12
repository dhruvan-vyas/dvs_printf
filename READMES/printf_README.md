# The printf(...) Function: Animated Output Core (`dvs_printf.printf`)

The `printf()` function is the heart of the `dvs_printf` module. It is a high-performance replacement for Python's built-in `print()`, designed to transform static text into expressive, animated terminal output.


## Exhaustive `printf()` Functions & Parameter Reference

The printf function allow users to apply various animation styles to their values. 
Supports different data types (**string, int, float, list, set, tuple, dict, Any,** ...) with 
(**custom object**) and classes (**numpy, tensorflow, pytorch, pandas**) as input. 
Users can choose from a range of animation styles, including **`typing, Async, headlines, Center, Left, right`** and more. 
Customizable parameters include **`style, speed, delay, getmat, stay, color, background_color, reset_color, attrs.`** 


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



### **values**
values stream can be anything like
`(string, int, float, list, set, tuple, dict)`
and you can give multiple input as any-data-type.
animation workd separately for each element given, 
and for each item in given iterable.

```python              
printf(str, list, [tuple, set], dict, int, float, any,...)
```     

### **style**

Style defines different types of console-based output animation.<br>
Each style type works differently according to the description below.

https://github.com/user-attachments/assets/6efb18df-5181-4423-bf65-52f096ec9b3f

```python
style: ["typing", "async", "headline", "newsline", "mid", "gunshort", "snip", 
    "left", "right", "center", "centerAC", "centerAL", "centerAR", "fire", 
    "wave", "blink", "scatter", "matrix", "matrix2", "silverfade", "glitch", "f2b", "b2f", "help"]
``` 
```python
printf(values, style="center 30%")
``` 

### **Available Animation Styles (20+ Styles)**
| Style Key | Description | Category | Base Delay Constant |
| :--- | :--- | :--- | :---: |
| `"typing"` | Sequential character-by-character typewriter animation (default) | Core | `0.08 s` |
| [`"async"`](./special_styles_README.md#1-async-style) | High-speed simulated parallel line rendering (supports `"async <num_lines>"`) | Core | `0.045 s` |
| `"headline"` | Centered bold section heading animation | Alignment | `0.08 s` |
| [`"center"`](./special_styles_README.md#2-center--alignment-styles) | Horizontally centered line layout (supports `centerAL`, `centerAR`, `centerAC`, `center <pos>%`) | Alignment | `0.08 s` |
| `"left"` / `"right"` | Aligned text slide animations | Alignment | `0.032 s` |
| [`"glitch"`](./special_styles_README.md#3-glitch-distortion-style) | Electronic noise and character distortion (supports `glitch<char>` like `glitch*`) | Advanced | `0.05 s` |
| `"matrix"` / `"matrix2"` | Iconic falling digital code streams and rain | Advanced | `0.03 s` |
| `"scatter"` | Fragmented characters coalescing into final string | Advanced | `0.30 s` |
| `"newsline"` | Scrolling ticker-tape bracketed animation | Advanced | `0.18 s` |
| [`"silverfade"`](./special_styles_README.md#4-silver-fade-style) | Multi-stage grayscale fading text effect (supports `silverfade <iterations>`) | Cinematic | `0.05 s` |
| `"gunshort"` | High-velocity character firing motion effect | Motion | `0.064 s` |
| `"snip"` | Horizontal scissors trimming motion effect | Motion | `0.016 s` |
| `"wave"` | Oscillating case-swapping ripple effect | Motion | `0.05 s` |
| `"fire"` | Flickering intense color glow effect | Motion | `0.05 s` |
| `"blink"` | Rapid visibility flash animation | Motion | `0.05 s` |
| `"f2b"` / `"b2f"` | Front-to-back and back-to-front sliding persistence | Motion | `0.05 s` |

---

## Special Parameterized Styles (Advanced)

`printf()` supports special **inline-parameterized styles**, where custom control parameters (such as line counts, alignment percentages, distortion mask characters, and fade iterations) are attached directly to the style string key.

For complete documentation, video demonstrations, and comprehensive code examples for each special style, see the dedicated [**Special Parameterized Styles Guide**](./special_styles_README.md).

| Special Style | Parameter Syntax | Example Style String | Description |
| :--- | :--- | :--- | :--- |
| [**`async`**](./special_styles_README.md#1-async-style) | `async` or `async <num_lines>` | `"async 8"` | Renders multiple lines simultaneously line-by-line. |
| [**`center` / Alignment**](./special_styles_README.md#2-center--alignment-styles) | `center`, `center<align>`, `center <pos>%` | `"centerAL 30%"`, `"centerAR 70%"` | Custom horizontal terminal alignment & percentage-based positioning. |
| [**`glitch`**](./special_styles_README.md#3-glitch-distortion-style) | `glitch` or `glitch<char>` | `"glitch*"`, `"glitch#"` | Random character distortion effect with customizable mask character. |
| [**`silverfade`**](./special_styles_README.md#4-silver-fade-style) | `silverfade` or `silverfade <iterations>` | `"silverfade 5"` | Multi-pass shimmering silver gradient sweep effect. |

---

### **speed**
Speed defines `printf`'s animation rendering speed multiplier. `Default speed is 3`, and you can set `speed` from `1` to `6` or `7`.
Each style's rendering speed is calculated as `speed_key[style] / speed`.

https://github.com/user-attachments/assets/631e97d4-e615-4af8-8960-54915001c313

* **1** = *Very Slow*
* **2** = *Slow*
* **3** = *Medium* *(default)*
* **4** = *Medium Fast*
* **5** = *Fast*
* **6** = *Very Fast*
* **7** = *Super Fast* *(ideal for very long text streams)*

```python
printf("Slow typewriter effect", speed=1)
printf("High speed stream", speed=6)
```

---

### **delay**
Specifies the pause duration (in seconds) after rendering each line or between line transitions. Automatically normalized using `abs(delay)`.

```python
# Pause for 1.5 seconds after printing each line
printf("Step 1 Complete", "Step 2 Complete", delay=1.5)
```

---

### **stay**
Controls output persistence.
- **`True`** *(default)*: The printed output remains visible on the terminal screen (`\n`).
- **`False`**: The rendered output line is cleared (`\x1b[2K` ANSI line erase) after animation completes.

```python
# Temporary status line that disappears when done
printf("Buffering data...", stay=False, speed=5)
printf("Done!", stay=True)
```

---

### **getmat**
Configures matrix and complex structure formatting for data science types (`NumPy`, `PyTorch`, `TensorFlow`, `Pandas`, nested lists/dicts).
- **`False`** *(default)*: Standard string conversion.
- **`True`**: Formats matrices and collections line-by-line without string truncation.
- **`"show"`**: Formats the matrix line-by-line **and** appends metadata lines displaying the object's class name, data type (`dtype`), and shape dimensions (`shape`).

```python
import numpy as np

arr = np.ones((3, 3))

# Print matrix with metadata info header
printf(arr, getmat="show", color="cyan")
```

---

### **attrs**
A list of text attribute strings applied to the output text during animation.

#### Supported Attributes:
- `"bold"` — Emboldened text
- `"italic"` — Italicized text
- `"underline"` — Underlined text
- `"reverse"` — Reverse video (swaps foreground and background)
- `"strike"` — Strikethrough text
- `"hidden"` — Invisible text

```python
printf("CRITICAL ALERT", attrs=["bold", "underline"], color="red")
```

---

### **color** & **background_color**
- **`color`** (`tuple | str | Colors | None = None`): Sets foreground text color scheme.
- **`background_color`** (`tuple | str | None = None`): Sets background color behind text.

Accepts:
- **Color Name:** `"red"`, `"cyan"`, `"lime"`, `"gold"`, `"scarlet"`, etc. (345+ named colors).
- **HEX String:** `"#FF0055"`, `"#00AEFF"`
- **RGB Tuple:** `(255, 165, 0)`
- **`Colors` Object / Gradient:** Pass a dynamic gradient or degree-based angle palette created via `Colors()`.

```python
from dvs_printf import printf, Colors

# Simple color name & HEX background
printf("System Ready", color="lime", background_color="#1A1A1A")

# Angular RGB Gradient palette
theme = Colors("cyan", "magenta", angle=45)
printf("GRADIENT HEADER", color=theme, attrs=["bold"])
```

---

### **reset_color**
Controls whether the ANSI reset code (`\033[0m`) is automatically appended at the end of the animated output.
- **`True`** *(default)*: Appends ANSI reset code to prevent color and attribute leakage into subsequent console text.
- **`False`**: Keeps ANSI style formatting active for downstream console output.

```python
# Preserve color for subsequent standard print statements
printf("Warning: ", color="yellow", reset_color=False)
print("Continue with caution.") # Prints in yellow
```

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

printf("Transformation Matrix:", matrix_data, style="async", getmat="show", color="cyan")
```

# Internal Architecture & High-Performance Design

1. **Low-Latency Generator Engine (~16,000ns Startup):** Operates on lazy generator evaluation (`yield` streams via `list_of_str()`). Character rendering begins in under 16,000 nanoseconds (~16 µs) regardless of payload size or data structure complexity.
2. **Safe-Area Console Bounds Detection:** Dynamically queries terminal dimensions (`os.get_terminal_size()`) at runtime, auto-adjusting safe margins to prevent output wrapping corruption when animating large matrices, deeply nested collections, NumPy arrays, PyTorch tensors, or Pandas DataFrames.
3. **Multi-Line & Alignment Processing:** Supports complex horizontal alignments (`center`, `headline`, `left`, `right`) and inline multi-line animations simultaneously.
4. **Global State Pre-Configuration Caching (`Init` / `dvs_printf.init`):** Uses a thread-safe singleton pre-configuration caching layer. Developers can configure visual settings once at application startup, allowing downstream `printf()` invocations to inherit profiles seamlessly:

```python
from dvs_printf import Init, Colors

# Pre-configure application-wide animation profile
theme = Init(style="wave", speed=4, colors=Colors("cyan", "magenta"), attrs=["bold"])

# All subsequent calls inherit global configuration
theme.printf("Service Online")
theme.printf("Database Connected")
```

5. **Validation Gate:** Validates arguments (`_validate_style`, `_validate_speed`, `_validate_delay`, `_validate_attrs`, `_validate_getmat`) before execution.
6. **Dynamic Speed Calibration:** Speed is calculated as `target_constant / speed_multiplier`. Different animation styles use tuned base constants so visual movement feels natural at any speed setting.
7. **Lazy Style Loader:** Complex animation modules (`matrix`, `glitch`, `silverfade`) reside in `_other_styles.py` and are imported on-demand via `load_function()`, keeping initial package startup instantaneous.
8. **ANSI Direct-Write Buffering:** Bypasses high-level Python formatting by writing directly to `sys.stdout.write` + `flush`, eliminating string allocation churn per frame.

---
*© 2026 dvs-printf Team • Professional Console Animation*