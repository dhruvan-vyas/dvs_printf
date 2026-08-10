import pytest
import time
from dvs_printf.loaders import LoadingBar, ProgressUpdater
from dvs_printf.exceptions.loader_exception import LoaderValueError

# --- Define the tasks to be used in the tests ---
def successful_task(duration: float):
    """A task that completes successfully after a given duration."""
    time.sleep(duration)
    return "SUCCESS_RESULT"

def failing_task():
    """A task that raises a ValueError."""
    raise LoaderValueError("Something went wrong!")

def long_running_task():
    """A task designed to exceed the default timeout."""
    time.sleep(1)
    return "LONG_RUNNING_RESULT"

def progress_task(progress_updater: ProgressUpdater):
    """A task that reports its progress using the ProgressUpdater."""
    for i in range(11):
        progress_updater.set_progress(i * 10)
        time.sleep(0.005)
    return "PROGRESS_RESULT"

# --- Test Fixtures and Functions ---
@pytest.fixture
def loader_instance():
    """
    A pytest fixture to provide a fresh LoadingBar instance for each test.
    """
    return LoadingBar(timeout=2.0, title_text="Test Loader")

def test_successful_task_completion(loader_instance):
    """
    Test that a task completes successfully and returns the correct result
    when it finishes before the timeout.
    """
    result = loader_instance(successful_task, duration=0.02)
    assert result == "SUCCESS_RESULT"

def test_failing_task_raises_exception(loader_instance):
    """
    Test that an exception raised within the task thread is correctly
    re-raised in the main thread by the LoadingBar.
    """
    with pytest.raises(ValueError): 
        loader_instance(failing_task)

def test_timeout_on_long_running_task(loader_instance):
    """
    Test that a task which exceeds the set timeout raises an exception.
    """
    with pytest.raises(Exception):
        loader_instance(long_running_task, timeout=0.3)

def test_progress_updater(loader_instance):
    """
    Test that the ProgressUpdater object is correctly passed to the task
    and that the task can use it to update the loading bar's progress.
    """
    result = loader_instance(progress_task, progress_updater=True, timeout=2.0)
    assert result == "PROGRESS_RESULT"