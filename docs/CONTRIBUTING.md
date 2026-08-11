# Contributing to dvs_printf

Thank you for considering contributing to **`dvs_printf`**! We welcome contributions from developers of all skill levels. Whether you are fixing bugs, optimizing animation rendering, adding new color palettes, or expanding documentation, your efforts help improve the library for the entire community.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Features](#suggesting-features)
   - [Improving Documentation](#improving-documentation)
3. [Development Setup](#development-setup)
4. [Contribution Workflow](#contribution-workflow)
5. [Specialized Subsystem Guides](#specialized-subsystem-guides)
   - [Colors & Gradients Guide](contributing/COLORS_GUIDE.md)
   - [Text Animations Guide](contributing/TEXT_ANIMATIONS_GUIDE.md)
   - [Loaders & Threading Guide](contributing/LOADERS_AND_THREADING_GUIDE.md)
6. [Code Style & Verification](#code-style--verification)
7. [License](#license)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please review it before submitting issues or pull requests.

---

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check existing issues to see if the problem has already been reported. When opening a new issue, include as much context as possible:

- **Description:** A concise summary of the issue.
- **Steps to Reproduce:** Minimal code example demonstrating the failure.
- **Expected Behavior:** What should have happened.
- **Actual Behavior:** Actual console output or traceback stack.
- **Environment Context:** Python version, OS, terminal emulator (e.g. GNOME Terminal, macOS Terminal, Windows Terminal), and `dvs_printf` version.

### Suggesting Features

Feature proposals are always welcome! When opening a feature request issue, please describe:

- **Feature Summary:** What capability would you like to see added?
- **Use Case:** Why is this useful and what problem does it solve?
- **Proposed Syntax / API:** Example code showing how users would interact with the new feature.

### Improving Documentation

If you notice inaccuracies, typos, missing explanations, or poor formatting in any README or guide, feel free to open a Pull Request.

---

## Development Setup

To work on `dvs_printf` locally:

1. **Fork and Clone the Repository:**
   ```bash
   git clone https://github.com/<your-username>/dvs_printf.git
   cd dvs_printf
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv

   # On Linux / macOS:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Package in Editable Mode with Dependencies:**
   ```bash
   pip install -e .
   pip install pytest
   ```

---

## Contribution Workflow

1. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Implement Your Changes:**
   - Keep changes focused and modular.
   - Maintain PEP 8 coding conventions.
   - Add inline docstrings explaining complex algorithms.

3. **Run Unit Tests:**
   ```bash
   pytest tests
   ```

4. **Commit & Push:**
   ```bash
   git commit -m "feat(colors): add new gradient preset 'solar_flare'"
   git push origin feature/my-new-feature
   ```

5. **Open a Pull Request:**
   Submit a PR against the `main` branch of `dhruvan-vyas/dvs_printf` with a detailed description of your changes.

---

## Specialized Subsystem Guides

`dvs_printf` is organized into several dedicated subsystems. For deep technical guidelines on extending specific modules, see:

- [**Colors & Gradients Guide**](contributing/COLORS_GUIDE.md): Adding color spaces, named color lookup mappings, and 2D angular gradient palettes.
- [**Text Animations Guide**](contributing/TEXT_ANIMATIONS_GUIDE.md): Implementing new streaming animation styles, frame delay formulas, and lazy loading functions in `_other_styles.py`.
- [**Loaders & Threading Guide**](contributing/LOADERS_AND_THREADING_GUIDE.md): Creating custom spinners (`SpinnerFrems`), progress bars (`LoadingBarConfig`), and managing worker thread synchronization.

---

## Code Style & Verification

- **PEP 8 Compliance:** Follow standard Python formatting standards.
- **Type Annotations:** Add type hints (`Union`, `Optional`, `Tuple`, `Callable`) for public function signatures.
- **Zero Heavy Dependencies:** The core package must remain lightweight and executable on standard Python installations without requiring compiled C extensions.

---

## License

By contributing to `dvs_printf`, you agree that your contributions will be licensed under the project's [Apache License 2.0](../LICENSE).
