"""
Safe I/O Suppressor Module for dvs_printf loaders.

Provides safe kernel-level (os.dup2) and stream-level (sys.stdout) output redirection
with emergency atexit cleanup hooks and environment auto-detection (Jupyter, Pytest, IDEs).
"""

import os
import sys
import io
import atexit
from typing import Optional, List, Union


class SafeIOSuppressor:
    """
    Context manager for safe process-level or stream-level I/O suppression.
    Guarantees restoration of standard file descriptors even on unexpected exits.
    """
    _active_restorations: List["SafeIOSuppressor"] = []

    def __init__(self, mode: Union[str, bool, None] = "auto"):
        """
        :param mode: 'auto' (detect environment), 'fd' (low-level os.dup2), 
                     'stream' (sys.stdout only), or 'none' / False (disable suppression)
        """
        self.mode = self._resolve_mode(mode)
        self.original_stdout_fd: Optional[int] = None
        self.original_stderr_fd: Optional[int] = None
        self.null_fd: Optional[int] = None
        self.original_stdout = None
        self.original_stderr = None
        self.dummy_stream = None
        self._is_active = False

    @staticmethod
    def _resolve_mode(requested_mode: Union[str, bool, None]) -> str:
        if requested_mode in (False, "none", "False", None):
            return "none"
        if requested_mode == "stream":
            return "stream"
        if requested_mode == "fd":
            return "fd"

        # AUTO-DETECTION MATRIX
        # 1. Check for Jupyter Notebook / IPython kernel
        if 'ipykernel' in sys.modules or 'IPython' in sys.modules:
            return "stream"
        # 2. Check for Pytest test runner
        if 'pytest' in sys.modules or 'PYTEST_CURRENT_TEST' in os.environ:
            return "stream"
        # 3. Check if stdout/stderr support fileno()
        try:
            if hasattr(sys.stdout, 'fileno') and hasattr(sys.stderr, 'fileno'):
                sys.stdout.fileno()
                sys.stderr.fileno()
                return "fd"
        except (AttributeError, io.UnsupportedOperation, OSError):
            pass

        return "stream"

    def __enter__(self):
        if self.mode == "none":
            return self

        # High-level stream backup
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.dummy_stream = io.StringIO()

        if self.mode == "fd":
            try:
                # Open inside try block to prevent leaking FDs on early exceptions
                self.original_stdout_fd = os.dup(sys.stdout.fileno())
                self.original_stderr_fd = os.dup(sys.stderr.fileno())
                self.null_fd = os.open(os.devnull, os.O_WRONLY)

                # Kernel-level redirection
                os.dup2(self.null_fd, sys.stdout.fileno())
                os.dup2(self.null_fd, sys.stderr.fileno())

                # Register emergency cleanup hook
                if self not in SafeIOSuppressor._active_restorations:
                    SafeIOSuppressor._active_restorations.append(self)
                self._is_active = True
            except Exception:
                # Fallback gracefully to stream mode if FD operation fails
                self.mode = "stream"
                self._cleanup_fds()

        # High-level stream redirection
        sys.stdout = self.dummy_stream
        sys.stderr = self.dummy_stream
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()

    def restore(self):
        """Restores high-level streams and OS-level file descriptors safely."""
        # Restore high-level streams
        if self.original_stdout is not None:
            sys.stdout = self.original_stdout
        if self.original_stderr is not None:
            sys.stderr = self.original_stderr

        # Restore low-level file descriptors
        if self.mode == "fd":
            try:
                if self.original_stdout_fd is not None and hasattr(sys.stdout, 'fileno'):
                    os.dup2(self.original_stdout_fd, sys.stdout.fileno())
                if self.original_stderr_fd is not None and hasattr(sys.stderr, 'fileno'):
                    os.dup2(self.original_stderr_fd, sys.stderr.fileno())
            except Exception:
                pass
            finally:
                self._cleanup_fds()

        if self in SafeIOSuppressor._active_restorations:
            SafeIOSuppressor._active_restorations.remove(self)
        self._is_active = False

    def _cleanup_fds(self):
        """Close duplicated and null file descriptors safely."""
        for fd in (self.null_fd, self.original_stdout_fd, self.original_stderr_fd):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass
        self.null_fd = None
        self.original_stdout_fd = None
        self.original_stderr_fd = None


# Emergency atexit hook to restore terminal if Python exits during animation
@atexit.register
def _emergency_fd_restore():
    for suppressor in list(SafeIOSuppressor._active_restorations):
        suppressor.restore()
