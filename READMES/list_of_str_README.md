# `list_of_str` Function: Multi-Type Data Serialization Core

The `list_of_str` function is an essential utility within `dvs_printf`. It serves as the input normalization engine for `printf()`, converting heterogeneous data types—including primitive values, deeply nested Python collections, and multi-dimensional scientific matrices (`NumPy`, `PyTorch`, `TensorFlow`, `Pandas`)—into a clean, memory-efficient stream of strings suitable for console animations.

---

## 📌 Function Signature

```python
list_of_str(*values: Any, getmat: bool | str | None = False) -> Generator[str, None, None]
```

### Parameter Breakdown

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `*values` | `Any` | *Required* | Positional inputs of any data type (`str`, `int`, `float`, `list`, `tuple`, `dict`, `set`, `ndarray`, `Tensor`, `DataFrame`, custom objects). |
| `getmat` | `bool \| str` | `False` | Matrix serialization mode. Reshapes N-dimensional arrays into row-by-row string streams (`True` / `"true"`) and appends metadata headers (`"show"`). |

---

## ⚙️ How It Works

1. **Generator-Based Stream Processing:** Implemented as a Python generator (`yield`), enabling memory-efficient processing of large datasets and matrix arrays without allocating giant lists in memory.
2. **Control Character Stripping:** Automatically strips non-printable control characters (`\x00`–`\x1F`, `\x7F`–`\x9F`) from input strings to prevent console corruption.
3. **Responsive Line Wrapping (`divide_line`):** Inspects the active terminal window width (`terminal_width - 2`, falling back to 80 characters). Long strings exceeding terminal width are gracefully split at word boundaries.
4. **Recursive Unwrapping:** Automatically flattens arbitrarily nested lists, tuples, sets, and dictionary structures into single-element string streams.

---

## 📊 Data Structure Handling

| Input Type | Conversion & Serialization Behavior |
| :--- | :--- |
| `str` | Strips control characters, splits multiline text at `\n`, and applies word-wrapping (`divide_line`) if longer than terminal width. |
| `int`, `float`, `bool`, `None` | Converted directly to string (`"123"`, `"3.14159"`, `"True"`, `"None"`). |
| `dict` | Iterates over key-value pairs, formatting each entry as `"key: value"`. If a value contains newlines, each line is yielded separately. |
| `list`, `tuple`, `set` | Unpacked recursively element-by-element. Structure order is preserved for lists/tuples. |
| `NumPy` / `PyTorch` / `TensorFlow` / `Pandas` | When `getmat` is active, reshapes N-D matrices into 2D row slices (`[row_1]`, `[row_2]`, ...) and optionally appends `<class, shape, dtype>` metadata headers. |

---

## 🎛️ `getmat` Matrix Serialization Modes

The `getmat` parameter controls how multi-dimensional numeric matrices and arrays are formatted:

- **`getmat = False`** *(default)*: Outputs standard native string representation of the object (including class wrappers and default array brackets).
- **`getmat = True` | `"true"`**: Reshapes the matrix into 2D row slices and yields individual row vectors (e.g., `"[1.0, 1.0, 1.0]"`), ideal for applying truecolor gradient animations across matrix rows.
- **`getmat = "show"` | `"show info"`**: Yields the formatted 2D row vectors **plus** structured metadata rows detailing object `<class>`, data type `dtype`, and shape `shape`.

> [!WARNING]
> **Truthy Check Behavior:**
> Internally, `list_of_str` evaluates `if getmat:`. In Python, any non-empty string is truthy. Passing string literals such as `"false"` will evaluate as **truthy** (`True`). To disable matrix mode, pass boolean `False` or `None`.

---

## 💡 Code Examples

### 1. Primitives & Deeply Nested Collections

```python
from dvs_printf import list_of_str

nested_data = (
    "Greetings, world",
    "Line 1\nLine 2",
    [100, 3.14159, ("nested_item", 2001, 2002)],
    ["apple", "banana"],
    {"status": "OK", "code": 200},
    True,
    None
)

# Convert nested collection into clean string generator
output = list(list_of_str(nested_data))

print(output)
# Output:
# [
#     'Greetings, world', 
#     'Line 1', 
#     'Line 2', 
#     '100', 
#     '3.14159', 
#     'nested_item', 
#     '2001', 
#     '2002', 
#     'apple', 
#     'banana', 
#     'status: OK', 
#     'code: 200', 
#     'True', 
#     'None'
# ]
```

---

### 2. Dictionaries & Multiline Content

```python
from dvs_printf import list_of_str

user_profile = {
    "name": "Johnny Depp",
    "profession": "Actor & Musician",
    "bio": "Passionate about coding\nLoves open-source projects"
}

output = list(list_of_str(user_profile))

print(output)
# Output:
# [
#     'name: Johnny Depp',
#     'profession: Actor & Musician',
#     'bio: Passionate about coding',
#     'Loves open-source projects'
# ]
```

---

### 3. TensorFlow Variables & Tensors (`getmat`)

```python
import tensorflow as tf
from dvs_printf import list_of_str

tf_array = tf.Variable([
    [[1, 1, 1],
     [2, 2, 2],
     [3, 3, 3]]
], dtype=tf.float32)

# Mode 1: Default (getmat=False)
print(list(list_of_str(tf_array, getmat=False)))
# Output:
# [
#     "<tf.Variable 'Variable:0' shape=(1, 3, 3) dtype=float32, numpy=",
#     "array([[[1., 1., 1.],",
#     "        [2., 2., 2.],",
#     "        [3., 3., 3.]]], dtype=float32)>"
# ]

# Mode 2: Matrix Row Mode (getmat=True)
print(list(list_of_str(tf_array, getmat=True)))
# Output:
# [
#     '[1.0, 1.0, 1.0]',
#     '[2.0, 2.0, 2.0]',
#     '[3.0, 3.0, 3.0]'
# ]

# Mode 3: Matrix Mode with Metadata Header (getmat="show")
print(list(list_of_str(tf_array, getmat="show")))
# Output:
# [
#     '[1.0, 1.0, 1.0]',
#     '[2.0, 2.0, 2.0]',
#     '[3.0, 3.0, 3.0]',
#     "<class 'Tensorflow'",
#     " float32 ",
#     " shape: (1, 3, 3)>"
# ]
```

---

### 4. NumPy `ndarray` (`getmat`)

```python
import numpy as np
from dvs_printf import list_of_str

np_matrix = np.array([
    [[1, 1, 1], [2, 2, 2], [3, 3, 3]],
    [[4, 4, 4], [5, 5, 5], [6, 6, 6]]
], dtype=np.int64)

# Formatted with metadata header
output = list(list_of_str(np_matrix, getmat="show"))

print(output)
# Output:
# [
#     '[1, 1, 1]', '[2, 2, 2]', '[3, 3, 3]',
#     '[4, 4, 4]', '[5, 5, 5]', '[6, 6, 6]',
#     "<class 'numpy.ndarray' ",
#     " dtype=int64 ",
#     " shape=(2, 3, 3)>"
# ]
```

---

### 5. PyTorch `Tensor` (`getmat`)

```python
import torch
from dvs_printf import list_of_str

tensor = torch.tensor([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0]
])

output = list(list_of_str(tensor, getmat="show"))

print(output)
# Output:
# [
#     '[1.0, 2.0, 3.0]',
#     '[4.0, 5.0, 6.0]',
#     "<class 'torch.Tensor' ",
#     " dtype=torch.float32 ",
#     " shape=torch.Size([2, 3])>"
# ]
```

---

### 6. Terminal Responsiveness & Word Wrapping (`divide_line`)

When a single string line exceeds the current terminal window length, `list_of_str` automatically invokes `divide_line` to break long lines at spaces:

```python
from dvs_printf import list_of_str

long_text = "This is an extremely long string that exceeds standard console boundaries and requires automatic line wrapping."

# Assuming terminal width is 40 characters
wrapped_output = list(list_of_str(long_text))

# Output splits cleanly across lines:
# [
#     "This is an extremely long string that",
#     "exceeds standard console boundaries and",
#     "requires automatic line wrapping."
# ]
```

---

### 7. Internal Integration with `printf()`

`printf()` calls `list_of_str()` as its very first step prior to applying ANSI colors, gradients, and animation routines:

```python
from dvs_printf import printf
import numpy as np

arr = np.eye(3)

# Animated matrix display with 'show' metadata
printf("Identity Matrix:", arr, style="async", getmat="show", color="cyan")
```

---
*© 2026 dvs-printf Team • Professional Console Animation*
