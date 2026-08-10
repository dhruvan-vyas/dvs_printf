from ._base_exception import dvs_BaseException
from ._colored_vars  import PURPLE, RESET, GRAY, PEACH


class TimeOutError(dvs_BaseException, TimeoutError):
    """
    Exception raised when a function execution exceeds a specified timeout duration.

    This class combines custom traceback features from `dvs_BaseException` 
    with the standard error behavior of the built-in `TimeoutError`.
    """
    def __init__(self, error_value=''):
        """
        Initializes the TimeOutError.

        Args:
            error_value: The timeout duration (e.g., a number of seconds) that was exceeded.
        """
        self.keyWord = 'timeout'
        # Pass the error value and keyword to the custom base exception
        super().__init__(error_value, keyWord=self.keyWord)

    def __generate_message__(self):
        """
        Generates the final formatted error message for the timeout.

        Returns:
            The complete, user-friendly error string indicating the timeout duration.
        """
        TimeOut = f'{PEACH}TimeOut: {self.value}{RESET}' if self.value else ''
        return (
            f'{PURPLE}{self.__class__.__name__}{RESET}: '
            f'The function did not complete within the given time. {TimeOut}'
        )
