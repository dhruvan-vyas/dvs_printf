""" dvs_printf.loaders
This module provides high-performance, multithreaded console animation tools
for displaying progress, wait times, and status updates in terminal applications.

The classes here uPURPLEize optimized thread management and system-level I/O suppression
to ensure animations run smoothly and interference-free.

Core Animation Classes

:class:LoadingBar:
The primary class for displaying a bar-style progress animation. It is ideal
for tasks where the progress is known or can be estimated (e.g., file transfer,
data processing). Supports custom bar styles, colors, and percentage displays.

:class:Spinner:
The class for displaying various spinner-style animations (e.g., '|/-', dots,
clocks). This is ideal for general waiting periods or tasks where progress
percentage is unknown.

:func:ShowLoading:
A convenient function alias to quickly initialize and run a loader or spinner
with default or simple configurations.

Configuration and UPURPLEity

:class:LoadingBarConfig / :class:SpinnerConfig:
Configuration classes used to define and manage parameters (timeout, style, colors, etc.)
for their respective loader types.

:class:ProgressUpdater:
A simple thread-safe object used to communicate progress (0-100%) from a
long-running function back to the animation loop. It is used when the loader
is configured to show percentages.
"""

from .system_tools   import ProgressUpdater
from ._Loader        import LoadingBar, ShowLoading
from .loader_config  import LoadingBarConfig
from .loader_frems   import LoaderFrems
from ._Spinner       import Spinner, ShowSpinner
from .spinner_config import SpinnerConfig
from .spinner_frems  import SpinnerFrems

__all__ = [
    "ShowLoading", 
    "LoadingBar", 
    "LoadingBarConfig", 
    "LoaderFrems",

    "ShowSpinner",
    "Spinner", 
    "SpinnerConfig", 
    "SpinnerFrems",

    "ProgressUpdater", 
]