# # new_loadingbar/config.py
# from dataclasses    import dataclass, asdict, field, fields
# from typing         import Union, Optional, TYPE_CHECKING
from ..colors       import Colors, ColorInput, GredinatInput
# from .SpinnerFrems import SpinnerFrems

# if TYPE_CHECKING:
#     from .system_tools import ProgressUpdater

# # --- Spinner Configuration Data Class ---
# @dataclass
# class SpinnerConfig:
#     timeout: int  = 40
#     inject_progress: Optional["ProgressUpdater"] = None
#     style: SpinnerFrems | str  = "arrow"
#     animation_position:    str  = "before"

#     # Messages
#     title:                  str = "Loading"
#     attrs: list[str] = field(default_factory=list)
#     final_message: Optional[str] = None
#     error_message: Optional[str] = None

#     # Other settings
#     stay:           bool = True
#     show_progress:  bool = True
#     show_timer:     bool = True
#     reversed_timer: bool = False

#     # Colors linked to messages/elements
#     spinner_color:       Colors | GredinatInput  = None
#     title_color:         Colors | GredinatInput  = None
#     final_message_color: Colors | ColorInput = "springgreen"
#     error_message_color: Colors | ColorInput = "scarlet"
#     timer_color:         Colors | ColorInput = "pink"
#     progress_color:      Colors | ColorInput = "gray"

#     def __iter__(self):
#         yield from [(f.name, getattr(self, f.name)) for f in fields(self)]

#     def update(self, other: Union["SpinnerConfig", dict]) -> "SpinnerConfig":
#         """
#         Update the current config with values from another SpinnerConfig or a dict.\\
#         Returns self for chaining.
#         """
#         # ==================(NEW V3)=======================
#         if isinstance(other, SpinnerConfig):
#             setattr(self, "style", other.style)
#             other = asdict(other)
#             del other["style"]

#         for f in fields(self):
#             if f.name in other and other[f.name] is not None:
#                 setattr(self, f.name, other[f.name])

#         return self






from dataclasses import dataclass, asdict, field, fields
from typing import Tuple, Union, Optional, TYPE_CHECKING, List, Dict, Any
from ..colors import ColorInput, GredinatInput

if TYPE_CHECKING:
    # from ..colors.colors import Colors
    from ..colors       import Colors, ColorInput, GredinatInput
    from .system_tools import ProgressUpdater
    from .spinner_frems import SpinnerFrems


# --- Type Aliases (Assumed from Project Context) ---
# ColorInput = Union[str, Tuple[int, int, int]]
# GredinatInput = Union[List[ColorInput], Tuple[ColorInput, ...]]
# ----------------------------------------------------


# --- Spinner Configuration Data Class ---
@dataclass
class SpinnerConfig:
    """
    A data container for all Spinner configuration settings.

    This class defines the animation style, colors, timing, and behavior for the 
    console spinner used to indicate an ongoing background task.

    Attributes:
        timeout (int): Maximum time (in seconds) the associated task is allowed to run 
                       before raising a timeout error. Defaults to 40.
        inject_progress (Optional[ProgressUpdater]): Internal marker for injecting the 
                                                     progress tracking object into the task.
        style (SpinnerFrems | str): The animation style to use (e.g., 'dots', 'arrow'). 
                                     Accepts a string name or a pre-configured SpinnerFrems object.
        animation_position (str): Position of the spinner relative to the title ('before', 'after', 'dual').

        # Message and Appearance
        title (str): The primary message displayed next to the spinner (e.g., "Loading...").
        attrs (List[str]): List of text attributes to apply to the title (e.g., ['bold', 'italic']).
        final_message (Optional[str]): Custom message displayed upon successful completion.
        error_message (Optional[str]): Custom message displayed if a task-level error occurs.

        # Behavior
        stay (bool): If True, the completed spinner line remains on the screen. If False, the line is cleared.
        show_progress (bool): If True, displays percentage completion (0.0% to 100.0%).
        show_timer (bool): If True, displays elapsed time (or time remaining if reversed_timer=True).
        reversed_timer (bool): If True, calculates and displays the estimated time remaining based on timeout.

        # Color Configuration
        spinner_color (Colors | GredinatInput): Color(s) for the spinner frames. Accepts a single color or a gradient.
        title_color (Colors | GredinatInput): Color for the main title text.
        final_message_color (Colors | ColorInput): Color for the success message.
        error_message_color (Colors | ColorInput): Color for the error message/highlight.
        timer_color (Colors | ColorInput): Color for the timing label.
        progress_color (Colors | ColorInput): Color for the percentage progress label.
    """
    timeout: int = 40
    inject_progress: Optional["ProgressUpdater"] = None
    style: Union["SpinnerFrems", str] = "arrow"
    animation_position: str = "before"

    # Messages
    title: str = "Loading"
    attrs: List[str] = field(default_factory=list)
    final_message: Optional[str] = None
    error_message: Optional[str] = None

    # Other settings
    stay: bool = True
    show_progress: bool = True
    show_timer: bool = True
    reversed_timer: bool = False

    # Colors linked to messages/elements
    spinner_color: Union["Colors", GredinatInput] = None
    title_color: Union["Colors", GredinatInput] = None
    final_message_color: Union["Colors", ColorInput] = "springgreen"
    error_message_color: Union["Colors", ColorInput] = "scarlet"
    timer_color: Union["Colors", ColorInput] = "pink"
    progress_color: Union["Colors", ColorInput] = "gray"

    def __iter__(self):
        """Allows iteration over field names and values."""
        yield from [(f.name, getattr(self, f.name)) for f in fields(self)]

    def update(self, other: Union["SpinnerConfig", Dict[str, Any]]) -> "SpinnerConfig":
        """
        Updates the current configuration with settings from another object or dictionary.

        Args:
            other (SpinnerConfig | dict): The source object/dictionary containing new settings.

        Returns:
            SpinnerConfig: The updated instance of the configuration class (self).
        """
        if isinstance(other, SpinnerConfig):
            # Special handling for 'style' attribute to preserve its type if possible
            setattr(self, "style", other.style)
            other_dict = asdict(other)
            del other_dict["style"] # Avoid double processing the style
        else:
            other_dict = other

        for f in fields(self):
            # If the field is 'style', we already handled it or it's not present in 'other'
            if f.name == 'style':
                continue

            if f.name in other_dict and other_dict[f.name] is not None:
                setattr(self, f.name, other_dict[f.name])

        return self

    def __add__(self, other: "SpinnerConfig") -> "SpinnerConfig":
        """
        Combines two SpinnerConfig objects into a new one.

        Values from `other` override values from `self`.

        Args:
            other (SpinnerConfig): The configuration to merge into the current one.

        Returns:
            SpinnerConfig: A new instance containing the merged configuration.
        """
        if not isinstance(other, SpinnerConfig):
            return NotImplemented

        combined_data = asdict(self)
        for k, v in asdict(other).items():
            if v is not None:
                combined_data[k] = v
        return SpinnerConfig(**combined_data)
