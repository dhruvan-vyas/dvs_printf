from dvs_printf.loaders._Spinner import (
    Spinner,
    ProgressUpdater,
)
import pytest
import time
import sys
import os

# --- Define the tasks to be used in the tests ---
def successful_task(duration: float):
    """A task that completes successfully after a given duration."""
    time.sleep(duration)
    return "SUCCESS_RESULT"

def failing_task():
    """A task that raises a ValueError."""
    raise ValueError("Something went wrong!")

def long_running_task():
    """A task designed to exceed the default timeout."""
    time.sleep(0.3)
    return "LONG_RUNNING_RESULT"

def progress_task(progress_updater: ProgressUpdater):
    """A task that reports its progress using the ProgressUpdater."""
    for i in range(11):
        progress_updater.set_progress(i * 10)
        time.sleep(0.005)
    return "PROGRESS_RESULT"

# --- Test Fixtures and Functions ---
@pytest.fixture
def spinner_instance():
    """
    A pytest fixture to provide a fresh Spinner instance with a short timeout for tests.
    """
    return Spinner(timeout=0.1, title="Test Spinner")

@pytest.fixture(autouse=True)
def capture_stdout():
    """
    Fixture to capture and restore stdout to prevent test output from mixing.
    """
    original_stdout_fd = os.dup(sys.stdout.fileno())
    null_fd = os.open(os.devnull, os.O_RDWR)
    
    # Redirect stdout to a null device
    os.dup2(null_fd, sys.stdout.fileno())
    
    yield
    
    # Restore stdout
    os.dup2(original_stdout_fd, sys.stdout.fileno())
    os.close(null_fd)
    os.close(original_stdout_fd)


# --- Core Functionality Tests ---

def test_successful_task_completion(spinner_instance):
    """
    Tests that a task completes successfully and returns the correct result.
    """
    result = spinner_instance(successful_task, duration=0.02)
    assert result == "SUCCESS_RESULT"

def test_failing_task_raises_exception(spinner_instance):
    """
    Tests that an exception raised within the task thread is correctly
    re-raised in the main thread by the Spinner.
    """
    with pytest.raises(ValueError, match="Something went wrong!"):
        spinner_instance(failing_task)

def test_timeout_on_long_running_task(spinner_instance):
    """
    Tests that a task that exceeds the set timeout raises a TimeoutError.
    """
    with pytest.raises(TimeoutError):
        spinner_instance(long_running_task)

def test_progress_updater(spinner_instance):
    """
    Tests that the ProgressUpdater object is correctly passed to the task
    and that the task can use it to update the spinner's progress.
    """
    result = spinner_instance(progress_task, progress_updater=True)
    assert result == "PROGRESS_RESULT"

# --- Configuration and Customization Tests ---

def test_custom_timeout(spinner_instance):
    """
    Tests that the timeout parameter can be overridden at runtime.
    """
    with pytest.raises(TimeoutError):
        # A 0.3-second task should time out with a 0.1-second timeout
        spinner_instance(successful_task, duration=0.3, timeout=0.1)

def test_different_spinner_style():
    """
    Tests that a different spinner style can be configured.
    """
    spinner = Spinner(style="dots", timeout=1)
    result = spinner(successful_task, duration=0.02)
    assert result == "SUCCESS_RESULT"

def test_custom_title_and_messages():
    """
    Tests that custom titles, final messages, and error messages are applied correctly.
    """
    spinner = Spinner(
        title="Custom Title",
        final_message="Task Completed!",
        error_message="Something Broke!"
    )
    result = spinner(successful_task, duration=0.02)
    assert result == "SUCCESS_RESULT"
    
# --- Decorator Test ---

def test_decorator_functionality():
    """
    Tests that the decorator works as expected, wrapping a function and running it with the spinner.
    """
    spinner = Spinner(timeout=1, title="Decorator Test")

    @spinner.decorator
    def decorated_task(duration):
        time.sleep(duration)
        return "DECORATOR_RESULT"
    
    result = decorated_task(duration=0.02)
    assert result == "DECORATOR_RESULT"