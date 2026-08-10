from ._base_exception import dvs_BaseException
from ._colored_vars   import YELLOW, SKYBLUE, RESET

class _Warning(dvs_BaseException, ValueError, Warning):
    """Custom warning class with styled ANSI output."""
    def __init__(self, value, message: str):
        self.message = f"{YELLOW}[WARNING]{RESET} {SKYBLUE}{message}{RESET}"
        super().__init__(value, self.message, skip=2)

    def __str__(self):
        return  self.message

    def print(self):
        print(self.message)


# ------------------------------------------------------
# Demo usage
# ------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         # Just raise our styled warning
#         raise Print_Warning("This is a test warning with yellow bold text.")
#     except Print_Warning as w:
#         print(w)