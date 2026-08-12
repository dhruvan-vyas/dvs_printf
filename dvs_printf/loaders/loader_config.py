from typing      import Union, Optional, TYPE_CHECKING, List, Tuple
from dataclasses import dataclass, asdict, fields

# Type aliases for color inputs (assumed to be defined elsewhere)
ColorInput = Union[str, Tuple[int, int, int]]
GredinatInput = Union[List[ColorInput], Tuple[ColorInput, ...]]
# Forward declaration for type checking external classes
if TYPE_CHECKING:
    from .system_tools   import ProgressUpdater
    from ..colors.colors import Colors

@dataclass
class LoadingBarConfig:
    """
    A data container for all LoadingBar configuration settings.

    This class defines the visual style, colors, dimensions, and behavior for the
    console loading bar. It should be used to configure a `LoadingBar` instance.

    Attributes:
        title_text (str): The main message displayed alongside the bar (e.g., "Processing").
        inject_progress (Optional[ProgressUpdater]): Internal marker indicating if the 
            task requires a ProgressUpdater object (usually set automatically by run).
        style (str): The character style of the bar itself (e.g., "grow", "line").
        final_message (Union[str, bool, None]): Custom message displayed on successful completion. 
        animation_strategy (Optional[type]): Reserved for internal strategy injection.
        bar_length (int): The fixed length of the bar characters (excluding borders).
        bar_borders (Optional[str]): Optional custom border characters (e.g., "[]", "<>"). 
            Overrides the style's default borders.

            ## Advanced Settings
        refresh_rate (float): Delay (in seconds) between animation frame updates. Automatically 
                              calculated based on `timeout` or overridden by `FPS`.
        timeout (Optional[int]): Maximum time in seconds the associated task is allowed to run. 
                                 Raises TimeOutError if exceeded. Defaults to 80.
        stay (Optional[bool]): If True, the completed bar remains on the screen. If False, 
                               the line is cleared after completion.
        show_gradient_anyway (bool): Forces character-by-character color gradient mode 
                                    even in terminals with limited color support.
        grid_rotation_speed (int): Speed of color rotation if using a gradient-based bar 
                                   style (1 is slow, 10 is fast). Defaults to 1.
        full_screen_mode (Optional[bool]): If True, attempts to stretch the bar to the 
                                           full width of the terminal.
        FPS (Optional[int]): Frames Per Second target for animation. Overrides `refresh_rate`.

            ## Color Configuration (All accept named color, hex string, or RGB tuple)
        title_color (ColorInput | GredinatInput): Color for the main `title_text`.
        bar_color (ColorInput | GredinatInput): Color(s) for the filled portion of the bar. 
                                                Accepts a single color or a gradient (list/tuple).
        unfilled_bar_color (ColorInput): Color for the empty portion of the bar.
        bar_borders_color (ColorInput): Color for the border characters.
        percentage_color (ColorInput): Color for the percentage label (e.g., "99.0%").
        timing_color (ColorInput): Color for the timing label (e.g., "in 1.2s").
        error_color (ColorInput): Color used for error messages and highlighting failed bars.
    """
    # Defaults
    title_text: str = "Loading"
    inject_progress: Optional["ProgressUpdater"] = None
    style: str = "grow"
    final_message: Union[str, bool, None] = None
    # error_message: Union[str, bool, None] = None
    animation_strategy: Optional[type] = None
    bar_length: int = 40
    bar_borders: str = None

    # Advanced settings
    refresh_rate: float = 0.1
    timeout: Optional[int] = 80
    stay: bool = None
    show_gradient_anyway: bool = False
    grid_rotation_speed: int = 1
    full_screen_mode: bool = None
    FPS: int = None
    suppress_io: Union[str, bool, None] = "auto"

    # Colors
    title_color:        Union["Colors", GredinatInput, ColorInput] = (255, 255, 255)
    bar_color:          Union["Colors", GredinatInput, ColorInput] = "green"
    unfilled_bar_color: Union["Colors", ColorInput] = "#2B2B2B"
    bar_borders_color:  Union["Colors", ColorInput] = "#00aeff"
    percentage_color:   Union["Colors", ColorInput] = "#ea9329"
    timing_color:       Union["Colors", ColorInput] = "#00aeff"
    error_color:        Union["Colors", ColorInput] = "scarlet"


    def update(self, other: Union["LoadingBarConfig", dict]) -> "LoadingBarConfig":
        """
        Updates the current configuration with settings from another object or dictionary.

        Non-None values in `other` will override the existing attributes of this instance.

        Args:
            other (LoadingBarConfig | dict): The source object/dictionary containing new settings.

        Returns:
            LoadingBarConfig: The updated instance of the configuration class (self).
        """
        if isinstance(other, LoadingBarConfig):
            other = asdict(other)

        for f in fields(self):
            if f.name in other and other[f.name] is not None:
                setattr(self, f.name, other[f.name])
        return self

    def __add__(self, other: "LoadingBarConfig") -> "LoadingBarConfig":
        """
        Combines two LoadingBarConfig objects into a new one.

        Values from `other` override values from `self`.

        Args:
            other (LoadingBarConfig): The configuration to merge into the current one.

        Returns:
            LoadingBarConfig: A new instance containing the merged configuration.
        """
        if not isinstance(other, LoadingBarConfig):
            return NotImplemented

        combined_data = asdict(self)
        for k, v in asdict(other).items():
            if v is not None:
                combined_data[k] = v
        return LoadingBarConfig(**combined_data)
