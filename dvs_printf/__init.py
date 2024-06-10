from .__printf__ import printf as pf

class init:
    def __init__(self,style:str='typing',speed:int|float=3, 
    interval:int|float=1,stay:bool=True,getmat:bool|str=False):
        """
[dvs_printf Initializer](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#dvs_printfinit-method): allows to preset parameters for printf

---
#### Functions: 
```python
import dvs_printf

pf = dvs_printf.init()
printf = pf.printf

pf.set_style = "typing"
pf.set_speed = 3
pf.set_interval = 2
pf.set_stay = True
pf.set_getmat = False

printf(values, ..., keywords)    # The Core Printf Function 
```

---
#### Animation Styles: 
[typing, async, headline, newsline, mid, gunshort, snip, scatter, fire, wave, blink, \\
left, right, center, centerAC, centerAL, centerAR, matrix, matrix2, f2b, b2f, help] 
---
#### Parameters: 
style (str, optional): Different types of printing animation styles. 
    Defaults to 'typing'.
speed (int | float, optional): Speed of printf animation from 1 to 6 or 7. 
    Defaults to 3.
interval (int | float, optional): Waiting time between two lines. 
    Defaults to 1.
stay (bool, optional): Whether to keep the values displayed after animation. 
    Defaults to True.
getmat (bool | str, optional): Matrix data modifier for data structures like 
    PyTorch, TensorFlow, NumPy, Pandas, or lists. Defaults to False. 
     Set to True, "true", or "show" for matrix info.
        """

        [self._style,self._speed,self._interval,self._stay,
        self._getmat] = [style,speed,interval,stay,getmat]

    @property
    def style(self) -> str:
        """Different types of printing animation styles."""
        return self._style 
    
    @style.setter
    def set_style(self, value: str) -> None:
        """Sets the printing animation style."""
        self._style = value

    @property
    def speed(self) -> int | float:
        """Speed of printf animation from 1 to 6 or 7."""
        return self._speed
    
    @speed.setter
    def set_speed(self, value: int | float) -> None:
        """Sets the speed of the animation."""
        self._speed = value

    @property
    def interval(self) -> int | float:
        """Waiting time between two lines."""
        return self._interval
    
    @interval.setter
    def set_interval(self, value: int | float) -> None:
        """Sets the interval time between animations."""
        if (type(value) == int or type(value) == float) and value >= 0:
            self._interval = value
        else:raise ValueError("Interval must be a non-negative number (int or float).")

    @property
    def stay(self) -> bool:
        """Whether to keep the values displayed after animation."""
        return self._stay
    
    @stay.setter
    def set_stay(self, value: bool) -> None:
        """Sets whether to keep values displayed after animation."""
        self._stay = value

    @property
    def getmat(self) -> bool | str:
        """Matrix data modifier for data structures."""
        return self._getmat

    @getmat.setter
    def set_getmat(self, value: bool | str) -> None:
        """Sets the matrix data modifier."""
        if isinstance(value, (bool, str)) and (value in (True, False, "true", "show")):
            self._getmat = value
        else:raise ValueError("getmat must be True, False, 'true', or 'show'.")

    def printf(self, *values: any, 
        style:str|None=None,speed:int|float|None=None,interval:int|float|None=None, 
        stay:bool|None=None,getmat:bool|str|None=None) -> None:
        """
Prints values to a stream with animation. 

animation styles: [typing, async, headline, newsline, mid, gunshort, snip, scatter, fire, wave, 
    blink, left, right, center, centerAC, centerAL, centerAR, matrix, matrix2, f2b, b2f, help] 

Parameters: (overrides instance setting)
    *values: Values to be printed.
    style (str, optional): Animation style. 
    speed (int | float, optional): Animation speed.
    interval (int | float, optional): Delay between each lines.
    stay (bool, optional): Whether to keep values displayed after animation.
    getmat (bool | str, optional): Matrix data modifier.
        """
        pf(values, 
            style = style or self.style,
            speed = speed or self.speed,
            interval = interval or self.interval,
            stay = stay or self.stay,
            getmat = getmat or self.getmat )
        
