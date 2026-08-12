# Release Notes: dvs_printf v3.1.3

**Release Date:** August 12, 2026  
**Package Version:** `3.1.3`  
**License:** Apache 2.0 

---

## Summary of Changes

Version 3.1.3 delivers the enterprise-grade `SafeIOSuppressor` context manager for kernel-level POSIX `os.dup2` file descriptor manipulation, emergency `atexit` restoration protection, Jupyter/Pytest environment auto-detection, comprehensive documentation overhauls, and robust CI build configuration fixes.

---

## Key Features and Enhancements

### 1. Fail-Safe POSIX I/O Suppression (`SafeIOSuppressor`)
- **Centralized Context Engine:** Replaced manual `os.dup2` calls in `LoadingBar` and `Spinner` with `SafeIOSuppressor`, ensuring exception-safe allocation and cleanup.
- **Emergency `atexit` Hooks:** Registered `@atexit.register` restoration routines to guarantee file descriptors 1 (`stdout`) and 2 (`stderr`) are restored instantly if Python exits unexpectedly or receives `SIGINT` (`Ctrl+C`).
- **Environment Auto-Detection (`suppress_io="auto"`):** Detects Jupyter Notebook (`ipykernel`), `pytest` runners, and IDE consoles, falling back to high-level stream redirection without triggering `io.UnsupportedOperation: fileno`.
- **Configurable Modes:** Added `suppress_io` support (`"auto"`, `"fd"`, `"stream"`, `False`) to give developers fine-grained control over process-wide FD redirection vs thread-local stream isolation.

### 2. Comprehensive Documentation & Sub-Module Guides
- **Master & Sub-Module Guides:** Completely updated `README.md`, `loaders_README.md`, `colors_README.md`, and `printf_README.md`.
- **High-Performance Benchmarks:** Documented the ~16,000ns startup latency generator engine and console safe-area bounds detection (`os.get_terminal_size()`) for PyTorch, NumPy, and Pandas matrices.
- **2D Angular Gradient Matrix Examples:** Added code examples demonstrating rotating 2D angular spatial gradients across multi-line text grids.

### 3. Packaging & CI Build Stabilization
- **CI Build Fallback:** Updated `setup.py` with dynamic README detection (`os.path.exists("PYPI_README.md")`), preventing `FileNotFoundError` during GitHub Actions CI runs or clean git clones.
- **Clean PyPI Wheel Distribution:** Freshly built wheel and sdist distributions.

---

# Release Notes: dvs_printf v3.1.0

**Release Date:** August 10, 2026  
**Package Version:** `3.1.0`  
**License:** Apache 2.0 

---

## Summary of Changes

Version 3.1.0 introduces full 24-bit TrueColor angular gradient projection, multi-stop color palette interpolation, multi-threaded progress loaders, AST-based source token exception highlighting, and optimized terminal downsampling.

---

## Key Features and Enhancements

### 1. Expanded Color and Gradient Engine (`dvs_printf.colors`)
- **Multi-Format Color Parsing:** Native parsing for HEX (`#RGB`, `#RRGGBB`), RGB tuples, RGB strings (`rgb: r,g,b`), HSL (`hsl: h,s,l`), HSV (`hsv: h,s,v`), CMYK (`cmyk: c,m,y,k`), and 345+ named colors.
- **Angular 2D Gradients:** Implemented 2D character-grid geometry calculation for arbitrary angle projections (0 to 360 degrees).
- **Dynamic Downsampling:** Automatically degrades TrueColor (24-bit) escape sequences down to 256-color (8-bit) or 16-color (4-bit) depending on terminal environment detection (`console_EnvType`).

### 2. Animated Output Engine (`dvs_printf.printf`)
- **Streaming Styles:** Over 20 animation styles including `typing`, `glitch`, `matrix`, `matrix2`, `headline`, `async`, `wave`, `fire`, `newsline`, `gunshort`, `snip`, and `silverfade`.
- **Data Matrix Serialization:** Automatic line-by-line pretty formatting for non-string objects (`list`, `dict`, `tuple`, matrices).
- **Speed Multipliers:** Dynamic character-delay calculations derived from style base frequencies and user speed multipliers.

### 3. Threaded Task Loaders (`dvs_printf.loaders`)
- **Background Worker Threads:** Added `Spinner` and `LoadingBar` classes to execute user functions concurrently alongside animated terminal progress indicators.
- **40+ Spinner Styles:** Integrated pre-configured spinner animations (`dots`, `arrow`, `moon`, `shark`, `pong`, `bounce`, `line`, etc.).
- **Progress Tracking:** Added `ProgressUpdater` for real-time iteration tracking via `inject_progress`.

### 4. AST Exception Visualizer (`dvs_printf.exceptions`)
- **AST Frame Analysis:** Inspects stack frames using Python `ast` and `inspect` modules.
- **Token Pointing:** Emits visual column pointers beneath failing source tokens.

---

## Bug Fixes and Stability Improvements

- Fixed setuptools `setup.py` build configuration for PyPI distribution.
- Corrected division-by-zero errors in HSL and HSV fractional string conversion.
- Normalized color string inputs by stripping whitespace and converting to lowercase before dictionary lookups.
- Resolved ANSI escape sequence leakage upon animation loop completion.

---

## Migration Guide

### 1. Unified Loaders API
Use `Spinner` or `LoadingBar` directly from `dvs_printf.loaders`:

```python
from dvs_printf.loaders import Spinner, LoadingBar

# For indeterminate waiting tasks:
spinner = Spinner(title="Processing", style="dots")
result = spinner.run(my_task_function)

# For progress tracking tasks:
loader = LoadingBar(title_text="Downloading")
loader.run(my_download_function, progress_updater=True)
```

### 2. Class Naming Update
- Use capital `Init` class for global configuration settings (`from dvs_printf import Init`). The lowercase `init` class is retained for backward compatibility.

---

## Upgrade Instructions

Upgrade via `pip`:

```bash
pip install --upgrade dvs-printf
```
