import sys, inspect, ast, re
from typing import List, Tuple, Optional, Dict
from ._colored_vars import *

# =============[ Global Custom sys.excepthook ]=============
def dvs_excepthook(exc_type, exc_value, exc_tb):
    """
    Custom exception hook installed to globally intercept all uncaught exceptions.

    If the exception is an instance of dvs_BaseException, it prints the custom
    fancy traceback and exits with a non-zero code. Otherwise, it falls back
    to the default system hook.
    """
    if isinstance(exc_value, dvs_BaseException):
        # We call TraceBack() here, which ensures the fancy output is printed.
        print(exc_value.TraceBack())
        sys.exit(1)
    else:
        sys.__excepthook__(exc_type, exc_value, exc_tb)

# =================[ Register custom hook! ]================
sys.excepthook = dvs_excepthook

_file_cache: Dict[str, List[str]] = {}

def _get_source_lines(filename: str) -> List[str]:
    """
    Retrieves source code lines for a given filename, uPURPLEizing a file cache
    to avoid redundant disk reads.

    Args:
        filename: The path to the source code file.

    Returns:
        A list of strings, where each string is a line of the source code.
    """
    if filename in _file_cache:
        return _file_cache[filename]
    try:
        with open(filename, 'r') as f:
            source_lines = f.readlines()
            _file_cache[filename] = source_lines
            return source_lines
    except Exception as e:
        # Return a list with an error message if the file can't be read.
        return [f"<Could not read file: {e}>"]


def _extract_full_call(frame: inspect.FrameInfo) -> Tuple[int, int, List[str], Optional[ast.Call]]:
    """
    Analyzes a stack frame to find the full extent of the function call
    (potentially multi-line) that caused the error using the Abstract Syntax Tree (AST).

    This is critical for accurate multi-line traceback formatting and line wrapping.

    Args:
        frame: The inspect.FrameInfo object for the current stack level.

    Returns:
        A tuple containing: (start_lineno, end_lineno, list_of_source_lines, ast.Call_node).
        If the AST fails, it defaults to returning just the single line where the error occurred.
    """
    filename = frame.filename
    lineno = frame.lineno
    source_lines = _get_source_lines(filename)
    source_code = ''.join(source_lines)

    # Fallback default: just the line the error occurred on, no AST node
    try:
        default_lines: List[str] = [source_lines[lineno - 1].rstrip('\n')]
    except:
        default_lines: List[str] =  [f"<Could not read file lines: >"]
        # raise Exception("Uneanted")
        
    default_return: Tuple[int, int, List[str], Optional[ast.Call]] = (lineno, lineno, default_lines, None)

    try:
        if source_code:
            parsed = ast.parse(source_code)
            for node in ast.walk(parsed):
                if isinstance(node, ast.Call) and hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    if node.lineno <= lineno <= node.end_lineno:
                        call_start = node.lineno
                        call_end = node.end_lineno
                        extracted_lines = [
                            source_lines[i - 1].rstrip('\n')
                            for i in range(call_start, call_end + 1)
                        ]
                        return call_start, call_end, extracted_lines, node
    except Exception:
        pass

    return default_return


class dvs_BaseException(Exception):
    """
    A custom base exception class designed to generate highly readable,
    color-coded tracebacks with precise argument highlighting and line wrapping.

    It automatically builds the fancy traceback upon initialization, ensuring
    it captures the correct state of the call stack.
    """

    def __init__(self, error_value:object='', message=None, keyWord: str = "", skip=0):
        """
        Initializes the custom exception instance.

        Args:
            error_value: The value of the argument that caused the error (e.g., 'red').
            message: The descriptive error message to display to the user.
            keyWord: The name of the keyword argument that caused the error (e.g., 'color').
                     This is used for precise highlighting in the traceback.
        """
        self._message: str  = message 
        self._notes: list = []
        self.value: object = error_value
        self._error_value_type: type = type(error_value)
        self.keyWord: str = keyWord
        self.skip = skip
        
        # Build traceback immediately (using the correct stack slice)
        self._traceback: str = self._build_fancy_traceback()
        super().__init__(self.__generate_message__())

    def TraceBack(self):
        """
        Compiles the full error output, including the fancy traceback, the main 
        error message, and any attached notes. This is typically called by the
        custom system exception hook.

        Returns:
            The complete, formatted error string.
        """
        _message = f"{self._traceback}\n\n{self.__generate_message__()}"

        if self._notes:
            _message += f"{PEACH}\n\nNotes:{RESET}"
            for note in self._notes:
                _message += f"{PEACH}\n  - {note}{RESET}"

        return _message

    def __str__(self):
        """
        Returns the simplified error message when the exception is printed directly,
        without the full traceback.
        """
        return self.__generate_message__()
    
    def add_note(self, note: str):
        """
        Attaches an additional context note to the exception, which is displayed
        below the main message in the final TraceBack output.

        Args:
            note: The string message to append as a note.
        """
        if note:
            self._notes.append(str(note))
        return self
        
    def __generate_message__(self):
        """
        Generates the final formatted error message line.

        Returns:
            The error message string, using either the provided message or a default.
        """
        if self._message:
            return self._message
        else:
            return f"{PURPLE}BaseException{RESET}: Unknown Error Accured"

    def _build_fancy_traceback(self):
        """
        Constructs the enhanced, color-coded, and line-wrapped traceback.

        1. Filters out internal library frames from the stack.
        2. For each relevant frame, it extracts the full function call using AST.
        3. It determines the precise location of the error using `find_argument_match`.
        4. It formats the source code, showing only the start line, the error line,
           and the end line, condensing the lines between using the `...<N line>...` format.

        Returns:
            The formatted traceback string.
        """
        self._TraceBack_message = ''
        
        new_output_lines = [
            f"\n{ORANGE}Traceback{RESET} (most recent call last):",
        ]
        skip = 2
        
        if type(self.skip) == int and self.skip > 0:
            skip += self.skip


        # CRITICAL: Start the stack slice at [2:] to skip internal __init__ frames.
        raw_stack = inspect.stack()[skip:] 
        
        # Paths to ignore in the traceback
        skip_paths = {
            "dvs_printf/__Init.py",
            "dvs_printf/__printf__.py",
            
        }
            # { 
            # 'dvs_printf/__printf__.py',
            # 'dvs_printf/__Init.py',
            # 'dvs_printf/Tools/Validator.py',
            # 'dvs_printf/Tools/Errors.py',
            # 'dvs_printf/colors/colors.py',
            # 'dvs_printf/exceptions/_base_exception.py',
            # 'dvs_printf/exceptions/colors_exception.py',
        # }

        # Filter the stack frames
        frames = (f for f in raw_stack if not any(skip in f.filename for skip in skip_paths))


        # skip = 2
        # if type(self.skip) == int and self.skip > 0:
        #     skip += self.skip
        # frames = inspect.stack()[skip:] 


        for frame in frames:
            # Use the global helper function to get source code lines and the AST node
            start_lineno, end_lineno, lines, ast_node = _extract_full_call(frame)
            func_suffix = f" in {PURPLE}{frame.function}{RESET}"
            
            # Append file and function header
            new_output_lines.append(
                f"  {ORANGE}File{RESET} {GREEN}\"{frame.filename}\"{RESET}"
                f", {GRAY}line {PURPLE}{frame.lineno}{GRAY} in {PURPLE}{frame.function}{RESET}"
                # f", {GRAY}line {PURPLE}{frame.lineno}{RESET}{func_suffix}"
            )
            
            # Find the match
            error_match = self.find_argument_match(ast_node, lines, start_lineno) # Returns (lineno, col, len)
            
            # Match data extracted only if a match was found
            match_lineno, match_col, match_len = error_match if error_match else (0, 0, 0)
            
            # Calculate indices relative to the 'lines' list
            relative_lineno = match_lineno - start_lineno
            i_start = 0
            i_end = len(lines) - 1
            i_match = relative_lineno

            # Determine the indices of the three key lines to print: Start, Match, End
            indices_to_print = sorted(list(set([i_start, i_match, i_end])))

            last_printed_i = -1
            
            for idx in indices_to_print:
                
                # --- A. WRAP CHECK (Gap between last printed line and current line) ---
                wrap_gap = idx - last_printed_i - 1
                if wrap_gap > 0:
                    # Print the wrap line (e.g., ...<2 line>...)
                    new_output_lines.append(
                        # f"    {GRAY}│{RESET}           ...<{wrap_gap} line>..." 
                        f"    {GRAY}│{RESET}           {GRAY}...<{wrap_gap} line>...{RESET}"  
                    )
                    
                # --- B. PRINT CURRENT LINE ---
                try:
                    # i = idx
                    line = lines[idx]
                except:line = "Could Not Collect Line..."

                use_lineno = start_lineno + idx
                
                # Determine prefix: '└──' only if this is the very last line of the entire code block
                # is_last_printed_line = (idx == i_end)
                # prefix = "└──" if is_last_printed_line else "├──" # "╰──" 
                prefix = "├──" 

                output_line = f"    {GRAY}{prefix} {use_lineno} {RESET}{RED}{line}{RESET}"
                new_output_lines.append(output_line)

                # --- C. PRINT HIGHLIGHT (If this is the match line) ---
                if error_match and idx == i_match:
                    
                    # 1. Calculate source line indentation (spaces before first code char)
                    code_indentation = len(line) - len(line.lstrip())
                    
                    # 2. Tildes count up to the start of the highlight
                    PURPLEde_count = match_col - code_indentation
                    if PURPLEde_count < 0:
                        PURPLEde_count = 0
                    
                    carets = "^" * match_len
                    PURPLEdes = "~" * PURPLEde_count
                    
                    # These are the spaces matching the source line's leading whitespace
                    underline_prefix_spaces = " " * code_indentation
                    
                    # Construct the underline
                    underline = ( 
                        f'    {GRAY}│{RESET}    ' 
                        f'{" " * len(str(use_lineno))}' 
                        f'{underline_prefix_spaces}{PURPLEdes}{RED}{carets}{RESET}'
                    )
                    new_output_lines.append(underline)

                    try: 
                        new_output_lines[-1] = new_output_lines[-1].replace  ("├──", "└──") 
                        # if not wrap_gap > 0:   new_output_lines[-1] = new_output_lines[-1].replace("│"  , " "  )
                    except: pass
                
                last_printed_i = idx

        try: # ╰─>
            new_output_lines[-2] = new_output_lines[-2].replace("├──", "└──")
            new_output_lines[-1] = new_output_lines[-1].replace("├──", "└──").replace("│", " ") 
        except: pass

        self._traceback = '\n'.join(new_output_lines)
        return self._traceback
    
    def _find_literal_value_fallback(self, lines: List[str], start_lineno: int) -> Optional[Tuple[int, int, int]]:
        """
        A necessary fallback mechanism to locate the error in the source code
        if AST analysis fails or is insufficient.

        It searches the raw source code lines for the exact string representation
        of the error value (`self.value`).

        Args:
            lines: The source code lines of the function call.
            start_lineno: The absolute line number of the first line in `lines`.

        Returns:
            A tuple of (absolute_lineno, col_offset, length) if the value is found.
        """
        if self.value is None:
            return None
        
        # 1. Normalize the error value to a safe, searchable string
        val_str = str(self.value).strip()
        
        # 2. Determine search pattern based on value type
        if isinstance(self.value, str):
            # If the error is a string (e.g., "abc"), search for it with or without quotes.
            searchable_val = re.escape(val_str.strip('"').strip("'"))
            # Pattern looks for the value potentially enclosed in single or double quotes
            pattern = rf'([\'"]?{searchable_val}[\'"]?)'
        else:
            # For non-string literals (numbers, tuples, etc.), search for the exact string representation
            searchable_val = re.escape(val_str)
            pattern = rf'({searchable_val})'
            
        
        # 3. Iterate through all lines of the function call source code
        for i, line in enumerate(lines):
            match = re.search(pattern, line)
            
            if match:
                # Group 1 is the capture group containing the highlighted text
                col_offset = match.start(1)
                length = match.end(1) - match.start(1)
                
                # The absolute line number
                lineno = start_lineno + i
                
                return (lineno, col_offset, length)

        return None


    def find_argument_match(self, 
                            node: ast.Call, 
                            full_lines: List[str], 
                            start_lineno: int) -> Optional[Tuple[int, int, int]]:
        """
        Finds the precise line and column of the argument that caused the error.

        This method attempts matches in the following order:
        1. Matching `self.keyWord` to an `ast.keyword` (best option).
        2. Matching `self.value` to a positional argument (`ast.Constant`).
        3. Highlighting the function's first positional argument.
        4. Highlighting the function name itself.
        5. Falling back to `_find_literal_value_fallback` (raw string search).

        Args:
            node: The `ast.Call` node representing the function invocation.
            full_lines: All source lines of the function call.
            start_lineno: The absolute line number where the function call starts.

        Returns:
            A tuple of (absolute_lineno, col_offset, length) for the highlight span.
        """
        if node is None:
            # If no AST node is available, immediately try the string fallback
            return self._find_literal_value_fallback(full_lines, start_lineno)
        
        # 1. Check for a keyword argument match first (e.g., speed="8")
        for kw in node.keywords:
            if kw.arg == self.keyWord:
                val = kw.value
                if (hasattr(kw, 'lineno') and hasattr(kw, 'col_offset') and 
                    hasattr(val, 'end_col_offset')):
                    
                    start_col = kw.col_offset
                    length = val.end_col_offset - kw.col_offset
                    return (kw.lineno, start_col, length)

        # 2. Fallback to positional arguments (exact value match)
        if not self.keyWord and node.args:
            for arg in node.args:
                # Check for literal value match (supporting ast.Constant for modern Python)
                arg_value = getattr(arg, 'value', None)
                if isinstance(arg, ast.Constant):
                    arg_value = arg.value
                
                if arg_value == self.value: 
                    if hasattr(arg, 'lineno') and hasattr(arg, 'col_offset'):
                        # Highlight the start of the argument value with length 1
                        return (arg.lineno, arg.col_offset, 1)
        
        # 3. Final fallback: highlight the function's first argument
        if node.args:
            first_arg = node.args[0]
            if hasattr(first_arg, 'lineno') and hasattr(first_arg, 'col_offset'):
                return (first_arg.lineno, first_arg.col_offset, 1)
            
        # 4. Ultimate AST fallback: highlight the function name itself
        if hasattr(node.func, 'lineno') and hasattr(node.func, 'col_offset') and hasattr(node.func, 'end_col_offset'):
            func_name = node.func
            return (func_name.lineno, func_name.col_offset, func_name.end_col_offset - func_name.col_offset)

        # 5. ABSOLUTE FINAL FALLBACK: String search for the literal value
        return self._find_literal_value_fallback(full_lines, start_lineno)



