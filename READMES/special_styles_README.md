# Special Parameterized Styles Reference (`dvs_printf.printf`)

The `printf()` function supports special **inline-parameterized styles**, where custom control parameters (such as simultaneous line counts, alignment percentages, distortion mask characters, and fade iteration passes) are attached directly to the style string key.

---

## Exhaustive Special Styles Overview

| Special Style | Parameter Syntax | Example Style String | Description |
| :--- | :--- | :--- | :--- |
| [**`async`**](#1-async-style) | `async` or `async <num_lines>` | `"async 8"` | Renders multiple lines simultaneously line-by-line. |
| [**`center` / Alignment**](#2-center--alignment-styles) | `center`, `center<align>`, `center <pos>%` | `"centerAL 30%"`, `"centerAR 70%"` | Custom horizontal terminal alignment & percentage-based positioning. |
| [**`glitch`**](#3-glitch-distortion-style) | `glitch` or `glitch<char>` | `"glitch*"`, `"glitch#"` | Random character distortion effect with customizable mask character. |
| [**`silverfade`**](#4-silver-fade-style) | `silverfade` or `silverfade <iterations>` | `"silverfade 5"` | Multi-pass shimmering silver gradient sweep effect. |

---

### 1. `async` Style

The `async` style introduces **simultaneous multi-line rendering**, printing sets of lines in parallel across the terminal screen rather than sequentially line-by-line.

https://github.com/user-attachments/assets/6f05b6f6-b234-41e6-b7f4-7a5052bfa0ff

#### Key Features:
- **Simultaneous Parallel Output:** Renders multiple lines character-by-character at the exact same time using ANSI cursor positioning (`\033[F`).
- **Adaptive Terminal Display:** `style="async"` automatically detects available terminal height (`terminal_height - 1`) and splits long text into optimal display batches.
- **Custom Line Batching (`async <num_lines>`):** Specify `style="async <number>"` (e.g., `"async 2"`, `"async 4"`, `"async 8"`, `"async 16"`) to control exactly how many lines are printed simultaneously in each batch before advancing.

#### Usage Examples:
```python
from dvs_printf import printf

# Automatically batch lines based on available terminal height
printf("Line 1\nLine 2\nLine 3\nLine 4", style="async")

# Print in sets of 2 lines simultaneously
printf(
    "This is line 1\nThis is line 2\nThis is line 3", 
    "This is line 4\nThis is line 5", 
    delay=0,
    style="async 2"   # Renders sets of 2 lines simultaneously: [1-2, 3-4, 5]
) 
```

> [!NOTE]
> The term **"async"** in `dvs_printf` refers to the visual parallel-line rendering animation style and is independent of Python's standard `asyncio` event loop.

---

### 2. Center & Alignment Styles

The `center` family provides fine-grained control over text positioning, horizontal alignment, and percentage-based terminal layouts.

#### Variants & Parameter Syntax:

| Style Variant | Syntax | Description | Example |
| :--- | :--- | :--- | :--- |
| **`center`** | `style="center"` | Standard horizontal center alignment based on terminal width. | `printf("Title", style="center")` |
| **`center <percentage>%`** | `style="center <int>%"` | Positions the center target at `<percentage>%` of full terminal width. | `printf("Left-ish", style="center 30%")` |
| **`centerAL`** | `style="centerAL"` or `style="centerAL <percentage>%"` | **Arrange-Left**: Left-aligns text starting at target terminal percentage. | `printf("Sidebar", style="centerAL 20%")` |
| **`centerAR`** | `style="centerAR"` or `style="centerAR <percentage>%"` | **Arrange-Right**: Right-aligns text ending at target terminal percentage. | `printf("Panel", style="centerAR 80%")` |
| **`centerAC`** | `style="centerAC"` | **Arrange-Center**: Centered alignment within calculated margin bounds. | `printf("Header", style="centerAC")` |

#### Usage Examples:
```python
from dvs_printf import printf

# Standard center alignment
printf("SYSTEM MAIN MENU", style="center")

# Center text at 30% from the left margin of full terminal window
printf("System Status: Operational", style="center 30%")

# Left-align text starting at 20% of terminal width (centerAL)
printf("User: Admin", "Role: Superuser", style="centerAL 20%")

# Right-align text ending at 80% of terminal width (centerAR)
printf("Memory: 16GB", "CPU: 4.2GHz", style="centerAR 80%")
```

---

### 3. Glitch Distortion Style

The `glitch` style produces a digital noise and character corruption animation before unveiling the final text string.

#### Parameter Syntax:
- **Default Glitch:** `style="glitch"` (uses default distortion mask character `^`).
- **Custom Mask Character:** `style="glitch<char>"` (append any custom character directly to `"glitch"`, e.g. `"glitch*"`, `"glitch#"`, `"glitch@"`, `"glitch~"`).

#### Usage Examples:
```python
from dvs_printf import printf

# Standard glitch effect with default mask '^'
printf("LOADING SYSTEM REGISTRY...", style="glitch")

# Glitch animation using asterisks '*' as the noise mask
printf("CRITICAL SYSTEM WARNING", style="glitch*", color="red", speed=5)

# Glitch animation using hash '#' symbols
printf("DECRYPTING DATA STREAM...", style="glitch#", color="magenta")
```

---

### 4. Silver Fade Style

The `silverfade` style creates a cinematic, shimmering metallic silver-to-grey gradient sweep across text.

#### Parameter Syntax:
- **Default Silver Fade:** `style="silverfade"` (runs 2 shimmering passes).
- **Custom Shimmer Iterations:** `style="silverfade <iterations>"` (append number of passes directly to `"silverfade"`, e.g. `"silverfade 3"`, `"silverfade 5"`, `"silverfade 10"`).

#### Usage Examples:
```python
from dvs_printf import printf

# Standard silver fade animation (2 iterations)
printf("INITIALIZING GRAPHICS ENGINE...", style="silverfade")

# Extended silver fade shimmer (5 iterations)
printf("SUCCESSFULLY LOADED MODULES", style="silverfade 5", delay=1)
```

---
*© 2026 dvs-printf Team • Professional Console Animation*
