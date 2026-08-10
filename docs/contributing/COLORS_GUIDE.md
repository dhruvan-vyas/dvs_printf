# Colors & Gradients Contributor Guide (`dvs_printf.colors`)

This guide provides technical documentation for contributing to the `colors` subsystem of `dvs_printf`, detailing color parsing, 2D angular gradients, pre-built gradient presets, named color dictionaries, `console_EnvType` environment detection, and parameter reference tables.

---

## 1. Pipeline & Architecture Overview

```
[ Raw Color Input (HEX, RGB, HSL, HSV, CMYK, Named Color) ]
                           │
                           ▼
               [ get_RGB_values() Parser ]
                           │
                           ▼
               [ Environment Detection ]
             (console_EnvType: 1, 2, or 3)
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   [ TrueColor ]      [ ANSI-256 ]       [ ANSI-16 ]
 \033[38;2;R;G;Bm    \033[38;5;Nm       \033[3Xm
```

---

## 2. Environment Intelligence (`console_EnvType`)

The module automatically detects terminal color depth and sets `console_EnvType`:

| `console_EnvType` | Level | Support Detail | Terminal Emulators & Environment Matrix | Result |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **TrueColor** | 24-bit RGB (16.7M colors) | Linux (GNOME Terminal, Konsole, Alacritty, Kitty), macOS (Terminal.app, iTerm2), Windows Terminal, VS Code Integrated Terminal, GitHub Actions CI. | Full 24-bit cinematic RGB output (`\033[38;2;R;G;Bm`). |
| **2** | **ANSI-256** | 8-bit palette (256 colors) | xterm-256color terminals, tmux, screen, legacy Linux terminals. | Downsampled 256-color palette index (`\033[38;5;Nm`). |
| **3** | **ANSI-16** | 4-bit standard colors | Windows Command Prompt (`cmd.exe`), basic xterm, legacy serial consoles. | Standard 16 ANSI color codes (`\033[3Xm`). |
| **4** | **No Color** | Plain text / Monochrome | Environments with `NO_COLOR` set or non-interactive pipes/redirects. | Plain un-styled text output. |

---

## 3. Exhaustive `Colors` Class Parameter Reference

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

| Parameter | Type | Default | Deep Technical Explanation |
| :--- | :--- | :--- | :--- |
| `*colors` | `ColorInput \| GredinatInput \| GradientStyles` | *Optional* | Positional arguments defining foreground colors.<br>• **Single Color:** Accepts HEX (`"#FF0000"`), RGB tuple `(255,0,0)`, named color (`"scarlet"`), HSL (`"hsl: 120,1,0.5"`), HSV (`"hsv: 240,1,1"`), or CMYK (`"cmyk: 0,1,1,0"`).<br>• **Gradient:** Pass multiple color arguments or a list of colors. |
| `background` | `ColorInput \| List[ColorInput] \| bool \| None` | `None` | Specifies background color or background gradient.<br>• **`None` / `False`:** No background applied.<br>• **`True`:** Background mode (applies foreground colors as background).<br>• **Single Color:** Applies a static background color.<br>• **List of Colors:** Applies a background gradient across the character grid. |
| `angle` | `int \| None` | `None` | Angle in degrees (`0°` to `360°`) for 2D character-grid gradient calculation (`0°` horizontal, `90°` vertical, `45°` diagonal). |
| `style` | `GradientStyles \| None` | `None` | Predefined gradient palette object or style name (e.g. `GradientStyles.rainbowflame`). Overrides explicit `*colors`. |

---

## 4. Pre-built Gradient Styles (`GradientStyles`)

`dvs_printf` defines 24 pre-built gradient presets in `dvs_printf/colors/gredinat_styles.py`:

- **Presets:** `rainbowflame`, `rosetwilight`, `sunsetburn`, `electricdreams`, `neonparty`, `cyberwave`, `seewave` (`seawave`), `forestfade`, `midnightblues`, `loki`, `loki_serene`, `tva_portal`, `iron_man`, `captain_america`, `thor`, `hulk`, `hawkeye`, `black_widow`, `tva`, `timedoors`, `tempad`, `dark_purple`, `light_purple`, `tea`.

### Adding a New Gradient Preset

1. Open `dvs_printf/colors/gredinat_styles.py`.
2. Add a new tuple of RGB color stops to `GradientStyles`:
   ```python
   class GradientStyles:
       # Existing presets...
       solar_flare = ( (255, 69, 0), (255, 140, 0), (255, 215, 0), (255, 255, 255) )
   ```
3. Test using `Colors(GradientStyles.solar_flare)`.

---

## 5. Built-in Named Colors List (345+ Colors)

Color lookup entries are defined in `dvs_printf/colors/colors_dictionary.py`:

- **Basic:** `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`.
- **Light:** `lightblack`, `lightred`, `lightgreen`, `lightyellow`, `lightblue`, `lightmagenta`, `lightcyan`, `lightwhite`.
- **Dark:** `darkblue`, `darkcyan`, `darkgoldenrod`, `darkgray`, `darkgreen`, `darkkhaki`, `darkmagenta`, `darkolivegreen`, `darkorange`, `darkorchid`, `darkred`, `darksalmon`, `darkseagreen`, `darkslateblue`, `darkslategray`, `darkturquoise`, `darkviolet`.
- **Popular Tones:** `aliceblue`, `antiquewhite`, `aqua`, `aquamarine`, `avocado`, `azure`, `babyblue`, `beige`, `bisque`, `blanchedalmond`, `bluebell`, `blueviolet`, `brick`, `brown`, `bubblegum`, `burlywood`, `burntorange`, `butter`, `cadetblue`, `candy`, `carnation`, `chartreuse`, `chocolate`, `coral`, `cornflowerblue`, `cornsilk`, `cottoncandy`, `cream`, `crimson`, `deeppink`, `deepskyblue`, `dimgray`, `dodgerblue`, `firebrick`, `forestgreen`, `fuchsia`, `gainsboro`, `gold`, `goldenrod`, `gray`, `greenyellow`, `hotpink`, `indianred`, `indigo`, `ivory`, `khaki`, `lavender`, `lawngreen`, `lemon`, `lightcoral`, `lightpink`, `lightsalmon`, `lightseagreen`, `lightskyblue`, `lightsteelblue`, `lime`, `limegreen`, `linen`, `maroon`, `mediumaquamarine`, `mediumblue`, `mediumorchid`, `mediumpurple`, `mediumseagreen`, `mediumslateblue`, `mediumspringgreen`, `mediumturquoise`, `mediumvioletred`, `midnightblue`, `mintcream`, `moccasin`, `navajowhite`, `navy`, `oldlace`, `olive`, `olivedrab`, `orange`, `orangered`, `orchid`, `palegoldenrod`, `palegreen`, `paleturquoise`, `palevioletred`, `papayawhip`, `peachpuff`, `peru`, `pink`, `plum`, `powderblue`, `purple`, `rebeccapurple`, `rosybrown`, `royalblue`, `saddlebrown`, `salmon`, `sandybrown`, `scarlet`, `seagreen`, `seashell`, `sienna`, `silver`, `skyblue`, `slateblue`, `slategray`, `snow`, `springgreen`, `steelblue`, `tan`, `teal`, `thistle`, `tomato`, `turquoise`, `violet`, `wheat`, `yellowgreen`.
- **Greyscale Range:** `gray0` through `gray100` (`grey0` through `grey100`).

---

## 6. Testing Color Conversion & Environment Emulation

Override `console_EnvType` in tests to verify downsampling behavior:

```python
import dvs_printf.colors.ansi as ansi

# Force TrueColor mode (24-bit)
ansi.console_EnvType = 1

# Force ANSI-256 mode (8-bit)
ansi.console_EnvType = 2

# Force ANSI-16 mode (4-bit)
ansi.console_EnvType = 3
```
