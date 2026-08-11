# Exception Management: Intelligent Debugging (`dvs_printf.exceptions`)

`dvs_printf` includes an error reporting system that goes beyond standard Python tracebacks. It is designed to help pinpoint mistakes in `printf` calls instantly.

---

## The Fancy Traceback: Console Simulation

When a validation error occurs, the module renders a high-visibility, color-coded report directly in your terminal:

```ansi
Traceback (most recent call last):
  File "main.py", line 12, in <module>
    └── 12  printf("Hello", color="red", style="typign")
                                         ~~~~~^^^^^^^^

StyleNameError: The Style 'typign' Is Not Recognized.

Did you mean?
  ➔ 'typing' (90% match)
```

### Key Features:
- **AST-Based Highlighting**: Pinpoints the exact argument and its column in source code.
- **Fuzzy Suggestion Engine**: Automatically suggests the correct style name if typos occur.
- **Contextual Wrapping**: Collapses irrelevant code blocks to keep terminal output clean.
- **Color Coding**: Uses high-contrast highlights for keywords and error values.

---

## Architecture & Exception Hierarchy

All exceptions in `dvs_printf` derive from a common base class:

```
dvs_BaseException (built-in Exception)
├── ColorsValueError
├── StyleNameError
├── SpeedValueError
├── AttrsValueError
├── LoaderValueError
├── SpinnerValueError
└── TimeOutError
```

---

## Exception Dictionary & Features

| Exception Class | Highlight Focus | Common Trigger |
| :--- | :--- | :--- |
| `dvs_BaseException` | Core Exception | Base class providing standardized message formatting and traceback context. |
| `ColorsValueError` | `color` / `background_color` | Invalid Hex strings, out-of-range RGB values (> 255), or unparseable color names. |
| `StyleNameError` | `style` keyword | Unrecognized style keys like `'typign'` or `'glitsh'`. |
| `SpeedValueError` | `speed` keyword | Speed values <= 0 or non-numeric arguments. |
| `AttrsValueError` | `attrs` list | Misspelled text attributes like `'boldy'`. |
| `LoaderValueError` | Loader target / params | Invalid target function or loader configuration options. |
| `SpinnerValueError` | Spinner target / style | Invalid target function or unrecognized spinner style name. |
| `TimeOutError` | Background Process | Thread execution exceeding the specified `timeout` limit. |

---

## How it Works Internally

The module provides a custom `dvs_excepthook` for advanced stack frame inspection:

1. **`_extract_full_call()`**: Uses Python's `inspect` module to locate physical lines of the failing function call in source files.
2. **`find_argument_match()`**: Parses the Abstract Syntax Tree (AST) of those lines via `ast.parse()` to correlate runtime objects with source code tokens and column offsets (`col_offset`, `end_col_offset`).
3. **`_Warning`**: A persistent but non-fatal notifier used for deprecation warnings (e.g., using the old lowercase `init` class).

---

## Enabling the Custom Traceback Hook

```python
import sys
from dvs_printf.exceptions import dvs_excepthook

# Register the custom excepthook for fancy tracebacks
sys.excepthook = dvs_excepthook
```

---

## Usage Example

```python
from dvs_printf.exceptions import ColorsValueError
from dvs_printf.colors import get_RGB_values

try:
    # Attempting to parse an invalid color specification
    rgb = get_RGB_values("invalid_color_name")
except ColorsValueError as err:
    print(f"Caught expected error: {err._message}")
    print(f"Offending value: {err.value}")
```

---
*© 2026 dvs-printf Team • Debugging at the Speed of Light*
