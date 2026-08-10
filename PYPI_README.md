# dvs_printf

High-performance Python console formatting engine providing animated text rendering, 24-bit TrueColor angular gradients, multi-threaded task loaders, and AST-driven exception visualizers.

---

## Features

- **Rich Color Engine:** Supports 24-bit TrueColor (RGB), 8-bit (256-color), and 4-bit (16-color) terminals. Accepts HEX, RGB, HSL, HSV, CMYK, and 345+ named colors.
- **Angular 2D Gradients:** Interpolates multi-stop linear and angled (0 to 360 degrees) color gradients across multi-line text matrices.
- **Animated Printing Engine:** Over 20 streaming animation styles (`typing`, `glitch`, `matrix`, `matrix2`, `headline`, `async`, `wave`, `fire`, `newsline`, `gunshort`, `snip`, `silverfade`) with precise speed multipliers.
- **Multi-Threaded Loaders & Spinners:** Non-blocking background task wrappers (`LoadingBar`, `Spinner`, `ShowLoading`, `ShowSpinner`) with progress tracking and console output suppression.
- **AST Exception Formatter:** Pinpoints frame failure locations and highlights exact syntax tokens with visual indicators.
- **Zero External Dependencies:** Built entirely on standard Python core modules.

---

## Installation

Install via PyPI:

```bash
pip install dvs-printf
```

Or install locally from source:

```bash
git clone https://github.com/dhruvan-vyas/dvs_printf.git
cd dvs_printf
pip install .
```

---

## Requirements

- Python 3.10 or higher.
- Compatible with Linux, macOS, and Windows (Windows Terminal or PowerShell recommended for 24-bit TrueColor support).

---

## Quickstart Guide

### 1. Animated Printing with Colors

```python
from dvs_printf import printf, Colors

# Animated typing text in green
printf("Connecting to remote server...", style="typing", color="green", speed=2)

# Glitch animation with gradient foreground
gradient_theme = Colors("cyan", "magenta", angle=45)
printf(
    "SYSTEM ERROR DETECTED",
    style="glitch",
    speed=4,
    color=gradient_theme,
    attrs=["bold"]
)
```

### 2. Multi-Stop Angular Gradients

```python
from dvs_printf.colors import Colors

# Create a multi-color gradient scheme
gradient = Colors("#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", angle=45)

text_block = [
    "==================================================",
    "       DVS_PRINTF ANGULAR GRADIENT ENGINE         ",
    "=================================================="
]

for line in gradient.apply(text_block):
    print("".join(line))
```

### 3. Multi-Threaded Task Spinners and Loading Bars

```python
import time
from dvs_printf.loaders import Spinner, LoadingBar

def background_task():
    time.sleep(2)
    return "Dataset Processed"

# Run background task with an animated spinner
spinner = Spinner(title="Fetching Remote Artifacts", style="dots", spinner_color="cyan")
result = spinner.run(background_task)
print("Result:", result)

# Progress tracking loading bar
def download_task(progress_updater):
    for i in range(101):
        time.sleep(0.02)
        progress_updater.update(i)

loader = LoadingBar(title_text="Downloading Engine Models", bar_color=["cyan", "blue"])
loader.run(download_task, progress_updater=True)
```

### 4. Global Configuration Management with Init

```python
from dvs_printf import Init

# Define global theme defaults
app_theme = Init(
    style="newsline",
    speed=3,
    colors="cyan",
    attrs=["bold"]
)

# Use configured instance across your application
app_theme.printf("System status: OPERATIONAL")
app_theme.printf("Database sync: COMPLETED")
```

---

## Terminal Environment Compatibility Matrix

| Terminal Emulator | TrueColor (24-bit) | 256-Color | 16-Color | Cursor Control |
| :--- | :--- | :--- | :--- | :--- |
| **Linux (GNOME, Konsole, Alacritty)** | Supported | Supported | Supported | Supported |
| **macOS (Terminal.app, iTerm2)** | Supported | Supported | Supported | Supported |
| **Windows Terminal** | Supported | Supported | Supported | Supported |
| **Windows Command Prompt (cmd.exe)** | Partial (Win10+) | Supported | Supported | Supported |
| **CI/CD Environments (GitHub Actions)** | Supported | Supported | Supported | N/A |

---

## License

Distributed under the Apache License 2.0. See `LICENSE` for details.
