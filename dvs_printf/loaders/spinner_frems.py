from dataclasses import dataclass
from typing import List, Tuple, Union, Dict
from ..exceptions import SpinnerValueError, PEACH, PURPLE, RESET

SPINNERS_FREMS: Dict[str, Tuple[int, Union[str, List[str]]]] = {
    # Name            MiliSecond    Frems   
    "spinner"        : ( 100, "-\\|/-\\|"),
    "spinner2"       : ( 100, " ¯ &  |& _ &|  "),
    "halfArc"        : (  90, "(    &¯    & ¯   &  ¯  &   ¯ &    ¯&    )&    .&   . &  .  & .   &.    "),
    "barFlip"        : (  90, "|    &¯    & ¯   &  ¯  &   ¯ &    ¯&    |&    _&   _ &  _  & _   &_    "),
    "mirrorWave"     : ( 100, "|   |&¯   _& ¯ _ &  -  & _ ¯ &_   ¯&|   |&¯   _& ¯ _ &  -  & _ ¯ &_   ¯"),
    "growVertical"   : ( 120, "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"),
    "growHorizontal" : ( 120, "▏▎▍▌▋▊▉█▉▊▋▌▍▎▏"),
    "bounce"         : ( 120, "⠁⠂⠄⠂⠁"),
    "simpleDots"     : ( 200, ".   &..  &... &....&.   "),
    "flip"           : (  70, "___-``'´-___"),
    "arrow"          : ( 120, "▹▹▹▹▹&▸▹▹▹▹&▹▸▹▹▹&▹▹▸▹▹&▹▹▹▸▹&▹▹▹▹▸"),
    "aesthetic"      : (  80, "▰▱▱▱▱▱▱&▰▰▱▱▱▱▱&▰▰▰▱▱▱▱&▰▰▰▰▱▱▱&▰▰▰▰▰▱▱&▰▰▰▰▰▰▱&▰▰▰▰▰▰▰"),
    "point"          : ( 125, "∙∙∙&●∙∙&∙●∙&∙∙●&∙∙∙"),
    "poop"           : ( 180, "∙⁎⁕●෴ "),
    "moon"           : ( 140, "🌑🌒🌓🌔🌕🌖🌗🌘"),
    "clock"          : ( 100, "🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚"),
    "earth"          : ( 180, "🌍🌎🌏"),
    "runner"         : ( 140, "🚶🏃"),
    "smiley"         : ( 200, "☺️😊😀😃😄😁"),
    "funny"          : ( 200, "😄😝"),
    "hearts"         : ( 200, "♥️❤️🧡🩵🩶🩷💙💚💛💜🤍🤎🖤❤️‍🔥"),#♥️❤️🧡🩵🩶🩷💙💚💛💜🤍🤎🖤❤️‍🔥 // 💛💙💜💚❤️
    "dots"           : (  80,"⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"),
    "dots2"          : (  80, "⣾⣽⣻⢿⡿⣟⣯⣷"),
    "dots3"          : (  80, "⠋⠙⠚⠞⠖⠦⠴⠲⠳⠓"),
    "dots4"          : (  80, "⠄⠆⠇⠋⠙⠸⠰⠠⠰⠸⠙⠋⠇⠆"),
    "dots5"          : (  80, "⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦⠖⠒⠐⠐⠒⠓⠋"),
    "dots6"          : (  80, "⠁⠉⠙⠚⠒⠂⠂⠒⠲⠴⠤⠄⠄⠤⠴⠲⠒⠂⠂⠒⠚⠙⠉⠁"),
    "dots7"          : (  80, "⠈⠉⠋⠓⠒⠐⠐⠒⠖⠦⠤⠠⠠⠤⠦⠖⠒⠐⠐⠒⠓⠋⠉⠈"),
    "dots8"          : (  80, "⠁⠁⠉⠙⠚⠒⠂⠂⠒⠲⠴⠤⠄⠄⠤⠠⠠⠤⠦⠖⠒⠐⠐⠒⠓⠋⠉⠈⠈"),
    "dots9"          : (  80, "⢹⢺⢼⣸⣇⡧⡗⡏"),
    "dots10"         : (  80, "⢄⢂⢁⡁⡈⡐⡠"),
    "dots11"         : ( 100, "⠁⠂⠄⡀⢀⠠⠐⠈"),
    "dots8Bit"       : (  80, 
        "⠀⠁⠂⠃⠄⠅⠆⠇⡀⡁⡂⡃⡄⡅⡆⡇⠈⠉⠊⠋⠌⠍⠎⠏⡈⡉⡊⡋⡌⡍⡎⡏⠐⠑⠒⠓⠔⠕⠖⠗⡐⡑⡒⡓⡔⡕⡖⡗⠘⠙⠚⠛⠜⠝⠞⠟⡘⡙"
        "⡚⡛⡜⡝⡞⡟⠠⠡⠢⠣⠤⠥⠦⠧⡠⡡⡢⡣⡤⡥⡦⡧⠨⠩⠪⠫⠬⠭⠮⠯⡨⡩⡪⡫⡬⡭⡮⡯⠰⠱⠲⠳⠴⠵⠶⠷⡰⡱⡲⡳⡴⡵⡶⡷⠸⠹⠺⠻"
        "⠼⠽⠾⠿⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⣀⣁⣂⣃⣄⣅⣆⣇⢈⢉⢊⢋⢌⢍⢎⢏⣈⣉⣊⣋⣌⣍⣎⣏⢐⢑⢒⢓⢔⢕⢖⢗⣐⣑⣒⣓⣔⣕"
        "⣖⣗⢘⢙⢚⢛⢜⢝⢞⢟⣘⣙⣚⣛⣜⣝⣞⣟⢠⢡⢢⢣⢤⢥⢦⢧⣠⣡⣢⣣⣤⣥⣦⣧⢨⢩⢪⢫⢬⢭⢮⢯⣨⣩⣪⣫⣬⣭⣮⣯⢰⢱⢲⢳⢴⢵⢶⢷"
        "⣰⣱⣲⣳⣴⣵⣶⣷⢸⢹⢺⢻⢼⢽⢾⢿⣸⣹⣺⣻⣼⣽⣾⣿"),
    "dots12"         : (  80,
        "⢀⠀&⡀⠀&⠄⠀&⢂⠀&⡂⠀&⠅⠀&⢃⠀&⡃⠀&⠍⠀&⢋⠀&⡋⠀&⠍⠁&⢋⠁&⡋⠁&⠍⠉&⠋⠉&⠋⠉&⠉⠙&⠉⠙&⠉⠩&"
        "⠈⢙&⠈⡙&⢈⠩&⡀⢙&⠄⡙&⢂⠩&⡂⢘&⠅⡘&⢃⠨&⡃⢐&⠍⡐&⢋⠠&⡋⢀&⠍⡁&⢋⠁&⡋⠁&⠍⠉&⠋⠉&⠋⠉&⠉⠙&"
        "⠉⠙&⠉⠩&⠈⢙&⠈⡙&⠈⠩&⠀⢙&⠀⡙&⠀⠩&⠀⢘&⠀⡘&⠀⠨&⠀⢐&⠀⡐&⠀⠠&⠀⢀&⠀⡀"),
    "SlideDot"       : (  80, 
        "│.         │&│..        │&│...       │&│....      │&│ ....     │&│  ....    │&"
        "│   ....   │&│    ....  │&│     .... │&│      ....│&│       ...│&│        ..│&"
        "│         .│&│         .│&│        ..│&│       ...│&│      ....│&│     .... │&"
        "│    ....  │&│   ....   │&│  ....    │&│ ....     │&│....      │&│...       │&"
        "│..        │&│.         │"),
    "SlideDotSimple" : (  80, 
        "│.         │&│ .        │&│  .       │&│   .      │&│    .     │&│     .    │&"
        "│      .   │&│       .  │&│        . │&│         .│&│        . │&│       .  │&"
        "│      .   │&│     .    │&│    .     │&│   .      │&│  .       │&│ .        │&"
        "│.         │"),
    "longBounce"     : ( 120,
        "│⠁          │&│⠁¯         │&│ ¯¯        │&│ ¯¯¯       │&│  ¯¯       │&│   ¯       │&"
        "│    ⠂      │&│     ⠄     │&│      ⠂    │&│       ¯   │&│       ¯¯  │&│       ¯¯¯ │&"
        "│        ¯¯ │&│         ¯⠁│&│          ⠁│&│          ⠁│&│         ¯⠁│&│        ¯¯ │&"
        "│       ¯¯¯ │&│       ¯¯  │&│       ¯   │&│      ⠂    │&│     ⠄     │&│    ⠂      │&"
        "│   ¯       │&│  ¯¯       │&│ ¯¯¯       │&│ ¯¯        │&│⠁¯         │&│⠁          │"),
    "bouncingBar"    : ( 100, 
        "[=   ]&[==  ]&[=== ]&[ ===]&[  ==]&[   =]&"
        "[   =]&[  ==]&[ ===]&[====]&[=== ]&[==  ]&[=   ]"),
    "bouncingBall"   : (  80, 
        "(●     )&( ●    )&(  ●   )&(   ●  )&(    ● )&"
        "(     ●)&(    ● )&(   ●  )&(  ●   )&( ●    )"),
    "pong"           : (  80, 
        "▐⠂       ▌&▐⠈       ▌&▐ ⠂      ▌&▐ ⠠      ▌&▐  ⡀     ▌&▐  ⠠     ▌&▐   ⠂    ▌&"
        "▐   ⠈    ▌&▐    ⠂   ▌&▐    ⠠   ▌&▐     ⡀  ▌&▐     ⠠  ▌&▐      ⠂ ▌&▐      ⠈ ▌&"
        "▐       ⠂▌&▐       ⠠▌&▐       ⡀▌&▐      ⠠ ▌&▐      ⠂ ▌&▐     ⠈  ▌&▐     ⠂  ▌&"
        "▐    ⠠   ▌&▐    ⡀   ▌&▐   ⠠    ▌&▐   ⠂    ▌&▐  ⠈     ▌&▐  ⠂     ▌&▐ ⠠      ▌&"
        "▐ ⡀      ▌&▐⠠       ▌"),
    "shark"          : ( 120,                
        "|\\____________&_|\\___________&__|\\__________&___|\\_________&____|\\________&"
        "_____|\\_______&______|\\______&_______|\\_____&________|\\____&_________|\\___&"
        "__________|\\__&___________|\\_&____________|\\&____________/|&___________/|_&"
        "__________/|__&_________/|___&________/|____&_______/|_____&______/|______&"
        "_____/|_______&____/|________&___/|_________&__/|__________&_/|___________&"
        "/|____________"),
    "domino"         : ( 120,
        "|||||&/||||&_||||&_/|||&__|||&__/||&___||&___/|&____|&____/&_____&_____&"
        "|||||&|||||&||||\\&||||_&|||\\_&|||__&||\\__&||___&|\\___&|____&\\____&_____"),
    "loaderGrow"     : (  40,
        "▏    &▎    &▍    &▌    &▋    &▊    &█▏   &█▎   &█▍   &█▌   &█▋   &█▊   &██▏  &"
        "██▎  &██▍  &██▌  &██▋  &██▊  &███▏ &███▎ &███▍ &███▌ &███▋ &███▊ &████▏&████▎&"
        "████▍&████▌&████▋&████▊&████▊&█████&█████&████▋&████▌&████▍&████▎&████▏&███▊ &"
        "███▋ &███▌ &███▍ &███▎ &███▏ &██▊  &██▋  &██▌  &██▍  &██▎  &██▏  &█▊   &█▋   &"
        "█▌   &█▍   &█▎   &█▏   &▊    &▋    &▌    &▍    &▎    &▏    "),
}
"""
    A static dictionary containing the raw configuration for all available spinner animations.

    Each entry maps a style name (str) to a tuple containing:
        1. Delay (int): The duration (in milliseconds) to pause between frames.
        2. Frames (str | List[str]): The sequence of characters/strings that make up the animation.
           If a string contains '&', it is split into individual frames at runtime.
"""


def Get_SPINNERS(name:str) -> Tuple[int, str | list]:
    '''
    Retrieve a spinner configuration by name.

    Looks up a spinner from the global `SPINNERS` dict by `name`, defaulting to 'spinner'\\
    Returns the delay and either a string or list as Spinner Frems.

    Parameters:
        name (str): The key used to look up the spinner in the `SPINNERS` dictionary.

    Returns:
        Spinner_Tuple (Tuple[int, str | list]): A tuple where the first element is the spinner delay in seconds (int),\\
        and the second element is either a string or a list of strings as Spinner Frems.
    '''
    try:
        _Sec, _Spinner = SPINNERS_FREMS[name] 

        return _Sec, (  _Spinner.split('&') if '&' in _Spinner else 
                        _Spinner
                    )
    except:
        raise SpinnerValueError(
            error_value=name, 
            keyWord='style',
            message=f"The style name {PEACH}{name}{RESET} is not defined.",
        )


# -----------------
# Spinner dataclass
# -----------------
@dataclass(frozen=True)
class Spinner_Frem:
    """A dataclass to hold the properties of a single spinner animation."""
    delay_ms: int
    frames: Union[List[str], str]
    __name__ = "Spinner_Frem"
    
    def __iter__(self): # Yield values in order (delay, frames)
        yield self.delay_ms
        yield self.frames


# ----------------------------
# Classproperty implementation
# ----------------------------
class classproperty(property):
#   def __init__(self, func):
#       self.func = func
#       self.cache_name = f"__cached_{func.__name__}"

    def __get__(self, obj, cls):
        return self.fget(cls)
    
# ---------------------
# SpinnerFrems Factory
# ---------------------
class SpinnerFrems:
    """Static factory for predefined spinners (lazy, cached)."""
    spinner        : Spinner_Frem = "spinner"
    spinner2       : Spinner_Frem = "spinner2"
    halfArc        : Spinner_Frem = "halfArc"
    barFlip        : Spinner_Frem = "barFlip"
    mirrorWave     : Spinner_Frem = "mirrorWave"
    growVertical   : Spinner_Frem = "growVertical"
    growHorizontal : Spinner_Frem = "growHorizontal"
    bounce         : Spinner_Frem = "bounce"
    simpleDots     : Spinner_Frem = "simpleDots"
    flip           : Spinner_Frem = "flip"
    arrow          : Spinner_Frem = "arrow"
    aesthetic      : Spinner_Frem = "aesthetic"
    point          : Spinner_Frem = "point"
    poop           : Spinner_Frem = "poop"
    moon           : Spinner_Frem = "moon"
    clock          : Spinner_Frem = "clock"
    earth          : Spinner_Frem = "earth"
    runner         : Spinner_Frem = "runner"
    smiley         : Spinner_Frem = "smiley"
    funny          : Spinner_Frem = "funny"
    hearts         : Spinner_Frem = "hearts"
    dots           : Spinner_Frem = "dots"
    dots2          : Spinner_Frem = "dots2"
    dots3          : Spinner_Frem = "dots3"
    dots4          : Spinner_Frem = "dots4"
    dots5          : Spinner_Frem = "dots5"
    dots6          : Spinner_Frem = "dots6"
    dots7          : Spinner_Frem = "dots7"
    dots8          : Spinner_Frem = "dots8"
    dots9          : Spinner_Frem = "dots9"
    dots10         : Spinner_Frem = "dots10"
    dots11         : Spinner_Frem = "dots11"
    dots8Bit       : Spinner_Frem = "dots8Bit"
    dots12         : Spinner_Frem = "dots12"
    SlideDot       : Spinner_Frem = "SlideDot"
    SlideDotSimple : Spinner_Frem = "SlideDotSimple"
    longBounce     : Spinner_Frem = "longBounce"
    bouncingBar    : Spinner_Frem = "bouncingBar"
    bouncingBall   : Spinner_Frem = "bouncingBall"
    pong           : Spinner_Frem = "pong"
    shark          : Spinner_Frem = "shark"
    domino         : Spinner_Frem = "domino"
    loaderGrow     : Spinner_Frem = "loaderGrow"


    @staticmethod
    def _get(name: str) -> Spinner_Frem:
        delay, frames = SPINNERS_FREMS[name]
        frames = frames.split("&") if isinstance(frames, str) and "&" in frames else frames
        return Spinner_Frem(delay, frames)
    
    # ================= (Example After for Loop) =================
    # This Is Dynamically attach classproperties 
    # @property
    # def bounce(self) -> Spinner_Frem: return self._get("bounce")
    # ============================================================


# ----------------------------------
# Dynamically attach classproperties
# ----------------------------------
for name in SPINNERS_FREMS:
    setattr(
        SpinnerFrems, name,
        classproperty(lambda cls, n=name: cls._get(n))
    )






