# Changelog

All notable changes to the **dvs_printf** module are documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/).

---

## [3.1.3] - 2026-08-12

### Added
- **`SafeIOSuppressor` Context Engine**: Introduced centralized, exception-safe POSIX `os.dup2` file descriptor suppressor.
- **Emergency `atexit` Hooks**: Added emergency cleanup registration to prevent terminal lockouts on unexpected process crashes or `SIGINT` signals.
- **Environment Auto-Detection Matrix**: Automatic environment detection (`suppress_io="auto"`) that gracefully falls back to stream redirection in Jupyter (`ipykernel`), `pytest`, and IDE consoles.
- **Configurable `suppress_io` Parameter**: Added `suppress_io` parameter (`"auto"`, `"fd"`, `"stream"`, `False`) to `LoadingBar`, `Spinner`, `ShowLoading`, and `ShowSpinner`.
- **Unit Tests**: Added dedicated `test_io_suppressor.py` unit test suite.

### Changed
- **Documentation Suite**: Completely enriched `README.md`, `loaders_README.md`, `colors_README.md`, and `printf_README.md` with technical architectural benchmarks (~16,000ns startup, safe-area console bounds, 2D spatial gradients).
- **PYPI_README Links**: Converted all relative links to absolute GitHub URLs for PyPI package rendering.

### Fixed
- **CI Build Failure**: Added dynamic README file resolution in `setup.py` (`os.path.exists("PYPI_README.md")`), fixing `FileNotFoundError` during GitHub Actions CI builds and clean clones.

---

## [3.1.0] - 2025-04-20

### Added
- **Redesigned Color Engine**: Full integration of the Colors module with support for 24-bit TrueColor (RGB).
- **Angular Gradients**: Support for smooth color transitions across text with angle-based interpolation.
- **Environment Auto-Detection**: Real-time detection of terminal capabilities (TrueColor, 256-color, 16-color).
- **New Animation Styles**: Added 'silverfade', 'glitch', 'fire', and 'newsline' styles.
- **AST Traceback Highlighting**: Intelligent error reporting that highlights the exact argument in source code.
- **Multi-Threaded Loaders**: Rewritten LoadingBar and Spinner classes with aggressive I/O suppression.
- **Init Class**: Introduced the Init class for unified global configuration and property-based validation.

### Changed
- **Modular Refactor**: Decoupled styles from core logic into _other_styles.py for lazy loading.
- **Speed Algorithm**: Balanced speed constants across all 20+ styles for consistent visual experience.
- **Public API**: Simplified imports; core classes are now directly accessible from the main package.
- **Documentation**: Comprehensive overhaul of the README suite in the READMES folder.

### Fixed
- **ANSI Leakage**: Resolved issues where color codes would persist after animation completion.
- **Terminal Width Errors**: Fixed calculations for 'center' and 'right' styles on narrow terminals.
- **Thread Safety**: Improved synchronization between worker and animation threads in loaders.

### Deprecated
- **init Class**: The lowercase 'init' class is deprecated in favor of 'Init'.

---

## [2.2.0] - 2024-11-15

### Added
- **Core printf**: Initial release of the animated printing function.
- **Style Library**: Basic support for 'typing', 'headline', and 'async'.
- **Simple Colors**: Support for named colors and standard 16-color ANSI codes.
- **Progress Bars**: First iteration of the LoadingBar component.

### Changed
- **Internal Optimization**: Improved character-by-character rendering performance.

---

## [1.0.0] - 2024-06-05

### Added
- **Project Genesis**: Initial private release for internal CLI tools.
- **Base Style**: Discovery and implementation of the 'typing' animation logic.