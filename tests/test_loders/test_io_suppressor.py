import sys
import io
import pytest
from dvs_printf.loaders.io_suppressor import SafeIOSuppressor
from dvs_printf.loaders import LoadingBar, Spinner


def test_safe_io_suppressor_stream_mode():
    """Verify stream mode redirects sys.stdout cleanly."""
    original_stdout = sys.stdout
    with SafeIOSuppressor(mode="stream") as suppressor:
        sys.stdout.write("Test output inside suppressor")
        assert sys.stdout != original_stdout
    assert sys.stdout == original_stdout


def test_safe_io_suppressor_none_mode():
    """Verify none / False mode leaves sys.stdout intact."""
    original_stdout = sys.stdout
    with SafeIOSuppressor(mode=False):
        assert sys.stdout == original_stdout
    assert sys.stdout == original_stdout


def test_safe_io_suppressor_auto_mode():
    """Verify auto mode resolves to a valid mode and cleans up streams."""
    original_stdout = sys.stdout
    with SafeIOSuppressor(mode="auto") as suppressor:
        assert suppressor.mode in ("fd", "stream")
    assert sys.stdout == original_stdout


def test_loader_and_spinner_suppress_io_config():
    """Verify LoadingBar and Spinner accept suppress_io configuration."""
    loader = LoadingBar(title_text="Testing", suppress_io="stream")
    assert loader.suppress_io == "stream"

    spinner = Spinner(title="Testing", suppress_io="stream")
    assert spinner.suppress_io == "stream"
