
# Contributing to dvs_printf

First of all, thank you for considering contributing to dvs_printf! We appreciate your time and effort to improve this project. Here are some guidelines to help you get started.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Features](#suggesting-features)
    - [Improving Documentation](#improving-documentation)
3. [Contribute to Workflow](#contribution-workflow)
    - [Submitting Changes](#submitting-changes)
    - [Development setup](#development-setup)
4. [Style Guide](#style-guide)
5. [License](#license)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the standards of behavior we expect from contributors.

## How to Contribute

### Reporting Bugs

If you find any bugs or have feature requests, please [open an issue](https://github.com/dhruvan-vyas/dvs_printf/issues). Provide as much detail as possible to help us understand and address the issue.

- **Description**: A clear and concise description of the problem.
- **Steps to Reproduce**: Detailed steps to reproduce the issue.
- **Expected Behavior**: What you expected to happen.
- **Actual Behavior**: What actually happened, including any error messages.
- **Environment**: Information about your environment (dvs_printf version, Python version, OS, etc.).

### Suggesting Features

We welcome feature suggestions! To suggest a new feature, please open an issue and include:

- **Feature Description**: A clear and concise description of the feature.
- **Use Case**: Why you need this feature, including specific use cases.
- **Possible Implementation**: Any thoughts on how this could be implemented.

### Improving Documentation

If you find any errors or areas for improvement in our documentation, please feel free to submit a pull request. Clear, comprehensive documentation helps everyone use the library more effectively.

## Contribute to Workflow

### Submitting Changes

1. **Fork the repository**: Click the “Fork” button at the top right of the repo page to create your own fork.

2. **Clone your fork**: Clone your forked repo to your local machine.
   ```sh
   git clone https://github.com/<your-username>/dvs_printf.git
   cd dvs_printf
   ```

3. **Create a branch**: Create a new branch for your changes.
    ```sh
    git checkout -b my-new-feature
    ```

4. **Make changes & tests**:<br>
    * **Make your changes to the local directory.** <br>
    
    * **see the [Development setup](#development-setup) section** For more details on setting up the module locally, installing dependencies, creating tests, and organizing files

    * **Update README.md file based on the changes you made.** 
5. **Write tests:** If applicable, write tests for your changes to ensure they work correctly.<br>
    test file name should be `test_<your_function_name>.py`

    **`test the repositorie locally`:**
    ```sh
    pytest tests
    ```
    ```py
    # Create your test.py file in either the Functionality or Compatibility folder
    # based on the changes you made in dvs_printf.

    tests/                      
    ├── __init__.py             
    │                           
    ├── test__Functionality/
    │   ├── test_<your_function_name>.py     # new test file
    │   └── ...
    │
    └── test_Compatibility/
        ├── test_<your_function_name>.py     # new test file
        └── ...
    ```

5. **Commit changes**: Commit your changes with a descriptive commit message.
    ```sh
    git commit -m 'Add some feature'
    ```

6. **Push changes**: Push your changes to your fork.
    ```sh
    git push origin my-new-feature
    ```

7. **Open a pull request**: <br>
    Open a pull request to the main repository [dvs_printf](https://github.com/dhruvan-vyas/dvs_printf). <br>
Please include a detailed description of your changes and any related issue numbers.


### Development setup


1. **Clone the repo**:
    ```sh
    git clone https://github.com/dhruvan-vyas/dvs_printf.git
    cd dvs_printf
    ```

2. **virtual environment** (optional):
    ```sh
    python -m venv venv

    # On Windows use
    venv\Scripts\activate.bat

    # On MacOS use 
    source venv/bin/activate
    ```

4. **Install dvs_printf Module.**
    ```py
    # install dvs_printf 
    pip install dvs_printf

    # OR install dvs_printf with your changes
    pip install -e .   
    ```

3. **Install dependencies**:
    ```py
    # install pytest to test your changes
    pip install pytest

    # For Compatibility Tests, install required module. (optional)
    pip3 install numpy torch pandas tensorflow
    ``` 

4. **organizing files**: <br>
    
    ```py
    dvs_printf/                                # add docstring for new function.
        ├── dvs_printf/  
        │   ├── __init__.py 
        │   ├── __<new_function_name>.py       # name your file `__<name>.py` OR `<Function_Name>.py`
        │   └── ...                            # To avoid conflicts when importing function
        │
        ├── tests/                       # Create your test.py file in either the 
        │   ├── __init__.py              # Functionality or Compatibility folder   
        │   │                            # based on the changes you made in dvs_printf.
        │   ├── test_functionality/
        │   │   ├── test_<your_function_name>.py     # new test file
        │   │   └── ...
        │   │
        │   └── test_compatibility/
        │       ├── test_<your_function_name>.py     # new test file
        │       └── ...
        │   
        ├── .gitignore      # add unnecessary file name 
        │
        ├── README.md       # Update readme file and 
        │                   # add new section for new function
        └── ...
    ```

## Style Guide

Please follow the PEP 8 style guide for Python code. 
You can use tools like flake8 and black to help maintain code quality and consistency.

**Please don't change the coding style in the [printf function](../dvs_printf/__printf__.py) and [otherStyles function](../dvs_printf/other_styles.py).**
**If you make changes to existing styles or add new styles or create new functions in these files, follow the current coding style.**


### Guidelines
- Ensure your code follows the project's coding style.
- Write clear and concise commit messages.
- Update documentation as necessary.
- Include tests for any new functionality.
- Be respectful and collaborative in code reviews and discussions.


## License

By contributing to dvs_printf, you agree that your contributions will be licensed under the MIT License.
