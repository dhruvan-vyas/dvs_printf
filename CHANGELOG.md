# Changelog

All notable changes to the **dvs_printf** module are documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/).

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