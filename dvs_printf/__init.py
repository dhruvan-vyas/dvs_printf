from .__printf__ import printf as pf
from .colors     import Colors
from .exceptions import _Warning
from ._validator import (   _validate_style,
                            _validate_speed,
                            _validate_delay,
                            _validate_attrs,
                            _validate_getmat,
                        )


class Init:
    """
    The primary initializer class for the dvs_printf module.

    This class allows users to set default animation parameters (style, speed, 
    colors, etc.) once. The configured settings are automatically applied 
    when the instance's `.printf()` method is called, eliminating the need 
    to specify the same arguments repeatedly.

    All parameters are validated immediately upon assignment via property setters.
    """
    def __init__(self,
        style: str | None = 'typing', 
        speed: int | float | None = 3, 
        delay: int | float | None = 0,  
        stay: bool |         None = True,
        attrs : list[str]  | None = [],
        colors: Colors     | None = None,
        getmat: bool | str | None = False,
    ):
        """
        Initializes the configuration instance with default or user-provided values.

        Args:
            style (str, optional): Default animation style (e.g., 'typing', 'right').
            speed (int | float, optional): Default animation speed multiplier (1-7).
            delay (int | float, optional): Default delay between animation phases.
            stay (bool, optional): Default setting for whether the final output remains visible.
            attrs (list[str], optional): Default text attributes (e.g., ['bold', 'italic']).
            colors (Colors, optional): Default color configuration object (must be an instance of Colors).
            getmat (bool | str, optional): Default setting for complex array handling (e.g., NumPy/Tensorflow).
        """
        [   self.style , 
            self.speed , 
            self.delay , 
            self.stay  , 
            self.attrs ,
            self.colors,
            self.getmat,
        ] = [ 
            style,
            speed,
            delay,
            stay,
            attrs,
            colors,
            getmat,
        ]

    # ====================== [ Style ]
    @property
    def style(self) -> str:
        """The currently configured default animation style."""
        return self._style
        
    @style.setter
    def style(self, value: str) -> None:
        """Validates and sets the default animation style."""
        _validate_style(str(value).lower())
        self._style = value

    # ====================== [ Speed ]
    @property
    def speed(self) -> int | float:
        """The currently configured default animation speed multiplier."""
        return self._speed
    
    @speed.setter
    def speed(self, value: int | float) -> None:
        """Validates and sets the default animation speed multiplier (1-7)."""
        _validate_speed(value)
        self._speed = value

    # ====================== [ Delay ]
    @property
    def delay(self) -> int | float:
        """The currently configured default delay between animation phases."""
        return self._delay
    
    @delay.setter
    def delay(self, value: int | float) -> None:
        """Validates and sets the default delay value."""
        _validate_delay(value)
        self._delay = value 

    # ====================== [ Stay ]
    @property 
    def stay(self) -> bool:
        """The currently configured default setting for persistence."""
        return self._stay
    
    @stay.setter
    def stay(self, value: bool) -> None:
        """Sets the default stay behavior (True to keep output, False to clear)."""
        self._stay = value

    # ====================== [ attrs ] 
    @property
    def attrs(self):
        """The currently configured default list of text attributes (e.g., ['bold'])."""
        return self._attrs
    
    @attrs.setter
    def attrs(self, value: Colors | None = None):
        """Validates and sets the default list of text attributes."""
        _validate_attrs(value)
        self._attrs = value

    # ====================== [ Colors ] 
    @property
    def colors(self):
        """The currently configured default Colors object for styling."""
        return self._colors
    
    @colors.setter
    def colors(self, value: Colors | None = None) -> None:
        """
        Validates that the input is an instance of the Colors class or None, and sets it.

        Raises:
            ColorsValueError: If the value is not a Colors instance.
        """
        if value is None or type(value).__name__ == "Colors": 
            self._colors = value
        else: 
            from .exceptions.colors_exception import ColorsValueError
            raise ColorsValueError(
                    error_value=value,
                    message="init.colors only accepts instence of Colors class as input.")

    # ====================== [ Getmat ]
    @property
    def getmat(self) -> bool | str:
        """The currently configured default setting for complex array handling (getmat)."""
        return self._getmat

    @getmat.setter
    def getmat(self, value: bool | str) -> None:
        """Validates and sets the default array handling mode."""
        _validate_getmat(value)
        self._getmat = value

    # ====================== [ Printf Function ]
    def printf(
        self,
        *values: object,
        style:  str  |         None = None, 
        speed:  int  | float | None = None,
        delay:  int  | float | None = None, 
        stay:   bool |         None = None, 
        getmat: bool | str   | None = None,
        attrs:  list [ str ] | bool = None,
        colors:     tuple[tuple[int, int, int] | str] | None = None,
        background_color: tuple[int, int, int] | str  | None = False,
        **kwargs
    ):
        """
        Prints values to the console stream using the configured animations and styles.

        Any argument explicitly passed to this method will override the default 
        value set during the Init instance's initialization.

        Args:
            *values (object): Positional arguments to be printed (strings, objects, arrays).
            style (str, optional): Overrides the default animation style.
            speed (int | float, optional): Overrides the default animation speed.
            colors (tuple | str, optional): Overrides the default Colors object, accepting 
                                            a raw color definition (tuple, string) or None.
            background_color (tuple | str, optional): Specifies or overrides the background color.
            
            **kwargs: Additional keyword arguments passed directly to the core `printf` function.

        Returns:
            None: The function primarily handles output to the console.
        """
        if values == () and "help" not in (style, self.style):
            return

        # Perform Validation on overridden arguments
        if style:   _validate_style(style)
        if speed:   _validate_speed(speed)
        if delay:   _validate_delay(delay)
        if attrs:   _validate_attrs(attrs)
        if getmat:  _validate_getmat(getmat)

        # Process new color arguments into a Colors object if provided
        if colors or background_color:
            if type(colors).__name__ != "Colors":
                colors = Colors(colors, background_color)
        else:
            # Use the default Colors instance stored in the class
            colors = self._colors

        # Call the core printf function, merging defaults and overrides
        return pf(*values,
            style  = style  or self.style,
            speed  = speed  or self.speed,
            delay  = delay  or self.delay,
            getmat = getmat or self.getmat,
            attrs  = attrs  or self.attrs or [], 
            stay   = stay   if stay != None else self.stay,
            color  = colors,

            _validated_kwargs = True,
            _validated_colors = bool(colors),
            **kwargs,
        )
    
class init(Init):
    """
    (DEPRECATED) Alias for the Init class.

    This class exists purely for backwards compatibility and raises a warning 
    upon instantiation, encouraging users to switch to the new `Init` class.
    """
    def __init__(self, style = 'typing', speed = 3, delay = 0, stay = True, attrs = [], colors = None, getmat = False):
        from .colors import Font_Styles
        _Warning(self,
            "The class `init` is deprecated and will be removed in a future update. "
            f"Use `{Font_Styles.BOLD}Init{Font_Styles.RESET_BOLD}` instead."
        ).print()

        if attrs is None: attrs = []
        super().__init__(style, speed, delay, stay, attrs, colors, getmat)
