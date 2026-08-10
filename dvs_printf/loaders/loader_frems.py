# ---------------------
# LoaderFrems Factory
# ---------------------
class LoaderFrems:
    """Static factory for predefined spinners (lazy, cached)."""
    @property 
    def grow(self) -> str: return "grow"
    
    @property
    def line(self) -> str: return "line"
    
    @property
    def growvertical(self) -> str: return "growvertical"

    @property
    def mesh(self) -> str: return "mesh"

    @property
    def numbers(self) -> str: return "numbers"
    
    @property
    def spinner(self) -> str: return "spinner"


def refector(style):
    style = str(style)
    style_len = len(style)
    
    if style_len == 1:  return style
    if style_len >= 2:  return [style[0], style[-1]]

    return ["#", "."]

def get_bar_style(style, background_gray2, unfilled_bar_color, reset_color):
    """
    returns
    -------
    "characters" = {
        "characters": ...,
        "partial_len": ...,
        "full_block": ...,
        "border": ...,
    }
    """
    return {
        "grow": {   # grow
                "characters": [f"{background_gray2}{char}{background_gray2}{unfilled_bar_color}" for char in "▏▎▍▌▋▊▉█"],# 
                "partial_len": 1,
                "full_block": "█", 
                "border": "│"#│,│
            },
        "line": {   # line
                "characters": [f"{unfilled_bar_color}╺━", f"╸{unfilled_bar_color}━", f"━{unfilled_bar_color}╺"],
                "partial_len": 2, 
                "full_block": "━", 
                "border": ""
            },
        "growvertical": {   # growvertical
                "characters": [f"{background_gray2}{char}{reset_color}{unfilled_bar_color}" for char in " ▁▂▃▄▅▆▇█"],
                "partial_len": 1, 
                "full_block": "█", 
                "border": "│"
            },
        "mesh": {       # mesh
                "characters": [f"{background_gray2}{char}{reset_color}{unfilled_bar_color}" for char in "░▒▓█"],
                "partial_len": 1, 
                "full_block": "█░", 
                "border": "│"
            },
        "numbers": {    # numbers
                "characters": [f"{background_gray2}{char}{reset_color}{unfilled_bar_color}" for char in "0123456789"],
                "partial_len": 2, 
                "full_block": "#.", 
                "border": "│"
            },
        "spinner": {    # spinner
                "characters": [f"{unfilled_bar_color}{char}" for char in "___-``'´-___"],
                "partial_len": 1, 
                "full_block": ["#", "."], 
                "border": "[]"
            },
    }.get(style,        # "default":
            { 
                "characters": [f"{unfilled_bar_color}{char}" for char in "|/-\\|/-\\"],
                "partial_len": 1, 
                "full_block": refector(style), 
                "border": "[]"
            } 
        )


# def get_bar_style(style, background_gray2, unfilled_bar_color, reset_color):
#     """
#     returns
#     -------
#     "characters" = {
#         "characters": ...,
#         "partial_len": ...,
#         "full_block": ...,
#         "border": ...,
#     }
#     """
#     return {
#         "grow": {   # grow
#                 "characters": [f"{background_gray2}{char}{background_gray2}{unfilled_bar_color}" for char in "▏▎▍▌▋▊▉█"],# 
#                 "partial_len": 1,
#                 "full_block": "█", 
#                 "border": "│"#│,│
#             },
#         "line": {   # line
#                 "characters": [f"{unfilled_bar_color}╺━", f"╸{unfilled_bar_color}━", f"━{unfilled_bar_color}╺"],
#                 "partial_len": 2, 
#                 "full_block": "━", 
#                 "border": ""
#             },
#         "growvertical": {   # growvertical
#                 "characters": [f"{background_gray2}{char}{reset_color}{unfilled_bar_color}" for char in " ▁▂▃▄▅▆▇█"],
#                 "partial_len": 1, 
#                 "full_block": "█", 
#                 "border": "│"
#             },
#         "mesh": {       # mesh
#                 "characters": [f"{background_gray2}{char}{reset_color}{unfilled_bar_color}" for char in "░▒▓█"],
#                 "partial_len": 1, 
#                 "full_block": "█░", 
#                 "border": "│"
#             },
#         "numbers": {    # numbers
#                 "characters": [f"{background_gray2}{char}{reset_color}{unfilled_bar_color}" for char in "0123456789"],
#                 "partial_len": 2, 
#                 "full_block": "#.", 
#                 "border": "│"
#             },
#         "spinner": {    # spinner
#                 "characters": [f"{unfilled_bar_color}{char}" for char in "___-``'´-___"],
#                 "partial_len": 1, 
#                 "full_block": ["#", "."], 
#                 "border": "[]"
#             },
#     }.get(style,        # "default":
#             { 
#                 "characters": [f"{unfilled_bar_color}{char}" for char in "|/-\\|/-\\"],
#                 "partial_len": 1, 
#                 "full_block": refector(style), 
#                 "border": "[]"
#             } 
#         )


