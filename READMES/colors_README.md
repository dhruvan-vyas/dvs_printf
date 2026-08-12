# The Colors Module: Professional Color Management (`dvs_printf.colors`)

The `dvs_printf.colors` module is an industrial-grade color engine for terminal applications. It provides full support for **24-bit TrueColor (RGB)**, 8-bit ANSI-256, 4-bit ANSI-16, complex angular 2D gradients, and dynamic environment detection.

---

## Architecture & Pipeline Overview

```
[ User Input (HEX / RGB / HSL / HSV / CMYK / Named Color) ]
                         │
                         ▼
             [ get_RGB_values() Parser ]
                         │
                         ▼
             [ Environment Detection ]
             (console_EnvType: 1, 2, or 3)
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   [ 24-bit TrueColor ] [ 8-bit 256-Color ] [ 4-bit 16-Color ]
   \033[38;2;R;G;Bm     \033[38;5;Nm        \033[3Xm
```

---

## Environment Intelligence: `console_EnvType` & Terminal Support

The module real-time adapts its ANSI color codes based on `console_EnvType`.

| `console_EnvType` | Level | Support Detail | Terminal Emulators & Environment Compatibility | Result |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **TrueColor** | 24-bit RGB (16.7M colors) | Linux (GNOME Terminal, Konsole, Alacritty, Kitty), macOS (Terminal.app, iTerm2), Windows Terminal, VS Code Integrated Terminal, GitHub Actions CI. | Full 24-bit cinematic RGB output. |
| **2** | **ANSI-256** | 8-bit palette (256 colors) | xterm-256color terminals, tmux, screen, legacy Linux terminals. | Downsampled 256-color palette index. |
| **3** | **ANSI-16** | 4-bit standard colors | Windows Command Prompt (`cmd.exe`), basic xterm, legacy serial consoles. | Standard 16 ANSI color codes (30-37 / 90-97). |
| **4** | **No Color** | Plain text / Monochrome | Environments with `NO_COLOR` set or non-interactive pipes/redirects. | Plain un-styled text output. |

---

## Exhaustive `Colors` Class Parameter Reference

```python
class Colors:
    def __init__(
        self,
        *colors: ColorInput | GredinatInput | GradientStyles,
        background: ColorInput | List[ColorInput] | bool | None = None,
        angle: int | None = None,
        style: GradientStyles | None = None,
    ): ...
```

### Parameter Breakdown

| Parameter | Type | Default | Deep Technical Explanation |
| :--- | :--- | :--- | :--- |
| `*colors` | `ColorInput \| GredinatInput \| GradientStyles` | *Optional* | Positional arguments defining foreground colors.<br>• **Single Color:** Accepts HEX string (`"#FF0000"`), RGB tuple `(255,0,0)`, named color (`"scarlet"`), HSL (`"hsl: 120,1.0,0.5"`), HSV (`"hsv: 240,1,1"`), or CMYK (`"cmyk: 0,1,1,0"`).<br>• **Gradient:** Pass multiple color arguments (e.g., `Colors("red", "blue")`) or a list of colors (e.g., `Colors(["red", "yellow", "blue"])`). |
| `background` | `ColorInput \| List[ColorInput] \| bool \| None` | `None` | Specifies background color or background gradient.<br>• **`None` / `False`:** No background color is applied.<br>• **`True`:** Background mode. Applies the foreground colors as background and resets foreground.<br>• **Single Color:** Applies a static background color.<br>• **List of Colors:** Applies a background gradient across the character grid. |
| `angle` | `int \| None` | `None` | Angular direction in degrees (`0°` to `360°`) for 2D character-grid gradient calculation.<br>• `0°`: Horizontal linear gradient (left to right).<br>• `90°`: Vertical linear gradient (top to bottom).<br>• `45°`: Diagonal gradient. |
| `style` | `GradientStyles \| None` | `None` | Predefined gradient palette object or style name (e.g., `GradientStyles.rainbowflame` or `"sunsetburn"`). Overrides explicit positional `*colors`. |

### Core Methods

- **`apply_to_str(value: str, reset: bool = True) -> str`**: Formats a single string. Automatically handles multiline strings (`\n`) by preserving and re-applying ANSI codes per line.
- **`apply(values: List[str], angle: int | None = None, reset: bool = True) -> Generator[List[str], None, None]`**: Yields colored character arrays line-by-line for multi-line inputs.
- **`_get_ansi_color(get_list: bool = False) -> str | list`**: Internal helper returning raw starting ANSI escape sequences.

---

## Pre-built Gradient Styles (`GradientStyles`)

`dvs_printf` includes 24 pre-built, expertly tuned gradient palettes in `dvs_printf/colors/gredinat_styles.py`:

| Preset Name | Description & Color Stops |
| :--- | :--- |
| `rainbowflame` | Full spectrum rainbow transition from red -> purple -> blue -> green -> yellow -> red. |
| `rosetwilight` | Soft twilight rose transition from deep magenta to pink and soft lavender. |
| `sunsetburn` | Intense burning sunset transition from bright yellow -> orange -> dark burnt brown -> yellow. |
| `electricdreams` | Vibrant retro synthwave purple-pink transition. |
| `neonparty` | High-contrast neon cyan -> blue -> magenta -> pink transition. |
| `cyberwave` | Cyberpunk neon red -> magenta -> blue -> cyan -> green -> yellow. |
| `seewave` (`seawave`) | Deep oceanic cyan to sea-blue aqua ripple. |
| `forestfade` | Lush forest green to light lime-green transition. |
| `midnightblues` | Deep midnight navy to royal blue and ice blue transition. |
| `loki` | Marvel's Loki emerald green, olive, and gold palette. |
| `loki_serene` | Soft purple and violet serene variant for Loki theme. |
| `tva_portal` | Temporal Variance Authority orange-gold portal theme. |
| `iron_man` | Crimson red, dark crimson, and gold armor theme. |
| `captain_america` | Navy blue, royal blue, white, and crimson shield theme. |
| `thor` | Asgardian storm blue, lightning silver, and electric gold theme. |
| `hulk` | Gamma dark green, forest green, and lime green theme. |
| `hawkeye` | Archery purple, indigo, and violet theme. |
| `black_widow` | Stealth black, charcoal grey, and crimson red theme. |
| `tva` | Retro TVA amber orange, tan, and brown theme. |
| `timedoors` | Fire orange, coral, and glowing amber timedoors theme. |
| `tempad` | Slate grey, charcoal, and orange tempad device theme. |
| `dark_purple` | Deep indigo to dark violet and purple transition. |
| `light_purple` | Soft pastel thistle to orchid and lavender transition. |
| `tea` | Earthy tea-leaf brown, beige, and warm tan palette. |

---

## Supported Named Colors List (345+ Colors)

`dvs_printf` includes built-in named color mappings directly accessible by name in `dvs_printf/colors/colors_dictionary.py`:

- **Primary & Basic Colors:** `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`.
- **Light Variants:** `lightblack`, `lightred`, `lightgreen`, `lightyellow`, `lightblue`, `lightmagenta`, `lightcyan`, `lightwhite`.
- **Dark Variants:** `darkblue`, `darkcyan`, `darkgoldenrod`, `darkgray`, `darkgreen`, `darkkhaki`, `darkmagenta`, `darkolivegreen`, `darkorange`, `darkorchid`, `darkred`, `darksalmon`, `darkseagreen`, `darkslateblue`, `darkslategray`, `darkturquoise`, `darkviolet`.
- **Deep & Bright Variants:** `deeppink`, `deepskyblue`, `deepmagenta`, `dodgerblue`, `firebrick`, `forestgreen`, `fuchsia`, `gold`, `goldenrod`, `hotpink`, `indianred`, `indigo`, `lawngreen`, `lime`, `limegreen`, `maroon`, `mediumaquamarine`, `mediumblue`, `mediumorchid`, `mediumpurple`, `mediumseagreen`, `mediumslateblue`, `mediumspringgreen`, `mediumturquoise`, `mediumvioletred`, `midnightblue`, `navy`, `olive`, `olivedrab`, `orange`, `orangered`, `orchid`, `palegoldenrod`, `palegreen`, `paleturquoise`, `palevioletred`, `peru`, `pink`, `plum`, `powderblue`, `purple`, `rebeccapurple`, `royalblue`, `saddlebrown`, `salmon`, `sandybrown`, `scarlet`, `seagreen`, `sienna`, `silver`, `skyblue`, `slateblue`, `slategray`, `springgreen`, `steelblue`, `tan`, `teal`, `thistle`, `tomato`, `turquoise`, `violet`, `wheat`, `yellowgreen`.
- **Pastel & Special Tones:** `aliceblue`, `antiquewhite`, `aqua`, `aquamarine`, `avocado`, `azure`, `babyblue`, `babylavender`, `beige`, `bisque`, `blanchedalmond`, `bluebell`, `blueviolet`, `brick`, `brown`, `bubblegum`, `burlywood`, `burntorange`, `butter`, `cadetblue`, `candy`, `carnation`, `chartreuse`, `chocolate`, `coral`, `cornflowerblue`, `cornsilk`, `cottoncandy`, `cream`, `crimson`, `dustrose`, `electricpurple`, `floralwhite`, `gainsboro`, `ghostwhite`, `greenleaf`, `honeydew`, `ice`, `ivory`, `khaki`, `lavender`, `lemon`, `lightcoral`, `lightpink`, `lightsalmon`, `lightseagreen`, `lightskyblue`, `lightsteelblue`, `linen`, `mint`, `mintcream`, `mintleaf`, `moccasin`, `navajowhite`, `neongreen`, `neonpink`, `oldlace`, `papayawhip`, `peachpink`, `peachpuff`, `peagreen`, `periwinkle`, `pinkpunch`, `pistachio`, `rose`, `rosybrown`, `sand`, `sandstone`, `seashell`, `snow`, `springmint`, `yellowlime`.
- **Greyscale Spectrum:** `gray0` to `gray100` (and `grey0` to `grey100`) providing step-by-step luminance gradations.

---

## Color Conversion Functions

| Function | Description | Returns |
| :--- | :--- | :--- |
| `name_to_rgb(name)` | Maps a color name string to its `(R, G, B)` tuple. | `tuple[int, int, int]` |
| `name_to_256(name)` | Maps a color name string to its ANSI-256 integer code. | `int` (0-255) |
| `name_to_16(name)` | Maps a color name string to the closest 16-color ANSI code. | `int` (30-37 / 90-97) |
| `get_colors_names()` | Displays an interactive, animated table of all available colors. | `list[str]` or `dict` |

---

## Code Examples

### Single Color Usage
```python
from dvs_printf.colors import Colors

red_text = Colors("scarlet")
print(red_text.apply_to_str("Operation failed!"))

alert = Colors("white", background="red")
print(alert.apply_to_str(" CRITICAL ERROR "))
```

### Multi-Stop Angled Gradient
```python
from dvs_printf.colors import Colors, GradientStyles

gradient = Colors(style=GradientStyles.cyberwave, angle=45)
lines = ["System Initialization", "Loading Core Modules", "Status: OPERATIONAL"]
for line in gradient.apply(lines):
    print("".join(line))
```

### Multi-Line Rotating 2D Angular Gradient Matrix
```python
import time
from dvs_printf.colors import Colors

# 2D spatial matrix treats '\n' as separate rendering layers
matrix_display = [
    "┌──────────────────────────────────────────────────────────┐",
    "│      DVS_PRINTF 2D ANGULAR ROTATING GRADIENT MATRIX      │",
    "├──────────────────────────────────────────────────────────┤",
    "│ [Node 01] Status: ACTIVE    | Latency: 0.016ms           │",
    "│ [Node 02] Status: BALANCED  | Throughput: 104,200 req/s  │",
    "└──────────────────────────────────────────────────────────┘"
]

# Rotate 2D gradient angle continuously across 0° to 360°
for current_angle in range(0, 360, 45):
    gradient_theme = Colors("#FF0055", "#00FFFF", "#FFFF00", angle=current_angle)
    # Apply spatial 2D matrix transformation
    rendered_rows = list(gradient_theme.apply(matrix_display))
    
    # Print formatted matrix grid
    print(f"\033[H\033[J--- Rotation Angle: {current_angle}° ---")
    for row in rendered_rows:
        print("".join(row))
    time.sleep(0.1)
```

---
*© 2026 dvs-printf Team • Visual Excellence in CLI*
